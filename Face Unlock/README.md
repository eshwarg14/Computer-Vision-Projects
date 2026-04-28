# 🔓 AI Face Unlock System

A real-time face recognition-based authentication system built using Python, OpenCV, and the face_recognition library. This application detects faces through webcam and grants access only to **authorized users**.

---

## Preview

![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/32e632bf59834a59c506740ec33246e6524c0048/Images/FCC.png)
![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/32e632bf59834a59c506740ec33246e6524c0048/Images/FU.png)

---

## ✨ Features

- 🔓 Face-based authentication system  
- 🤖 Real-time face recognition  
- 📷 Webcam-based detection  
- 👥 Multiple authorized users support  
- 📊 Live face detection count  
- 🔐 Unlock / Lock system  
- 🖥️ Advanced GUI with Tkinter  
- 📜 Event logging system  
- 💡 Visual feedback (color-coded boxes)  

---

## 🧠 What is Face Recognition?

Face recognition is a computer vision technique used to:

- Detect human faces  
- Extract facial features  
- Compare with stored faces  
- Identify or verify identity  

---

## 🤖 How face_recognition Works

The **face_recognition** library:

- 🧠 Uses deep learning (dlib-based model)  
- 🔢 Converts faces into numerical encodings  
- 📏 Compares encodings using distance  
- 🎯 Matches if distance < threshold  

---

## 🔐 Authentication Logic

- Known faces → Stored in folder  
- Webcam face → Converted to encoding  
- Compare both:
  - ✅ Match → Unlock  
  - ❌ No match → Locked  

---

## 🧠 Technologies Used

```
opencv-python
face_recognition
tkinter
pillow
numpy
```

📦 Install dependencies:

```bash
pip install opencv-python face_recognition pillow numpy
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py                         # Main application
├── Model & Utilities/
│   └── Testing Images/
│       └── Data/                  # Authorized faces folder
│           ├── user1.jpg
│           ├── user2.png
│           └── ...
└── README.md
```

---

## 📂 Authorized Faces Setup

- 📁 Add images of authorized users inside:

```
Model & Utilities/Testing Images/Data/
```

- 📌 Image filename = User name  
  Example:
  ```
  john.jpg → John
  ```

---

## ⚙️ Important Configuration

Update path in code:

```python
AUTHORIZED_FOLDER = "Model & Utilities/Testing Images/Data"
```

---

## 🛠️ How It Works

1️⃣ Load authorized images  
2️⃣ Convert faces → encodings  
3️⃣ Start webcam  
4️⃣ Detect faces in frame  
5️⃣ Compare with stored encodings  
6️⃣ If match:
   - 🔓 Unlock system  
7️⃣ Else:
   - 🔒 Remain locked  

---

## 📊 System States

- 🟡 SCANNING → Searching for faces  
- 🔴 LOCKED → Unknown face  
- 🟢 UNLOCKED → Authorized face detected  

---

## 📜 Event Logging

- Tracks:
  - Unlock events  
  - System status  
  - Errors  

---

## ⚠️ Requirements

- 📷 Webcam (mandatory)  
- 🐍 Python 3.8+  
- 💡 Good lighting improves accuracy  

---

## 🔧 Important Fix

Your current path is:

```
E:\JrBotics\...
```

👉 Replace with:

```python
AUTHORIZED_FOLDER = "Model & Utilities/Testing Images/Data"
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
