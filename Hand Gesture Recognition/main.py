import cv2
import mediapipe as mp
import numpy as np
from collections import deque, Counter
import time

mp_hands = mp.solutions.hands
gesture_history = deque(maxlen=10)

OVERLAY_BG   = (15, 15, 25)
ACCENT_GREEN = (80, 220, 100)
ACCENT_BLUE  = (100, 180, 255)
ACCENT_GOLD  = (50, 200, 220)
PURPLE       = (180, 80, 220)
DARK_GRAY    = (40, 40, 55)
WHITE        = (240, 240, 240)
GRAY         = (120, 120, 140)
FONT         = cv2.FONT_HERSHEY_SIMPLEX
FONT_BOLD    = cv2.FONT_HERSHEY_DUPLEX

THUMB_CMC  = mp_hands.HandLandmark.THUMB_CMC
THUMB_MCP  = mp_hands.HandLandmark.THUMB_MCP
THUMB_IP   = mp_hands.HandLandmark.THUMB_IP
THUMB_TIP  = mp_hands.HandLandmark.THUMB_TIP
INDEX_MCP  = mp_hands.HandLandmark.INDEX_FINGER_MCP
INDEX_PIP  = mp_hands.HandLandmark.INDEX_FINGER_PIP
INDEX_TIP  = mp_hands.HandLandmark.INDEX_FINGER_TIP
MIDDLE_MCP = mp_hands.HandLandmark.MIDDLE_FINGER_MCP
MIDDLE_PIP = mp_hands.HandLandmark.MIDDLE_FINGER_PIP
MIDDLE_TIP = mp_hands.HandLandmark.MIDDLE_FINGER_TIP
RING_MCP   = mp_hands.HandLandmark.RING_FINGER_MCP
RING_PIP   = mp_hands.HandLandmark.RING_FINGER_PIP
RING_TIP   = mp_hands.HandLandmark.RING_FINGER_TIP
PINKY_MCP  = mp_hands.HandLandmark.PINKY_MCP
PINKY_PIP  = mp_hands.HandLandmark.PINKY_PIP
PINKY_TIP  = mp_hands.HandLandmark.PINKY_TIP

GESTURES = {
    (1, 0, 0, 0, 0): ("Thumbs Up",  ACCENT_GREEN),
    (0, 0, 0, 0, 0): ("Fist",       (80, 80, 220)),
    (1, 1, 1, 1, 1): ("Open Palm",  ACCENT_GOLD),
    (0, 1, 1, 0, 0): ("Peace",      ACCENT_GREEN),
    (0, 1, 0, 0, 0): ("Point",      ACCENT_BLUE),
    (0, 0, 0, 0, 1): ("Pinky Up",   ACCENT_BLUE),
    (0, 1, 0, 0, 1): ("Rock On",    PURPLE),
    (1, 1, 0, 0, 0): ("Gun",        ACCENT_GOLD),
    (0, 1, 1, 1, 0): ("Three",      ACCENT_BLUE),
    (0, 1, 1, 1, 1): ("Four",       ACCENT_GOLD),
    (1, 1, 1, 0, 0): ("Three-Alt",  ACCENT_BLUE),
}


def lm(hand_landmarks, idx):
    p = hand_landmarks.landmark[idx]
    return np.array([p.x, p.y, p.z])

def angle_between(a, b, c):
    ba, bc = a - b, c - b
    cos_a = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cos_a, -1.0, 1.0)))

def finger_curl(hand_landmarks, mcp_id, pip_id, tip_id):
    ang = angle_between(lm(hand_landmarks, mcp_id), lm(hand_landmarks, pip_id), lm(hand_landmarks, tip_id))
    return float(np.clip((170 - ang) / 110, 0, 1))

def thumb_extended(hand_landmarks):
    tip, ip  = lm(hand_landmarks, THUMB_TIP), lm(hand_landmarks, THUMB_IP)
    mcp, cmc = lm(hand_landmarks, THUMB_MCP), lm(hand_landmarks, THUMB_CMC)
    imcp     = lm(hand_landmarks, INDEX_MCP)
    return angle_between(cmc, mcp, tip) > 150 and np.linalg.norm(tip[:2] - imcp[:2]) > np.linalg.norm(ip[:2] - imcp[:2])

def fingers_up(hand_landmarks):
    T = 0.40
    return [
        1 if thumb_extended(hand_landmarks) else 0,
        1 if finger_curl(hand_landmarks, INDEX_MCP,  INDEX_PIP,  INDEX_TIP)  < T else 0,
        1 if finger_curl(hand_landmarks, MIDDLE_MCP, MIDDLE_PIP, MIDDLE_TIP) < T else 0,
        1 if finger_curl(hand_landmarks, RING_MCP,   RING_PIP,   RING_TIP)   < T else 0,
        1 if finger_curl(hand_landmarks, PINKY_MCP,  PINKY_PIP,  PINKY_TIP)  < T else 0,
    ]

def classify_gesture(fingers):
    return GESTURES.get(tuple(fingers), ("Unknown", GRAY))

def smooth_gesture(g):
    gesture_history.append(g)
    return Counter(gesture_history).most_common(1)[0][0]

def draw_rounded_rect(img, x, y, w, h, r, color, alpha=0.75):
    overlay = img.copy()
    cv2.rectangle(overlay, (x + r, y), (x + w - r, y + h), color, -1)
    cv2.rectangle(overlay, (x, y + r), (x + w, y + h - r), color, -1)
    for cx, cy in [(x+r, y+r), (x+w-r, y+r), (x+r, y+h-r), (x+w-r, y+h-r)]:
        cv2.circle(overlay, (cx, cy), r, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def draw_finger_indicators(frame, fingers, x0, y0):
    bw, bh, gap = 28, 38, 6
    draw_rounded_rect(frame, x0 - 8, y0 - 8, 5 * bw + 4 * gap + 16, bh + 24, 6, OVERLAY_BG, 0.7)
    for i, (label, state) in enumerate(zip(["T", "I", "M", "R", "P"], fingers)):
        rx = x0 + i * (bw + gap)
        cv2.rectangle(frame, (rx, y0), (rx + bw, y0 + bh), ACCENT_GREEN if state else DARK_GRAY, -1 if state else 1)
        cv2.putText(frame, label, (rx + 7, y0 + bh - 10), FONT, 0.5, WHITE if state else GRAY, 1, cv2.LINE_AA)

def draw_ui(frame, gesture, color, fingers, fps, H, W):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, H - 100), (W, H), OVERLAY_BG, -1)
    cv2.addWeighted(overlay, 0.80, frame, 0.20, 0, frame)
    cv2.line(frame, (0, H - 100), (W, H - 100), color, 2)

    tw = cv2.getTextSize(gesture, FONT_BOLD, 1.4, 2)[0][0]
    cv2.putText(frame, gesture, ((W - tw) // 2, H - 52), FONT_BOLD, 1.4, color, 2, cv2.LINE_AA)
    draw_finger_indicators(frame, fingers, (W - (5 * 28 + 4 * 6)) // 2, H - 42)

    draw_rounded_rect(frame, W - 90, 10, 80, 32, 6, OVERLAY_BG, 0.7)
    cv2.putText(frame, f"FPS {fps:.0f}", (W - 83, 32), FONT, 0.6, ACCENT_BLUE, 1, cv2.LINE_AA)

    draw_rounded_rect(frame, 10, 10, 210, 32, 6, OVERLAY_BG, 0.7)
    cv2.putText(frame, "Gesture Recognition", (18, 32), FONT, 0.6, GRAY, 1, cv2.LINE_AA)

def draw_hand(frame, hand_landmarks, W, H):
    tip_ids = {THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP}
    for a, b in mp_hands.HAND_CONNECTIONS:
        pa, pb = hand_landmarks.landmark[a], hand_landmarks.landmark[b]
        cv2.line(frame, (int(pa.x*W), int(pa.y*H)), (int(pb.x*W), int(pb.y*H)), (60, 180, 100), 2, cv2.LINE_AA)
    for idx, lmk in enumerate(hand_landmarks.landmark):
        cx, cy, tip = int(lmk.x*W), int(lmk.y*H), idx in tip_ids
        cv2.circle(frame, (cx, cy), 8 if tip else 6, (20, 20, 30), -1)
        cv2.circle(frame, (cx, cy), 6 if tip else 4, ACCENT_GOLD if tip else WHITE, -1)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    prev_time = time.time()
    gesture, color = "-", GRAY

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75, min_tracking_confidence=0.65, model_complexity=1) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            H, W = frame.shape[:2]
            now = time.time()
            fps, prev_time = 1.0 / (now - prev_time + 1e-6), now

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_rgb.flags.writeable = False
            result = hands.process(img_rgb)
            img_rgb.flags.writeable = True

            fingers = [0, 0, 0, 0, 0]

            if result.multi_hand_landmarks:
                for hl in result.multi_hand_landmarks:
                    draw_hand(frame, hl, W, H)
                    fingers = fingers_up(hl)
                    raw, color = classify_gesture(fingers)
                    gesture = smooth_gesture(raw)
            else:
                gesture_history.clear()
                gesture, color = "-", GRAY

            draw_ui(frame, gesture, color, fingers, fps, H, W)
            cv2.imshow("Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
