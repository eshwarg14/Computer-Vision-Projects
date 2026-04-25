# 😴 AI Drowsiness Detection System

A real-time drowsiness detection system that monitors eye closure using computer vision. Built with OpenCV and MediaPipe, this application alerts users when they appear drowsy using an alarm system.

---

## Preview

![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/fcdec69941e6111062813d8da6c4643379e18794/Images/DD.png)

---

## ✨ Features

- 😴 Detects drowsiness in real-time  
- 👁️ Eye tracking using facial landmarks  
- 📊 Eye Aspect Ratio (EAR) calculation  
- ⏱️ Detects prolonged eye closure  
- 🔔 Alarm alert system  
- 📈 Live EAR graph visualization  
- 🖥️ Advanced GUI with Tkinter  
- ⏯️ Start / Stop functionality  

---

## 🧠 What is Drowsiness Detection?

Drowsiness detection is a computer vision technique used to identify when a person is **falling asleep or losing attention**, especially useful in:

- 🚗 Driver safety systems  
- 🧑‍💻 Work monitoring  
- 🏥 Health applications  

---

## 🧠 What is EAR (Eye Aspect Ratio)?

**EAR (Eye Aspect Ratio)** is used to measure eye openness.

👉 Formula:

- Measures vertical eye distance  
- Divides by horizontal eye width  

### 📌 Key Idea:
- 👁️ Open eye → EAR is high  
- 😴 Closed eye → EAR drops  

---

## ⚙️ Threshold Logic

- EAR < **0.22** → Eyes considered closed  
- Eyes closed for > **1.5 seconds** → Drowsiness detected  

---

## 🧠 Technologies Used

```
opencv-python
mediapipe
pillow
tkinter
math
threading
winsound (Windows only)
```

📦 Install dependencies:

```bash
pip install opencv-python mediapipe pillow
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🛠️ How It Works

- 📷 Webcam captures live video  
- 🤖 MediaPipe detects facial landmarks  
- 👁️ Eye landmarks extracted  
- 📏 EAR is calculated  
- ⏱️ Tracks duration of eye closure  
- 🚨 If threshold exceeded:
  - Alarm starts  
  - Warning displayed  
- 📊 GUI updates stats and graph  

---

## 📁 Project Structure

```
├── main.py        # Main detection script
└── README.md
```

---

## ⚠️ Requirements

- 📷 Webcam (mandatory)  
- 🐍 Python 3.8+  
- 💡 Good lighting for accurate detection  
- 🪟 Windows OS (for alarm sound using winsound)  

---

## 🔔 Important Note

- Alarm uses `winsound` → works only on Windows  
- For Linux/Mac, replace with:
```python
import os
os.system("say Alert")
```

---

## 👨‍💻 Authors

**Eshwar G & Shivani R**

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project:

- ⭐ Star the repo  
- 🍴 Fork it  
- 🛠️ Contribute  
