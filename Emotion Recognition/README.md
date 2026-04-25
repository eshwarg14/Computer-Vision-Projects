# 😊 Real-Time Emotion Recognition System

A real-time emotion detection system using computer vision and AI. This application analyzes facial expressions through webcam and identifies emotions like **Happy, Sad, Angry, Surprise**, etc., with live visualization.

---

## Preview

![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/412ffdda766661210c2e13f4d2216f4a4edce682/Images/ER.png)

---

## ✨ Features

- 😊 Real-time emotion detection via webcam  
- 🤖 AI-powered emotion analysis (DeepFace)  
- 🎨 Live emotion score visualization (bars)  
- 🧠 Detects multiple emotions:
  - Happy 😊  
  - Sad 😢  
  - Angry 😠  
  - Surprise 😲  
  - Fear 😨  
  - Disgust 🤢  
  - Neutral 😐  
- 🖥️ Interactive GUI with Tkinter  
- ⏸️ Pause/Resume functionality  

---

## 🧠 What is Emotion Recognition?

Emotion recognition is a computer vision technique used to detect **human emotions from facial expressions**.

👉 It analyzes:
- Facial landmarks  
- Expressions  
- Muscle movements  

---

## 🤖 What is DeepFace?

**DeepFace** is a deep learning-based facial analysis library.

- 🧠 Detects emotions from faces  
- 🎯 High accuracy  
- ⚡ Works in real-time  
- 🤖 Uses pre-trained neural networks  

---

## 🧠 Technologies Used

```
opencv-python
mediapipe (optional fallback logic)
deepface
tkinter
pillow
```

📦 Install dependencies:

```bash
pip install opencv-python deepface pillow
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🛠️ How It Works

- 📷 Webcam captures live video  
- 🤖 DeepFace analyzes face and emotions  
- 📊 Returns emotion probabilities  
- 🎯 Dominant emotion is selected  
- 🎨 UI updates:
  - Emoji  
  - Emotion label  
  - Score bars  
- 🖥️ Display results in real-time  

---

## 🔄 Fallback System

If **DeepFace is not installed**, the app uses a **simulated emotion system**:

- Generates pseudo emotion values  
- Ensures app still runs  
- Useful for testing/demo  

---

## 📁 Project Structure

```
├── main.py        # Main emotion detection app
├── Images/        # Demo screenshots
└── README.md
```

---

## ⚠️ Requirements

- 📷 Webcam (mandatory)  
- 🐍 Python 3.8+  
- 💡 Good lighting for accurate detection  

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

---

## 🚀 Future Improvements

- Multi-face emotion detection 👥
