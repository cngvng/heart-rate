import cv2
from ultralytics import YOLO

model = YOLO(model="runs/train9/weights/best.pt")

cap = cv2.VideoCapture(0)


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    results = model(frame)

    bboxes = results[0].boxes

    if bboxes is not None and len(bboxes) > 0:
        for i, box in enumerate(bboxes):
            confidence = box.conf.item()
            cls = box.cls.item()
            # Kiểm tra xem confidence có lớn hơn ngưỡng không
            print(f"Bounding Box {i + 1}: Confidence = {confidence} Class = {cls}")

            # # Lấy thông tin vị trí của bounding box và vẽ nó lên hình ảnh gốc
            # x, y, w, h = box.xywh.squeeze().tolist()  # Sử dụng .squeeze() để giảm chiều và chuyển sang danh sách
            # x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

            label = f"Confidence: {confidence:.2f} Class: {cls}"
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Hiển thị hình ảnh gốc với các bounding box có confidence rate cao
    cv2.imshow("YOLO detection", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Visualize the results on the frame
    # annotated_frame = results[0].plot()


    # # Display the annotated frame
    # cv2.imshow("YOLOv8 Inference", annotated_frame)

    