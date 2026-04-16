import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import threading
import time
from datetime import datetime

AUTHORIZED_FOLDER = r"Images\"
THRESHOLD         = 0.52
FRAME_W, FRAME_H  = 640, 480

BG        = "#070d14"
PANEL     = "#0b1520"
ACCENT    = "#00e5ff"
GREEN     = "#00ff88"
RED       = "#ff2d55"
AMBER     = "#ffb300"
MUTED     = "#1e3048"
TEXT      = "#cfe8ff"
SUBTEXT   = "#3d6080"

authorized_encodings, authorized_names = [], []
for f in os.listdir(AUTHORIZED_FOLDER):
    if f.lower().endswith((".jpg", ".jpeg", ".png")):
        path  = os.path.join(AUTHORIZED_FOLDER, f)
        img   = cv2.imread(path)
        if img is None: continue
        rgb   = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encs  = face_recognition.face_encodings(rgb)
        if encs:
            authorized_encodings.append(encs[0])
            authorized_names.append(os.path.splitext(f)[0])

class FaceUnlockApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Face Unlock")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.cap        = None
        self.running    = False
        self.status     = "STANDBY"
        self.log_lines  = []
        self.pulse_phase= 0.0

        self._build_ui()
        self._animate_pulse()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.mainloop()

    def _build_ui(self):
        W = self.root

        top = tk.Frame(W, bg=PANEL, height=52)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        tk.Label(top, text="◈", font=("Consolas", 18, "bold"),
                 fg=ACCENT, bg=PANEL).pack(side=tk.LEFT, padx=(18,6), pady=10)
        tk.Label(top, text="FACE UNLOCK SYSTEM", font=("Consolas", 14, "bold"),
                 fg=TEXT, bg=PANEL).pack(side=tk.LEFT, pady=10)

        self.clock_lbl = tk.Label(top, text="", font=("Consolas", 10),
                                   fg=SUBTEXT, bg=PANEL)
        self.clock_lbl.pack(side=tk.RIGHT, padx=18)
        self._tick_clock()

        tk.Label(top, text=f"  {len(authorized_encodings)} authorized  ",
                 font=("Consolas", 9), fg=ACCENT, bg=MUTED).pack(side=tk.RIGHT, pady=14)

        body = tk.Frame(W, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        cam_wrap = tk.Frame(body, bg=MUTED, padx=2, pady=2)
        cam_wrap.pack(side=tk.LEFT, padx=(16,8), pady=16)

        self.cam_lbl = tk.Label(cam_wrap, bg="#000", width=FRAME_W, height=FRAME_H)
        self.cam_lbl.pack()

        self._show_placeholder()

        right = tk.Frame(body, bg=BG, width=280)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=(0,16), pady=16)
        right.pack_propagate(False)

        self.ring_canvas = tk.Canvas(right, width=200, height=200,
                                      bg=BG, highlightthickness=0)
        self.ring_canvas.pack(pady=(10,0))
        self._draw_ring(SUBTEXT, "STANDBY")

        stats = tk.Frame(right, bg=BG)
        stats.pack(fill=tk.X, pady=(10,4))
        self.faces_var  = tk.StringVar(value="0")
        self.unlock_var = tk.StringVar(value="0")
        self._stat_box(stats, "FACES\nDETECTED", self.faces_var).pack(side=tk.LEFT, expand=True)
        self._stat_box(stats, "UNLOCKS\nTODAY",   self.unlock_var).pack(side=tk.LEFT, expand=True)
        self.unlock_count = 0

        tk.Frame(right, bg=MUTED, height=1).pack(fill=tk.X, pady=8)

        tk.Label(right, text="AUTHORIZED IDs", font=("Consolas", 9, "bold"),
                 fg=SUBTEXT, bg=BG).pack(anchor="w", padx=6)
        for name in authorized_names:
            row = tk.Frame(right, bg=BG)
            row.pack(fill=tk.X, padx=6, pady=2)
            tk.Label(row, text="●", fg=GREEN, bg=BG,
                     font=("Consolas", 8)).pack(side=tk.LEFT)
            tk.Label(row, text=f"  {name}", font=("Consolas", 9),
                     fg=TEXT, bg=BG).pack(side=tk.LEFT)

        tk.Frame(right, bg=MUTED, height=1).pack(fill=tk.X, pady=8)

        tk.Label(right, text="EVENT LOG", font=("Consolas", 9, "bold"),
                 fg=SUBTEXT, bg=BG).pack(anchor="w", padx=6)
        self.log_frame = tk.Frame(right, bg=BG)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=6)

        btn_row = tk.Frame(right, bg=BG)
        btn_row.pack(fill=tk.X, pady=(10,0))
        self.start_btn = self._btn(btn_row, "▶  START", ACCENT,  BG,     self._start)
        self.start_btn.pack(side=tk.LEFT, expand=True, padx=(0,4), ipady=8)
        self._btn(btn_row, "■  STOP",  MUTED,  TEXT,   self._stop
                  ).pack(side=tk.LEFT, expand=True, padx=(4,0), ipady=8)

    def _stat_box(self, parent, label, var):
        f = tk.Frame(parent, bg=MUTED, padx=10, pady=8)
        tk.Label(f, textvariable=var, font=("Consolas", 22, "bold"),
                 fg=ACCENT, bg=MUTED).pack()
        tk.Label(f, text=label, font=("Consolas", 7), fg=SUBTEXT,
                 bg=MUTED, justify="center").pack()
        return f

    def _btn(self, parent, text, bg, fg, cmd):
        return tk.Button(parent, text=text, font=("Consolas", 9, "bold"),
                         bg=bg, fg=fg, activebackground=MUTED,
                         activeforeground=TEXT, relief=tk.FLAT,
                         cursor="hand2", bd=0, command=cmd)

    def _draw_ring(self, color, label, pct=0):
        c = self.ring_canvas
        c.delete("all")
        cx, cy, r = 100, 100, 72
        c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=MUTED, width=8)
        if pct > 0:
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=90, extent=-int(pct*360),
                         outline=color, width=8, style="arc")
        c.create_text(cx, cy-10, text=label,
                      font=("Consolas", 13, "bold"), fill=color)
        now = datetime.now().strftime("%H:%M:%S")
        c.create_text(cx, cy+12, text=now,
                      font=("Consolas", 9), fill=SUBTEXT)

    def _animate_pulse(self):
        if self.running and self.status == "UNLOCKED":
            self.pulse_phase = (self.pulse_phase + 0.06) % 1.0
            self._draw_ring(GREEN, "UNLOCKED", self.pulse_phase)
        self.root.after(40, self._animate_pulse)

    def _show_placeholder(self):
        img = Image.new("RGB", (FRAME_W, FRAME_H), "#070d14")
        d   = ImageDraw.Draw(img)
        cx, cy = FRAME_W//2, FRAME_H//2
        for i, r in enumerate(range(20, 160, 28)):
            alpha = 60 - i*8
            d.ellipse([cx-r, cy-r, cx+r, cy+r],
                      outline=(0, 60, 80), width=1)
        d.text((cx-90, cy+170), "CAMERA STANDBY — PRESS START", fill=(30, 80, 100))
        self._set_frame(img)

    def _start(self):
        if self.running: return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self._log("ERR", "Webcam not found", RED)
            return
        self.running = True
        self._log("SYS", "Camera started", ACCENT)
        threading.Thread(target=self._cam_loop, daemon=True).start()

    def _stop(self):
        self.running = False
        if self.cap: self.cap.release()
        self._show_placeholder()
        self._draw_ring(SUBTEXT, "STANDBY")
        self.status = "STANDBY"
        self._log("SYS", "Camera stopped", AMBER)

    def _cam_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret: break

            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locs  = face_recognition.face_locations(rgb, model="hog")
            encs  = face_recognition.face_encodings(rgb, locs)

            num_faces = len(encs)
            self.faces_var.set(str(num_faces))

            pil = Image.fromarray(rgb).resize((FRAME_W, FRAME_H))
            draw = ImageDraw.Draw(pil)

            unlocked_any = False
            for (top, right, bottom, left), enc in zip(locs, encs):
                sy = FRAME_H / frame.shape[0]
                sx = FRAME_W / frame.shape[1]
                t,r,b,l = int(top*sy), int(right*sx), int(bottom*sy), int(left*sx)

                unlocked, name = False, "UNKNOWN"
                if authorized_encodings:
                    dists = face_recognition.face_distance(authorized_encodings, enc)
                    idx   = dists.argmin()
                    if dists[idx] < THRESHOLD:
                        unlocked = True
                        name     = authorized_names[idx]

                color = GREEN if unlocked else RED
                col_t = (0,255,136) if unlocked else (255,45,85)

                for pw in [4,2,1]:
                    draw.rectangle([l-pw, t-pw, r+pw, b+pw], outline=col_t, width=1)

                sz = 14
                for x1,y1,dx,dy in [(l,t,1,1),(r,t,-1,1),(l,b,1,-1),(r,b,-1,-1)]:
                    draw.line([x1,y1, x1+dx*sz,y1], fill=col_t, width=3)
                    draw.line([x1,y1, x1,y1+dy*sz], fill=col_t, width=3)

                label = f"{'✓' if unlocked else '✗'}  {name}"
                draw.rectangle([l, t-22, l+len(label)*8+6, t], fill=col_t)
                draw.text((l+4, t-20), label, fill=(10,10,10))

                if unlocked:
                    unlocked_any = True
                    self._log("OK", f"Unlocked: {name}", GREEN)

            draw.text((10, 10), f"FACES: {num_faces}", fill=(0,229,255))
            draw.text((10, 28), datetime.now().strftime("%H:%M:%S"), fill=(30,80,100))

            self._set_frame(pil)

            if num_faces == 0:
                self.status = "SCANNING"
                self.root.after(0, lambda: self._draw_ring(AMBER, "SCANNING", 0))
            elif unlocked_any:
                if self.status != "UNLOCKED":
                    self.status = "UNLOCKED"
                    self.unlock_count += 1
                    self.unlock_var.set(str(self.unlock_count))
            else:
                self.status = "LOCKED"
                self.root.after(0, lambda: self._draw_ring(RED, "LOCKED", 1.0))

            time.sleep(0.03)

    def _set_frame(self, pil_img):
        imgtk = ImageTk.PhotoImage(pil_img)
        self.cam_lbl.config(image=imgtk)
        self.cam_lbl._img = imgtk

    def _log(self, tag, msg, color=TEXT):
        ts = datetime.now().strftime("%H:%M:%S")
        if self.log_lines and self.log_lines[-1][1] == msg:
            return
        self.log_lines.append((ts, msg))
        if len(self.log_lines) > 6:
            self.log_lines.pop(0)
        for w in self.log_frame.winfo_children():
            w.destroy()
        for ts_, msg_ in self.log_lines:
            row = tk.Frame(self.log_frame, bg=BG)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=ts_, font=("Consolas", 7), fg=SUBTEXT, bg=BG).pack(side=tk.LEFT)
            tk.Label(row, text=f"  {msg_}", font=("Consolas", 8),
                     fg=color, bg=BG).pack(side=tk.LEFT)

    def _tick_clock(self):
        self.clock_lbl.config(text=datetime.now().strftime("%a %d %b  %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _quit(self):
        self.running = False
        if self.cap: self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    if not authorized_encodings:
        raise ValueError("No authorized faces loaded. Check your folder path.")
    FaceUnlockApp()
