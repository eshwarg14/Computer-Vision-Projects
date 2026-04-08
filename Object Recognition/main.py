import cv2
import numpy as np

net = cv2.dnn.readNetFromDarknet(
    r"E:\Yolo\yolov3.cfg",
    r"E:\Yolo\yolov3.weights"
)

with open(r"\Yolo\coco.names") as f:
    class_names = f.read().strip().split("\n")

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

cap = cv2.VideoCapture(0)
cap.set(3, 480)   
cap.set(4, 360)

frame_skip = 3    
frame_id = 0
detections = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    if frame_id % frame_skip == 0:
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (256, 256), swapRB=True, crop=False
        )

        net.setInput(blob)
        outputs = net.forward(output_layers)

        boxes, confidences, class_ids = [], [], []

        for output in outputs:
            for det in output:
                scores = det[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]

                if conf > 0.5:
                    cx, cy, bw, bh = det[0:4] * np.array([w, h, w, h])
                    x = int(cx - bw / 2)
                    y = int(cy - bh / 2)

                    boxes.append([x, y, int(bw), int(bh)])
                    confidences.append(float(conf))
                    class_ids.append(class_id)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        detections = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                detections.append((boxes[i], class_ids[i], confidences[i]))

    for (box, cid, conf) in detections:
        x, y, bw, bh = box
        label = f"{class_names[cid]} {conf*100:.0f}%"

        cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Object Recognition Using YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
