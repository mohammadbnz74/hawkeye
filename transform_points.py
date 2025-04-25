import cv2
import numpy as np


def transform_point(H, point):
    """Apply homography transformation to a single point."""
    x, y = point
    transformed = np.dot(H, np.array([x, y, 1]))
    transformed /= transformed[2]  # Normalize by w
    # return transformed[:2]  # Return (x, y) as a tuple
    return (int(transformed[0]),int(transformed[1]))  # Return (x, y) as a tuple


H = np.load(f'data/football/homography_matrix.npy')
H = np.linalg.inv(H)
image = cv2.imread("data/football/field.jpg")
image_2 = cv2.imread("data/football/frame.jpg")
clone = image.copy()
clicked_points = []

# Mouse callback to collect 4 points
def click_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        x_new, y_new = transform_point(H, (x,y))
        print(type(x),type(y))
        print(x_new,y_new)
        cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
        cv2.circle(image_2, (x_new, y_new), 5, (0, 255, 0), -1)
        cv2.imshow("Click 4 field points", clone)
        cv2.imshow("Cs", image_2)

cv2.imshow("Click 4 field points", clone)
cv2.setMouseCallback("Click 4 field points", click_point)
cv2.waitKey(0)
cv2.destroyAllWindows()
