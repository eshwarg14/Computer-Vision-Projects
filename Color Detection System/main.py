import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import colorsys

COLOR_NAMES = {
    (255,0,0):"Red",(0,255,0):"Lime",(0,0,255):"Blue",(255,255,0):"Yellow",
    (0,255,255):"Cyan",(255,0,255):"Magenta",(255,165,0):"Orange",
    (128,0,128):"Purple",(255,192,203):"Pink",(165,42,42):"Brown",
    (0,0,0):"Black",(255,255,255):"White",(128,128,128):"Gray",
    (0,128,0):"Green",(0,0,128):"Navy",(128,128,0):"Olive",
    (0,128,128):"Teal",(255,99,71):"Tomato",(255,215,0):"Gold",
    (75,0,130):"Indigo",(238,130,238):"Violet",(64,224,208):"Turquoise",
    (250,128,114):"Salmon",(240,230,140):"Khaki",(255,127,80):"Coral",
}

def closest_color(bgr):
    r,g,b = int(bgr[2]),int(bgr[1]),int(bgr[0])
    min_d, name = float("inf"), "Unknown"
    for (cr,cg,cb), n in COLOR_NAMES.items():
        d = (r-cr)**2+(g-cg)**2+(b-cb)**2
        if d < min_d: min_d,name = d,n
    return name

def bgr_to_info(bgr):
    r,g,b = int(bgr[2]),int(bgr[1]),int(bgr[0])
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    return {
        "name": closest_color(bgr),
        "hex":  f"#{r:02X}{g:02X}{b:02X}",
        "rgb":  f"rgb({r}, {g}, {b})",
        "hsv":  f"hsv({h*360:.0f}°, {s*100:.0f}%, {v*100:.0f}%)",
        "bgr_raw": (r,g,b),
    }

class ColorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Colour Detection System")
        self.configure(bg="#0d0d0f")
        self.resizable(True, True)

        self.cam = None
        self.running = False
        self.frame_cv = None
        self._build_ui()

    def _build_ui(self):
        left = tk.Frame(self, bg="#0d0d0f")
        left.pack(side="left", padx=16, pady=16)

        self.canvas = tk.Canvas(left, width=640, height=480,
                                bg="#1a1a1d", highlightthickness=2,
                                highlightbackground="#2e2e35")
        self.canvas.pack()
        self.canvas.bind("<Motion>",       self._on_mouse)
        self.canvas.bind("<Button-1>",     self._on_click)

        btn_row = tk.Frame(left, bg="#0d0d0f")
        btn_row.pack(pady=(10,0), fill="x")
        self._btn(btn_row, "📷  Webcam",   self._toggle_cam).pack(side="left", expand=True, padx=4)
        self._btn(btn_row, "🖼  Image",    self._open_image).pack(side="left", expand=True, padx=4)
        self._btn(btn_row, "⏹  Stop",     self._stop).pack(side="left", expand=True, padx=4)

        right = tk.Frame(self, bg="#0d0d0f", width=260)
        right.pack(side="right", fill="y", padx=(0,16), pady=16)
        right.pack_propagate(False)

        tk.Label(right, text="COLOUR ANALYSIS", font=("Courier",13,"bold"),
                 bg="#0d0d0f", fg="#7c7cff").pack(anchor="w", pady=(0,12))

        self.swatch = tk.Label(right, width=30, height=5, bg="#1a1a1d",
                               relief="flat")
        self.swatch.pack(fill="x", pady=(0,12))

        self.info_vars = {}
        for key in ("Name","HEX","RGB","HSV"):
            row = tk.Frame(right, bg="#0d0d0f")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{key:<5}", font=("Courier",10),
                     bg="#0d0d0f", fg="#555566", width=5, anchor="w").pack(side="left")
            var = tk.StringVar(value="—")
            self.info_vars[key] = var
            tk.Label(row, textvariable=var, font=("Courier",11,"bold"),
                     bg="#0d0d0f", fg="#e8e8ff", anchor="w").pack(side="left", padx=6)

        tk.Frame(right, bg="#2e2e35", height=1).pack(fill="x", pady=14)

        tk.Label(right, text="SAMPLED PALETTE", font=("Courier",11,"bold"),
                 bg="#0d0d0f", fg="#7c7cff").pack(anchor="w", pady=(0,8))
        self.palette_frame = tk.Frame(right, bg="#0d0d0f")
        self.palette_frame.pack(fill="x")
        self.palette_swatches = []

        self.status_var = tk.StringVar(value="Ready — hover or click on the image")
        tk.Label(right, textvariable=self.status_var, font=("Courier",9),
                 bg="#0d0d0f", fg="#444455", wraplength=240, justify="left"
                 ).pack(side="bottom", anchor="w")

    def _btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         font=("Courier",10,"bold"), bg="#1e1e28", fg="#c8c8ff",
                         activebackground="#2e2e48", activeforeground="#ffffff",
                         relief="flat", padx=12, pady=7, cursor="hand2",
                         bd=0, highlightthickness=0)

    def _toggle_cam(self):
        if self.running:
            self._stop()
            return
        self.cam = cv2.VideoCapture(0)
        if not self.cam.isOpened():
            self.status_var.set("❌ No webcam found.")
            return
        self.running = True
        self.status_var.set("📷 Webcam active — hover to detect")
        self._cam_loop()

    def _cam_loop(self):
        if not self.running: return
        ret, frame = self.cam.read()
        if ret:
            self.frame_cv = frame
            self._show_frame(frame)
        self.after(30, self._cam_loop)

    def _open_image(self):
        self._stop()
        path = filedialog.askopenfilename(
            filetypes=[("Images","*.png *.jpg *.jpeg *.bmp *.webp")])
        if not path: return
        self.frame_cv = cv2.imread(path)
        self._show_frame(self.frame_cv)
        self.status_var.set("🖼 Image loaded — hover / click to detect")

    def _stop(self):
        self.running = False
        if self.cam:
            self.cam.release()
            self.cam = None

    def _show_frame(self, frame):
        h, w = frame.shape[:2]
        scale = min(640/w, 480/h)
        nw, nh = int(w*scale), int(h*scale)
        resized = cv2.resize(frame, (nw, nh))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb))
        self.canvas.config(width=nw, height=nh)
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas._img = img
        self._frame_display = resized

    def _pixel_at(self, x, y):
        try:
            bgr = self._frame_display[y, x]
            return bgr
        except (AttributeError, IndexError):
            return None

    def _on_mouse(self, e):
        bgr = self._pixel_at(e.x, e.y)
        if bgr is None: return
        info = bgr_to_info(bgr)
        self._update_info(info, live=True)

    def _on_click(self, e):
        bgr = self._pixel_at(e.x, e.y)
        if bgr is None: return
        info = bgr_to_info(bgr)
        self._update_info(info, live=False)
        self._add_palette(info["hex"])

    def _update_info(self, info, live=False):
        self.swatch.config(bg=info["hex"])
        self.info_vars["Name"].set(info["name"])
        self.info_vars["HEX"].set(info["hex"])
        self.info_vars["RGB"].set(info["rgb"])
        self.info_vars["HSV"].set(info["hsv"])
        if not live:
            self.status_var.set(f"✔ Saved: {info['name']} {info['hex']}")

    def _add_palette(self, hex_color):
        if len(self.palette_swatches) >= 10:
            self.palette_swatches[0].destroy()
            self.palette_swatches.pop(0)
        sw = tk.Label(self.palette_frame, bg=hex_color, width=3, height=2,
                      text="", relief="flat", cursor="hand2")
        sw.pack(side="left", padx=2, pady=2)
        sw.bind("<Button-1>", lambda e, h=hex_color: self.clipboard_append(h))
        sw.bind("<Enter>",    lambda e, h=hex_color: self.status_var.set(f"Click to copy {h}"))
        self.palette_swatches.append(sw)

if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
