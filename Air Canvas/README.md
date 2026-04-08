# 🖐️ AirCanvas - Hand Gesture Drawing App

Real-time virtual drawing application using MediaPipe and OpenCV. Draw on screen using hand gestures with smooth tracking, adjustable brush, and an interactive UI.

---

## Preview

![Demo](Images/AC.png)

---

## ✨ Features

- ✍️ Draw using index finger (gesture-based)  
- 🎨 Multiple colors (Red, Green, Blue, Cyan, Magenta, White)  
- 🧽 Eraser mode (button + pinch gesture)  
- 📏 Adjustable brush thickness  
- 🌫️ Adjustable opacity  
- 🧹 Clear canvas functionality  
- 💾 Save drawings as image  
- 🖥️ Real-time webcam feed with overlay  

---

## 🧠 Technologies Used

```
opencv-python
mediapipe
numpy
pillow
tkinter
```

📦 Install dependencies:

```bash
pip install opencv-python mediapipe numpy pillow
```

---

## ▶️ Usage

```bash
python main.py
```

---

## ✋ Controls & Gestures

| Gesture | Action |
|--------|--------|
| ☝️ Index finger up | Draw |
| 🤏 Pinch (thumb + index) | Toggle eraser |
| ✋ No hand detected | Stop drawing |

---

## 🎛️ UI Controls

- 🎨 Color buttons → Change drawing color  
- 🧽 Eraser → Toggle eraser  
- 🧹 Clear → Reset canvas  
- 💾 Save → Save drawing as PNG  
- 📏 Brush slider → Adjust thickness  
- 🌫️ Opacity slider → Adjust transparency  

---

## 🛠️ How It Works

- 🤖 **Hand Tracking** – MediaPipe detects hand landmarks in real time  
- ✏️ **Drawing Logic** – Index finger tip is tracked and smoothed  
- 🤏 **Gesture Detection** – Pinch gesture toggles eraser mode  
- 🧩 **Canvas Rendering** – OpenCV draws on a virtual canvas  
- 🖥️ **Overlay** – Canvas is blended with live webcam feed  

---

## 📁 Project Structure

```
├── main.py        # Main application logic
├── Images/        # Demo images
└── README.md
```

---

## ⚠️ Requirements

- 📷 Webcam (mandatory)  
- 🐍 Python 3.8+  
- 💡 Good lighting for accurate detection  

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

---

## ⭐ Support

If you like this project:

- ⭐ Star the repo  
- 🍴 Fork it  
- 🛠️ Contribute  
