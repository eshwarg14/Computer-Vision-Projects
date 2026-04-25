# 🎨 AI Colour Detection System

A real-time color detection and analysis system using Computer Vision. This application detects colors from images or webcam feed and provides detailed information including **color name, HEX, RGB, and HSV values**.

---

## Preview

![Demo](https://github.com/eshwarg14/Computer-Vision-Projects/raw/84c6fd198faea564c01bd88a5c65789ec7ee41c3/Images/CD.png)

---

## ✨ Features

- 🎨 Detect colors in real-time (webcam + images)  
- 📷 Hover or click to analyze any pixel  
- 🧠 Smart color name detection  
- 🔢 Displays:
  - HEX code  
  - RGB values  
  - HSV values  
- 🎯 Color palette history (last 10 colors)  
- 📋 Click to copy color HEX  
- 🖥️ Modern GUI using Tkinter  

---

## 🧠 What is Color Detection?

Color detection is a computer vision technique used to:

- Identify pixel color values  
- Convert between color formats  
- Classify colors into human-readable names  

---

## 🎨 Color Formats Explained

### 🔴 RGB (Red, Green, Blue)
- Range: 0–255  
- Used in digital displays  

👉 Example:
```
rgb(255, 0, 0) → Red
```

---

### 🎯 HEX Code
- Used in web design  
- Format: `#RRGGBB`

👉 Example:
```
#FF0000 → Red
```

---

### 🌈 HSV (Hue, Saturation, Value)
- More intuitive color representation  
- Used in image processing  

👉 Example:
```
hsv(0°, 100%, 100%) → Red
```

---

## 🤖 How It Works

- 📷 Capture image/frame using OpenCV  
- 📍 Get pixel color at mouse position  
- 🔄 Convert BGR → RGB → HSV  
- 🧠 Match closest color name  
- 🖥️ Display results in GUI  

---

## 🧠 Technologies Used

```
opencv-python
numpy
tkinter
pillow
colorsys
```

📦 Install dependencies:

```bash
pip install opencv-python numpy pillow
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 📁 Project Structure

```
├── main.py        # Main application
└── README.md
```

---

## 🛠️ Functionalities

### 📷 Webcam Mode
- Detect colors in real-time  
- Move cursor to analyze  

---

### 🖼 Image Mode
- Load image from system  
- Click to detect color  

---

### 🎨 Palette System
- Stores last 10 selected colors  
- Click to copy HEX code  

---

## ⚠️ Requirements

- 📷 Webcam (optional)  
- 🐍 Python 3.8+  
- 💡 Good lighting improves accuracy  

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

- Color detection using object segmentation 🎯  
- Export palette as file 📁  
- Web-based version 🌐  
- Advanced color clustering (K-Means) 🤖  
