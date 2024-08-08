from YOLOv8 import YOLO
import cv2
import math 


cap = cv2.VideoCapture(0)


model = YOLO(r"D:\Mahesh\Coding files\traffic-light-detection\yolo\best weights\v9 - 64 epochs.pt")

# object classes
classNames = ["green", "red", "yellow"]

def Distance_finder(Focal_Length, real_face_width, obj_width_in_frame):
    distance = (real_face_width * Focal_Length)/obj_width_in_frame
    return distance


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            obj_width = x2 - x1
            dist = Distance_finder(650, 7.1, obj_width)

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)
            cls = int(box.cls[0])
            # print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img,  str(confidence), org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()