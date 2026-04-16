import cv2, math
import mediapipe as mp

pose = mp.solutions.pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def p(lm, w, h, i):
    return int(lm[i].x * w), int(lm[i].y * h)

while cap.isOpened():
    ret, f = cap.read()
    if not ret: break

    h, w = f.shape[:2]
    res = pose.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    label = "Detecting..."

    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark

        ls, rs = p(lm,w,h,11), p(lm,w,h,12)
        lh, rh = p(lm,w,h,23), p(lm,w,h,24)
        lw, rw = p(lm,w,h,15), p(lm,w,h,16)
        lk, rk = p(lm,w,h,25), p(lm,w,h,26)

        shoulder_y = (ls[1] + rs[1]) // 2
        hip_y = (lh[1] + rh[1]) // 2
        width = abs(ls[0] - rs[0])

        wrist_dist = math.hypot(lw[0]-rw[0], lw[1]-rw[1])
        namaste_th = max(40, width * 0.3)

        if wrist_dist < namaste_th and shoulder_y < lw[1] < hip_y:
            label = "Namaste"

        elif lw[1] < shoulder_y and rw[1] < shoulder_y:
            label = "Hands Up"

        elif (lw[1] < shoulder_y < rw[1]) or (rw[1] < shoulder_y < lw[1]):
            label = "Hi"

        elif lw[1] < shoulder_y or rw[1] < shoulder_y:
            label = "One Hand Up"

        elif abs(lw[1] - shoulder_y) < 40 and abs(rw[1] - shoulder_y) < 40:
            label = "T Pose"

        elif lw[1] > hip_y and rw[1] > hip_y:
            label = "Hands Down"

        elif abs(lh[1]-lk[1]) < 40 and abs(rh[1]-rk[1]) < 40:
            label = "Sitting"

        elif abs(ls[0]-lh[0]) > width * 0.4:
            label = "Leaning"

        else:
            label = "Standing"

        draw.draw_landmarks(f, res.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

    cv2.putText(f, label, (20,40), 0, 1, (0,255,255), 2)
    cv2.imshow("Pose Detection", f)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
