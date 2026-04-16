# 🧍‍♂️ Real-Time Human Pose Detection & Gesture Recognition

A real-time pose detection system built using MediaPipe and OpenCV. This project detects human body postures and classifies gestures like **Namaste, Hands Up, T-Pose, Sitting, Standing**, and more using webcam input.

---

## Preview

![Demo](Images/pose1.png)
![Demo](Images/pose2.png)

---

## ✨ Features

- 🧍‍♂️ Real-time human pose detection  
- 🤖 Gesture classification using body landmarks  
- 📷 Webcam-based tracking  
- ⚡ Fast and lightweight  
- 🎯 Multiple posture detection:
  - Namaste 🙏  
  - Hands Up 🙌  
  - One Hand Up ✋  
  - Hi 👋  
  - T-Pose 🧍  
  - Hands Down  
  - Sitting 🪑  
  - Leaning  
  - Standing  

---

## 🧠 What is Pose Detection?

Pose detection is a computer vision technique used to detect **human body key points (landmarks)** like:

- Head  
- Shoulders  
- Elbows  
- Wrists  
- Hips  
- Knees  

👉 These points help understand **body posture and movement**

---

## 🤖 What is MediaPipe Pose?

MediaPipe Pose is a machine learning model that:
- Detects **33 body landmarks**  
- Works in real-time  
- Provides accurate tracking  
- Runs efficiently on CPU  

---

## 🧠 Technologies Used

```
opencv-python
mediapipe
math
```

📦 Install dependencies:

```bash
pip install opencv-python mediapipe
```

---

## ▶️ How to Run

```bash
python main.py
```

Press `Q` to exit.

---

## 🛠️ How It Works

- 📷 Capture webcam frame  
- 🤖 MediaPipe detects body landmarks  
- 📍 Extract key points (shoulders, wrists, hips, knees)  
- 📏 Calculate positions and distances  
- 🧠 Apply rule-based logic to classify pose  
- 🖥️ Display detected gesture on screen  

---

## 🧠 Gesture Logic (Simplified)

- 🙏 **Namaste** → Hands close together in front  
- 🙌 **Hands Up** → Both hands above shoulders  
- 👋 **Hi** → One hand up, one down  
- ✋ **One Hand Up** → Only one hand raised  
- 🧍 **T-Pose** → Hands stretched sideways  
- ⬇️ **Hands Down** → Both hands below hips  
- 🪑 **Sitting** → Knees aligned with hips  
- ↔️ **Leaning** → Body tilted sideways  
- 🧍‍♂️ **Standing** → Default posture  

---

## 📁 Project Structure

```
├── main.py        # Main pose detection script
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

- Gesture-based controls 🎮  
- Fitness posture tracking 🏋️  
- Yoga pose detection 🧘  
- Multi-person detection 👥  
