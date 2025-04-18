from ultralytics import YOLO
import cv2
import numpy as np


def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results

def predict_and_detect(chosen_model, img, classes=[], conf=0.2, rectangle_thickness=2, text_thickness=1):
    results = predict(chosen_model, img, classes, conf=conf)
    boxes = []
    for result in results:
        for box in result.boxes:
            boxes.append(box.xyxy)
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    return img, results, boxes

def transform_point(H, point):
    """Apply homography transformation to a single point."""
    x, y = point
    transformed = np.dot(H, np.array([x, y, 1]))
    transformed /= transformed[2]  # Normalize by w
    # return transformed[:2]  # Return (x, y) as a tuple
    return (int(transformed[0]),int(transformed[1]))  # Return (x, y) as a tuple

model = YOLO("yolo11n.pt")
H = np.load(f'data/football/homography_matrix.npy')
H = np.linalg.inv(H)
image_field = cv2.imread("data/football/field.jpg")

# Run inference with the YOLO11n model on the 'bus.jpg' image
video_pth = "/home/mohammd/Documents/hawkeye/data/football/output.mp4"
cap = cv2.VideoCapture(video_pth)
counter = 0
while True:
    image_copy = image_field.copy()
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame, conf=0.1)
    # for result in results:
    results[0].save(f'b_{counter}')
    counter += 1
        # break()
    #     breakpoint()
    #     for box in result.boxes:
    #         x_c = int((box.xyxy[0][0]+box.xyxy[0][2])/2)
    #         y_c = int((box.xyxy[0][1]+box.xyxy[0][3])/2)
    #         projected_point = transform_point(H, (x_c,y_c))
    #         cv2.circle(image_copy, projected_point, 20, (255,0,255), -1)
    # image_copy = cv2.resize(image_copy, (600, 400))
    # cv2.imshow('', image_copy)
    # cv2.imshow('original frame', frame)
    # key = cv2.waitKey(1)
    # if key == 113:
    #     break