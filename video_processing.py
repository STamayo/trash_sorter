from ultralytics import YOLO
import cv2
import math

def start_video(t):

    print('Initializing video...')

    # start webcam
    cap = cv2.VideoCapture(2)
    cap.set(3, 640)
    cap.set(4, 480)

    # model
    model = YOLO("./datasets/dataset3best.pt", verbose=False)

    # object classes
    classNames = ["compost", "trash", "recycle"]
    colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    remap = [2, 1, 0]

    while True:

        success, img = cap.read()
        results = model(img, stream=True, verbose=False, conf = 0.7)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:

                # class name
                cls = int(box.cls[0])
                cls = remap[cls]
                t.set_type(cls)

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
                thickness = 2
               # print(confidence)
                cv2.putText(img, f'{classNames[cls]} ({confidence})', org, font, fontScale, colors[cls], thickness)
        
            if len(boxes) == 0:
                t.set_type(-1)
        
        cv2.imwrite('./images/current.jpg', img)
        #cv2.imshow('Webcam', img)
        
        if cv2.waitKey(1) == ord('q'):
            print('destryong video')
            break

    cap.release()
    cv2.destroyAllWindows()

class TrashType:

    cur_type = None
    old_type = None

    def set_type(self, inp):
        self.cur_type = inp
    
    def get_type(self) -> int:
        if self.cur_type is not None:
            return self.cur_type
        else: 
            return -1