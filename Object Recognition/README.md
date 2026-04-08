# 🎯 Real-Time Object Detection using YOLO

A real-time object detection system built using OpenCV and YOLO (You Only Look Once). Detects multiple objects from webcam feed with optimized performance for CPU.

---

## 📸 Demo / Preview

![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/d5bed6bafe3fa81272e4cf5631031e06cca1b92b/Images/OBR.png)

---

## ✨ Features

- 🎯 Real-time object detection via webcam  
- ⚡ Optimized for CPU (frame skipping)  
- 🧠 Uses YOLOv3 deep learning model  
- 📦 Detects multiple objects (COCO dataset)  
- 🖥️ Bounding boxes with labels & confidence  
- 🚀 Lightweight alternative support (YOLOv3 Lite)  

---

## 🧠 What is YOLO?

**YOLO (You Only Look Once)** is a popular real-time object detection algorithm.

- 👀 It looks at the entire image **only once**  
- ⚡ Faster than traditional detection methods  
- 🎯 Detects multiple objects in a single frame  
- 🧠 Uses deep learning (CNN)

👉 Example: It can detect **person, car, phone, bottle, etc.** in real time

---

## 📦 What is coco.names?

`coco.names` is a file that contains the **list of object class names** that YOLO can detect.

- 📋 It includes labels like:  
  `person, car, dog, bottle, chair, phone, etc.`  
- 🧠 YOLO predicts a **class ID (number)**  
- 📖 `coco.names` converts that number into a **readable label**

👉 Example:  
If YOLO predicts `class_id = 0` → `person`

---

## 🧠 Technologies Used

```
opencv-python
numpy
```

📦 Install dependencies:

```bash
pip install opencv-python numpy
```

---

## ▶️ Usage

```bash
python main.py
```

Press `Q` to exit.

---

## 📁 Project Structure

```
├── main.py          # Main detection script
├── YOLO/            # Model files
│   ├── yolov3.cfg
│   ├── yolov3.weights
│   ├── coco.names
│   ├── yolov3-lite.cfg      # (optional lightweight model)
│   └── yolov3-lite.weights  # (optional lightweight model)
└── README.md
```

---

## ⚠️ Important Notes

- 📷 Webcam required  
- 🐍 Python 3.8+  
- 💻 Works on CPU (no GPU needed)  

---

## 🚀 YOLOv3 vs YOLOv3 Lite

### 🔵 YOLOv3
- High accuracy 🎯  
- Heavy model 🧱  
- Slower on low-end systems  

### 🟢 YOLOv3 Lite
- Faster ⚡  
- Lightweight 💡  
- Slightly lower accuracy  

👉 If YOLOv3 is slow or not working properly, switch to **YOLOv3 Lite** from the `YOLO/` folder.

---

## 🛠️ How It Works

- 📷 Capture webcam frame  
- 🧠 Convert frame to blob  
- 🤖 Pass through YOLO network  
- 📦 Get bounding boxes + confidence  
- 🚫 Apply Non-Max Suppression (NMS)  
- 🖥️ Display results on screen  

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
