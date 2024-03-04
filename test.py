from inference_sdk import InferenceHTTPClient
import cv2
from ultralytics import YOLO
import json

model = YOLO(model="runs/train9/weights/best.pt")

cap = cv2.VideoCapture(0)

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="4AJmMFnOpoK1g4wWheVG"
)

while True:
    ret, frame = cap.read()
    # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # results = model(frame)
    result = CLIENT.infer(frame, model_id="fall-detection-67grz/6")
    print(result)
    result_json = json.dumps(result)
    result = json.loads(result_json)

    if 'predictions' not in result:
        continue
    prediction = result['predictions']
    if result['predictions']:  # Check if predictions exist
        for prediction in result['predictions']:
            # prediction = result['predictions']  # Access the first prediction
            x, y, w, h = prediction['x'], prediction['y'], prediction['width'], prediction['height']
            lass_name = prediction['class']
            x1, y1 = int(x), int(y)
            x2, y2 = int(x + w), int(y + h)
            class_name = prediction['class']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow("YOLO detection", frame)
    
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()