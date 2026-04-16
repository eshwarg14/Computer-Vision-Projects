import tkinter as tk
import cv2, threading, time, math
from PIL import Image, ImageTk

try:
    from deepface import DeepFace
    def ANALYZE(f):
        return DeepFace.analyze(f, actions=["emotion"], enforce_detection=False, silent=True)[0]
except ImportError:
    def ANALYZE(f):
        t = time.time()
        raw = {e: max(0.1, math.sin(t*s+o)*30+b) for e,s,o,b in
               [("happy",0.5,0,45),("neutral",0.3,1,25),("sad",0.7,2,12),
                ("angry",0.9,3,8),("surprise",1.1,4,5),("fear",0.6,5,3),("disgust",0.4,6,2)]}
        total = sum(raw.values())
        pct = {k: v/total*100 for k,v in raw.items()}
        h, w = f.shape[:2]
        return {"dominant_emotion": max(pct, key=pct.get), "emotion": pct,
                "region": {"x": w//4, "y": h//6, "w": w//2, "h": h*2//3}}

COLORS = {"happy":"#FFD700","sad":"#6495ED","angry":"#FF4500",
          "surprise":"#FF69B4","fear":"#9370DB","disgust":"#32CD32","neutral":"#A0A0A0"}
ICONS  = {"happy":"😊","sad":"😢","angry":"😠","surprise":"😲",
          "fear":"😨","disgust":"🤢","neutral":"😐"}

CAM_W, CAM_H = 580, 440

class EmotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Recognition")
        self.root.configure(bg="#0D0F1A")
        self.root.geometry("920x540")
        self.root.resizable(False, False)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.result, self.paused = None, False
        self.lock = threading.Lock()
        self.analyzing = False
        self.last_analyze = 0

        self._build_ui()
        self._cam_loop()

        self.analyze_thread_active = False
        threading.Thread(target=self._analyze_loop, daemon=True).start()

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg="#0D0F1A")
        hdr.pack(fill="x", padx=16, pady=8)
        tk.Label(hdr, text="◈ EMOTICA", font=("Courier New",18,"bold"),
                 fg="#4F6EF7", bg="#0D0F1A").pack(side="left")
        self.fps_var = tk.StringVar(value="FPS: —")
        tk.Label(hdr, textvariable=self.fps_var, font=("Courier New",9),
                 fg="#5A6080", bg="#0D0F1A").pack(side="right")

        body = tk.Frame(self.root, bg="#0D0F1A")
        body.pack(fill="both", expand=True, padx=16, pady=(0,12))

        self.cam_lbl = tk.Label(body, bg="#13162A", width=CAM_W, height=CAM_H)
        self.cam_lbl.pack(side="left")
        self.cam_lbl.pack_propagate(False)

        right = tk.Frame(body, bg="#0D0F1A", width=270)
        right.pack(side="right", fill="y", padx=(10,0))
        right.pack_propagate(False)

        card = tk.Frame(right, bg="#1A1E35")
        card.pack(fill="x", pady=(0,8))
        tk.Label(card, text="DOMINANT", font=("Courier New",8),
                 fg="#5A6080", bg="#1A1E35").pack(anchor="w", padx=12, pady=(8,0))
        self.emoji_lbl = tk.Label(card, text="—", font=("Segoe UI Emoji",32), bg="#1A1E35")
        self.emoji_lbl.pack(anchor="w", padx=12)
        self.dom_lbl = tk.Label(card, text="SCANNING", font=("Courier New",20,"bold"),
                                fg="#5A6080", bg="#1A1E35")
        self.dom_lbl.pack(anchor="w", padx=12, pady=(0,10))

        bars_frame = tk.Frame(right, bg="#1A1E35")
        bars_frame.pack(fill="x", pady=(0,8))
        tk.Label(bars_frame, text="EMOTION SCORES", font=("Courier New",8),
                 fg="#5A6080", bg="#1A1E35").pack(anchor="w", padx=12, pady=(8,4))
        self.bars, self.pct_vars = {}, {}
        for e, col in COLORS.items():
            row = tk.Frame(bars_frame, bg="#1A1E35")
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text=f"{ICONS[e]} {e:<8}", font=("Courier New",8),
                     fg="#5A6080", bg="#1A1E35", width=11, anchor="w").pack(side="left")
            c = tk.Canvas(row, height=10, width=110, bg="#13162A", bd=0, highlightthickness=0)
            c.pack(side="left", padx=3)
            self.bars[e] = c
            v = tk.StringVar(value="0%")
            tk.Label(row, textvariable=v, font=("Courier New",8),
                     fg=col, bg="#1A1E35", width=4).pack(side="left")
            self.pct_vars[e] = v
        tk.Frame(bars_frame, bg="#1A1E35", height=8).pack()

        tk.Button(right, text="⏸ PAUSE", font=("Courier New",9),
                  fg="#E8ECF8", bg="#4F6EF7", bd=0, pady=6, cursor="hand2",
                  command=self._toggle).pack(fill="x", pady=(0,4))
        tk.Button(right, text="✕ QUIT", font=("Courier New",9),
                  fg="#5A6080", bg="#1A1E35", bd=0, pady=6, cursor="hand2",
                  command=self._quit).pack(fill="x")

    def _cam_loop(self):
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                self._last_frame = frame

                with self.lock:
                    res = self.result
                if res:
                    reg = res.get("region", {})
                    x, y, w, h = reg.get("x",0), reg.get("y",0), reg.get("w",0), reg.get("h",0)
                    if w > 0 and h > 0:
                        hx = COLORS.get(res["dominant_emotion"], "#FFFFFF")
                        bgr = (int(hx[5:7],16), int(hx[3:5],16), int(hx[1:3],16))
                        for px,py,dx,dy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
                            cv2.line(frame,(px,py),(px+dx*20,py),bgr,2)
                            cv2.line(frame,(px,py),(px,py+dy*20),bgr,2)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb).resize((CAM_W, CAM_H), Image.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_lbl.imgtk = imgtk
                self.cam_lbl.configure(image=imgtk)

        self.root.after(30, self._cam_loop)

    def _analyze_loop(self):
        while True:
            time.sleep(0.5)
            if self.paused or not hasattr(self, "_last_frame"):
                continue
            try:
                frame = self._last_frame.copy()
                res = ANALYZE(frame)
                with self.lock:
                    self.result = res
                self.root.after(0, self._update_ui)
            except Exception:
                pass

    def _update_ui(self):
        with self.lock:
            res = self.result
        if not res:
            return
        dom = res["dominant_emotion"]
        self.emoji_lbl.config(text=ICONS.get(dom, "?"))
        self.dom_lbl.config(text=dom.upper(), fg=COLORS.get(dom, "#A0A0A0"))
        for e, val in res["emotion"].items():
            self.pct_vars[e].set(f"{val:.0f}%")
            c = self.bars[e]
            c.delete("all")
            c.create_rectangle(0, 0, 110, 10, fill="#13162A", outline="")
            filled = int(val / 100 * 110)
            if filled > 0:
                c.create_rectangle(0, 0, filled, 10, fill=COLORS[e], outline="")

    def _toggle(self):
        self.paused = not self.paused

    def _quit(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionApp(root)
    root.protocol("WM_DELETE_WINDOW", app._quit)
    root.mainloop()
