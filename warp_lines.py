import numpy as np
import cv2


def clamp_point(pt, width, height):
    x = int(np.clip(pt[0], 0, width - 1))
    y = int(np.clip(pt[1], 0, height - 1))
    return (x, y)

def transform_point(H, point):
    """Apply homography transformation to a single point."""
    x_, y_ = point
    transformed = np.dot(H, np.array([x_, y_, 1]))
    transformed /= transformed[2]  # Normalize by w
    # return transformed[:2]  # Return (x, y) as a tuple
    return (int(transformed[0]),int(transformed[1]))  # Return (x, y) as a tuple

# Example points: Four points from Image 1 and Image 2
H = np.load(f'data/football/homography_matrix.npy')
H = np.linalg.inv(H)
image1 = cv2.imread("data/football/field.jpg")
cap = cv2.VideoCapture(f'data/football/output.mp4')
x0 = 30
y1, y2 = 0, 600
while True:
    ret, frame = cap.read()
    for i in range(23):
        x = x0+i*39
        p_1 = transform_point(H, (x,y1))
        p_2 = transform_point(H, (x,y2))
        cv2.line(frame, p_1, p_2, (0,255,255), 1)
    frame2 = frame.copy()
    frame2 = cv2.resize(frame2, (800,600))
    cv2.imshow('', frame2)
    # cv2.imshow('222', image1)
    if cv2.waitKey() & 0xFF == ord('q'):
        break