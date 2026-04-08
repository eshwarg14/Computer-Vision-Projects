import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

COLORS = [(0,0,220),(30,180,30),(220,60,0),(0,200,200),(200,0,200),(255,255,255)]
COLOR_NAMES = ['Red','Green','Blue','Cyan','Magenta','White']
HEX_COLORS = ['#dd0000','#1eb41e','#dc3c00','#00c8c8','#c800c8','#cccccc']

state = {
    'color': 0,
    'thickness': 6,
    'prev': None,
    'smooth': None,
    'canvas': None,
    'shape': None,
    'eraser': False,
    'alpha': 0.85,
    'pinch': False
}

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

root = tk.Tk()
root.title("AirCanvas")
root.configure(bg='#0f0f1a')

video_label = tk.Label(root, bg='#0f0f1a')
video_label.grid(row=0, column=0, columnspan=9, pady=8)

ctrl = tk.Frame(root, bg='#0f0f1a')
ctrl.grid(row=1, column=0, columnspan=9)

def set_color(i):
    state['color'] = i
    state['prev'] = None
    state['eraser'] = False
    eraser_btn.config(relief=tk.RAISED, bg='#333')

def clear_canvas():
    if state['canvas'] is not None:
        state['canvas'][:] = 0
    state['prev'] = None

def save_canvas():
    f = filedialog.asksaveasfilename(defaultextension='.png')
    if f:
        cv2.imwrite(f, state['canvas'])
        messagebox.showinfo('Saved', f)

def toggle_eraser():
    state['eraser'] = not state['eraser']
    state['prev'] = None
    eraser_btn.config(
        relief=tk.SUNKEN if state['eraser'] else tk.RAISED,
        bg='#e67e22' if state['eraser'] else '#333'
    )

for i, (name, color) in enumerate(zip(COLOR_NAMES, HEX_COLORS)):
    tk.Button(
        ctrl, text=name, bg=color,
        fg='white' if name != 'White' else '#222',
        command=lambda i=i: set_color(i)
    ).grid(row=0, column=i, padx=2)

eraser_btn = tk.Button(ctrl, text='Eraser', bg='#333', fg='white', command=toggle_eraser)
eraser_btn.grid(row=0, column=len(COLORS))

tk.Button(ctrl, text='Clear', bg='#c0392b', fg='white', command=clear_canvas)\
    .grid(row=0, column=len(COLORS)+1)

tk.Button(ctrl, text='Save', bg='#27ae60', fg='white', command=save_canvas)\
    .grid(row=0, column=len(COLORS)+2)

def update_state(key, value):
    state[key] = int(float(value)) if key == 'thickness' else float(value)

for i, (label, key, lo, hi, default) in enumerate([
    ('Brush', 'thickness', 1, 40, 6),
    ('Opacity', 'alpha', 0.3, 1, 0.85)
]):
    tk.Label(root, text=label, bg='#0f0f1a', fg='#aaa').grid(row=2, column=i*2)
    slider = ttk.Scale(root, from_=lo, to=hi, orient='horizontal',
                       command=lambda v, k=key: update_state(k, v))
    slider.set(default)
    slider.grid(row=2, column=i*2+1, sticky='we')

status_var = tk.StringVar()
tk.Label(root, textvariable=status_var, bg='#0f0f1a', fg='#00e5ff')\
    .grid(row=3, column=0, columnspan=9)

def only_index_up(lm, h):
    return (
        lm[8].y*h < lm[6].y*h and
        lm[12].y*h > lm[10].y*h and
        lm[16].y*h > lm[14].y*h and
        lm[20].y*h > lm[18].y*h
    )

def is_pinch(lm, h, w):
    ix, iy = lm[8].x*w, lm[8].y*h
    tx, ty = lm[4].x*w, lm[4].y*h
    return np.hypot(ix - tx, iy - ty) < 40

def update_frame():
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    if state['canvas'] is None:
        state['canvas'] = np.zeros(frame.shape, dtype=np.uint8)

    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark

        x, y = int(lm[8].x*w), int(lm[8].y*h)

        if state['smooth'] is None:
            state['smooth'] = (x, y)

        sx = int(state['smooth'][0]*0.55 + x*0.45)
        sy = int(state['smooth'][1]*0.55 + y*0.45)
        state['smooth'] = (sx, sy)

        pinch = is_pinch(lm, h, w)
        draw = only_index_up(lm, h) and not pinch

        if pinch and not state['pinch']:
            toggle_eraser()
        state['pinch'] = pinch

        if draw:
            color = (0,0,0) if state['eraser'] else COLORS[state['color']]
            thickness = state['thickness'] * (4 if state['eraser'] else 1)

            if state['prev'] is not None:
                cv2.line(state['canvas'], state['prev'], (sx, sy), color, thickness)

            state['prev'] = (sx, sy)
            label = 'ERASING' if state['eraser'] else 'DRAWING'
        else:
            state['prev'] = None
            label = 'PINCH' if pinch else 'PEN UP'

        cv2.circle(frame, (sx, sy), state['thickness']//2 + 5, (0,255,0), -1)

        mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, label, (10, h-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        mode = 'ERASER' if state['eraser'] else COLOR_NAMES[state['color']]
        status_var.set(f"{mode} | {label} | {state['thickness']}px")

    else:
        state['prev'] = None
        state['smooth'] = None
        state['pinch'] = False
        status_var.set('No hand')

    combined = cv2.addWeighted(frame, 1, state['canvas'], state['alpha'], 0)

    img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)))
    video_label.imgtk = img
    video_label.configure(image=img)
    
    root.after(10, update_frame)

update_frame()
root.mainloop()
cap.release()
cv2.destroyAllWindows()
