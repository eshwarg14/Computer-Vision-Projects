import cv2
import mediapipe as mp
import math, time, threading, winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime

EAR_THRESHOLD    = 0.22
CLOSED_TIME_LIMIT= 1.5
L_EYE = [33, 160, 158, 133, 153, 144]
R_EYE = [263, 387, 385, 362, 380, 373]
FRAME_W, FRAME_H = 640, 480

BG     = "#06080f"
PANEL  = "#0c1220"
MUTED  = "#121e30"
ACCENT = "#00cfff"
GREEN  = "#00ff9d"
RED    = "#ff2d55"
AMBER  = "#ffaa00"
TEXT   = "#c8e0f4"
DIM    = "#2a4060"

class Alarm:
    def __init__(self):
        self.active = False
    def _loop(self):
        while self.active:
            winsound.Beep(1800, 250)
            time.sleep(0.1)
    def start(self):
        if not self.active:
            self.active = True
            threading.Thread(target=self._loop, daemon=True).start()
    def stop(self):
        self.active = False

def get_ear(lm, idx, w, h):
    p = [(int(lm[i].x*w), int(lm[i].y*h)) for i in idx]
    return (math.dist(p[1],p[5]) + math.dist(p[2],p[4])) / (2*math.dist(p[0],p[3]))

class DrowsinessApp:
    def __init__(self):
        self.root      = tk.Tk()
        self.root.title("Drowsiness Detector")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.alarm          = Alarm()
        self.face_mesh      = mp.solutions.face_mesh.FaceMesh(
                                refine_landmarks=True, max_num_faces=1)
        self.cap            = None
        self.running        = False
        self.closed_start   = None
        self.alert_count    = 0
        self.ear_history    = [0.3] * 60

        self._build_ui()
        self._tick_clock()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.mainloop()

    def _build_ui(self):
        top = tk.Frame(self.root, bg=PANEL, height=50)
        top.pack(fill=tk.X); top.pack_propagate(False)
        tk.Label(top, text="◈  DROWSINESS DETECTION SYSTEM",
                 font=("Consolas",13,"bold"), fg=ACCENT, bg=PANEL).pack(side=tk.LEFT, padx=18, pady=12)
        self.clock_lbl = tk.Label(top, text="", font=("Consolas",9), fg=DIM, bg=PANEL)
        self.clock_lbl.pack(side=tk.RIGHT, padx=18)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True)

        cam_border = tk.Frame(body, bg=DIM, padx=2, pady=2)
        cam_border.pack(side=tk.LEFT, padx=(14,8), pady=14)
        self.cam_lbl = tk.Label(cam_border, bg="#000", width=FRAME_W, height=FRAME_H)
        self.cam_lbl.pack()
        self._placeholder()

        right = tk.Frame(body, bg=BG, width=270)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=(0,14), pady=14)
        right.pack_propagate(False)

        self.ring = tk.Canvas(right, width=200, height=200,
                               bg=BG, highlightthickness=0)
        self.ring.pack(pady=(8,0))
        self._draw_ring("STANDBY", DIM, 0)

        tk.Label(right, text="EAR LEVEL", font=("Consolas",8,"bold"),
                 fg=DIM, bg=BG).pack(anchor="w", padx=8, pady=(10,2))
        self.ear_canvas = tk.Canvas(right, width=254, height=36,
                                     bg=MUTED, highlightthickness=0)
        self.ear_canvas.pack(padx=8)

        stats = tk.Frame(right, bg=BG); stats.pack(fill=tk.X, pady=8)
        self.ear_var   = tk.StringVar(value="0.00")
        self.dur_var   = tk.StringVar(value="0.0s")
        self.alert_var = tk.StringVar(value="0")
        self._stat(stats, "EAR",      self.ear_var,   ACCENT).pack(side=tk.LEFT, expand=True)
        self._stat(stats, "CLOSED",   self.dur_var,   AMBER).pack(side=tk.LEFT, expand=True)
        self._stat(stats, "ALERTS",   self.alert_var, RED).pack(side=tk.LEFT, expand=True)

        tk.Frame(right, bg=MUTED, height=1).pack(fill=tk.X, padx=8, pady=6)

        for label, val in [("EAR Threshold", f"{EAR_THRESHOLD}"),
                            ("Alert After",   f"{CLOSED_TIME_LIMIT}s")]:
            row = tk.Frame(right, bg=BG); row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=label, font=("Consolas",8), fg=DIM,  bg=BG).pack(side=tk.LEFT)
            tk.Label(row, text=val,   font=("Consolas",8,"bold"), fg=TEXT, bg=BG).pack(side=tk.RIGHT)

        tk.Frame(right, bg=MUTED, height=1).pack(fill=tk.X, padx=8, pady=6)

        tk.Label(right, text="EVENT LOG", font=("Consolas",8,"bold"),
                 fg=DIM, bg=BG).pack(anchor="w", padx=10)
        self.log_frame = tk.Frame(right, bg=BG)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        self._log_lines = []

        btn = tk.Frame(right, bg=BG); btn.pack(fill=tk.X, pady=(6,0))
        self._btn(btn, "▶  START", GREEN, BG,   self._start).pack(side=tk.LEFT, expand=True, padx=(0,3), ipady=9)
        self._btn(btn, "■  STOP",  MUTED, TEXT,  self._stop ).pack(side=tk.LEFT, expand=True, padx=(3,0), ipady=9)

    def _stat(self, parent, label, var, color):
        f = tk.Frame(parent, bg=MUTED, padx=8, pady=6)
        tk.Label(f, textvariable=var, font=("Consolas",16,"bold"), fg=color, bg=MUTED).pack()
        tk.Label(f, text=label, font=("Consolas",7), fg=DIM, bg=MUTED).pack()
        return f

    def _btn(self, parent, text, bg, fg, cmd):
        return tk.Button(parent, text=text, font=("Consolas",9,"bold"),
                         bg=bg, fg=fg, activebackground=MUTED, activeforeground=TEXT,
                         relief=tk.FLAT, cursor="hand2", bd=0, command=cmd)

    def _draw_ring(self, label, color, pct):
        c = self.ring; c.delete("all")
        cx, cy, r = 100, 100, 68
        c.create_oval(cx-r,cy-r,cx+r,cy+r, outline=MUTED, width=9)
        if pct > 0:
            c.create_arc(cx-r,cy-r,cx+r,cy+r, start=90, extent=-int(pct*360),
                         outline=color, width=9, style="arc")
        c.create_text(cx, cy-10, text=label, font=("Consolas",13,"bold"), fill=color)
        c.create_text(cx, cy+12, text=datetime.now().strftime("%H:%M:%S"),
                      font=("Consolas",9), fill=DIM)

    def _draw_ear_bar(self, ear):
        c = self.ear_canvas; c.delete("all")
        self.ear_history.append(ear)
        self.ear_history.pop(0)
        W, H = 254, 36
        bar_w = W / len(self.ear_history)
        for i, v in enumerate(self.ear_history):
            bh    = int(min(v / 0.4, 1.0) * H)
            color = GREEN if v >= EAR_THRESHOLD else RED
            x = int(i * bar_w)
            c.create_rectangle(x, H-bh, x+max(1,int(bar_w)-1), H, fill=color, outline="")
        ty = H - int(EAR_THRESHOLD / 0.4 * H)
        c.create_line(0, ty, W, ty, fill=AMBER, dash=(4,2))

    def _placeholder(self):
        img = Image.new("RGB", (FRAME_W, FRAME_H), "#06080f")
        d   = ImageDraw.Draw(img)
        cx, cy = FRAME_W//2, FRAME_H//2
        for r in range(20, 130, 25):
            d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(20,50,70), width=1)
        d.text((cx-110, cy+150), "CAMERA STANDBY — PRESS START", fill=(30,70,90))
        self._show(img)

    def _start(self):
        if self.running: return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return self._log("ERR", "Webcam not found", RED)
        self.running = True
        self._log("SYS", "Detection started", ACCENT)
        threading.Thread(target=self._loop, daemon=True).start()

    def _stop(self):
        self.running = False
        self.alarm.stop()
        if self.cap: self.cap.release()
        self._placeholder()
        self._draw_ring("STANDBY", DIM, 0)
        self.closed_start = None
        self._log("SYS", "Stopped", AMBER)

    def _loop(self):
        ear_avg = 0.3
        while self.running:
            ret, frame = self.cap.read()
            if not ret: break

            h, w = frame.shape[:2]
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res   = self.face_mesh.process(rgb)
            pil   = Image.fromarray(rgb).resize((FRAME_W, FRAME_H))
            draw  = ImageDraw.Draw(pil)

            sx, sy = FRAME_W/w, FRAME_H/h
            status_color = GREEN
            duration = 0.0

            if res.multi_face_landmarks:
                lm      = res.multi_face_landmarks[0].landmark
                ear_l   = get_ear(lm, L_EYE, w, h)
                ear_r   = get_ear(lm, R_EYE, w, h)
                ear_avg = (ear_l + ear_r) / 2

                for idx_set in [L_EYE, R_EYE]:
                    pts = [(int(lm[i].x*FRAME_W), int(lm[i].y*FRAME_H)) for i in idx_set]
                    ec  = (0,255,157) if ear_avg >= EAR_THRESHOLD else (255,45,85)
                    for j in range(len(pts)):
                        draw.line([pts[j], pts[(j+1)%len(pts)]], fill=ec, width=1)

                if ear_avg < EAR_THRESHOLD:
                    if self.closed_start is None:
                        self.closed_start = time.time()
                    duration     = time.time() - self.closed_start
                    status_color = RED
                    pct          = min(duration / CLOSED_TIME_LIMIT, 1.0)

                    if duration >= CLOSED_TIME_LIMIT:
                        overlay = Image.new("RGBA", (FRAME_W, FRAME_H), (255,0,40,50))
                        pil = Image.alpha_composite(pil.convert("RGBA"), overlay).convert("RGB")
                        draw = ImageDraw.Draw(pil)
                        draw.text((FRAME_W//2-140, FRAME_H//2-14),
                                  "⚠  DROWSINESS ALERT  ⚠", fill=(255,50,80))
                        self.alarm.start()
                        if self.alert_count == int(duration):
                            self.alert_count += 1
                    else:
                        self.alarm.stop()

                    self.root.after(0, lambda p=pct: self._draw_ring(
                        f"{duration:.1f}s", RED, p))
                else:
                    self.closed_start = None
                    self.alarm.stop()
                    self.root.after(0, lambda e=ear_avg: self._draw_ring(
                        "AWAKE", GREEN, min(e/0.4,1.0)))

                draw.text((10,10),  f"EAR: {ear_avg:.3f}", fill=(0,207,255))
                draw.text((10,28),  f"L: {ear_l:.3f}  R: {ear_r:.3f}", fill=(60,120,160))

            else:
                ear_avg = 0.3
                self.closed_start = None
                self.alarm.stop()
                draw.text((10,10), "NO FACE DETECTED", fill=(255,170,0))
                self.root.after(0, lambda: self._draw_ring("NO FACE", AMBER, 0))

            draw.text((FRAME_W-80, FRAME_H-18),
                      datetime.now().strftime("%H:%M:%S"), fill=(30,70,90))

            self._show(pil)
            self.root.after(0, lambda e=ear_avg, d=duration: self._update_stats(e, d))
            self.root.after(0, lambda e=ear_avg: self._draw_ear_bar(e))

    def _update_stats(self, ear, dur):
        self.ear_var.set(f"{ear:.2f}")
        self.dur_var.set(f"{dur:.1f}s")
        self.alert_var.set(str(self.alert_count))

    def _show(self, pil_img):
        imgtk = ImageTk.PhotoImage(pil_img)
        self.cam_lbl.config(image=imgtk)
        self.cam_lbl._img = imgtk

    def _log(self, tag, msg, color=TEXT):
        if self._log_lines and self._log_lines[-1][1] == msg: return
        self._log_lines.append((datetime.now().strftime("%H:%M:%S"), msg, color))
        if len(self._log_lines) > 5: self._log_lines.pop(0)
        for w in self.log_frame.winfo_children(): w.destroy()
        for ts, m, c in self._log_lines:
            row = tk.Frame(self.log_frame, bg=BG); row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=ts, font=("Consolas",7), fg=DIM, bg=BG).pack(side=tk.LEFT)
            tk.Label(row, text=f"  {m}", font=("Consolas",8), fg=c, bg=BG).pack(side=tk.LEFT)

    def _tick_clock(self):
        self.clock_lbl.config(text=datetime.now().strftime("%a %d %b  %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _quit(self):
        self.running = False
        self.alarm.stop()
        if self.cap: self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    DrowsinessApp()
