from ultralytics import YOLO
import cv2
import math

type = -1
old_type = -1

def get_type() -> int:
    if type != old_type:
        old_type = type
        return type
        
    return -1

def start_video():

    print('Initializing video...')

    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # model
    model = YOLO("./datasets/dataset1best.pt", verbose=False)

    # object classes
    classNames = ["compost", "trash", "recycle"]
    colors = [(0, 255, 0), (255, 0, 0), (255, 0, 0)]
    while True:
        type = -1
        success, img = cap.read()
        results = model(img, stream=True, verbose=False)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:

                # class name
                cls = int(box.cls[0])
                global type
                type = cls

                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), colors[cls], 3)

                # confidence
                confidence = math.ceil((box.conf[0]*100))/100
                #print("Confidence --->",confidence)
                #print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_DUPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, f'{classNames[cls]} ({confidence})', org, font, fontScale, colors[cls], thickness)
        
        cv2.imwrite('./images/current.jpg', img)
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()