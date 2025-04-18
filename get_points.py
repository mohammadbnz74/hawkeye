import cv2
import numpy as np

# Lists to store points
points_img1 = []
points_img2 = []

def select_points(event, x, y, flags, param):
    """Callback function to store selected points."""
    img, points = param
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x*2, y*2))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # Draw red dot
        cv2.imshow("Image", img)

def get_four_points(image_path, window_name):
    """Function to get four points from an image."""
    img = cv2.imread(image_path)
    img_copy = img.copy()
    h, w = img.shape[:2]
    img_copy = cv2.resize(img_copy, (w//2,h//2))
    points = []
    cv2.imshow("Image", img_copy)
    cv2.setMouseCallback("Image", select_points, (img_copy, points))

    while True:
        cv2.imshow("Image", img_copy)
        key = cv2.waitKey(1) & 0xFF
        if len(points) == 4:  # Stop when four points are selected
            break
        if key == ord('q'):  # Press 'q' to quit
            print(points)
            break

    cv2.destroyAllWindows()
    return points


# Load images
image1_path = "data/football/field.jpg"
print("Select four points in the first image...")
points_img1 = get_four_points(image1_path, "Image 1")
image2_path = f"data/football/frame.jpg"
print("Select four points in the second image...")
points_img2 = get_four_points(image2_path, "Image 2")

H, status = cv2.findHomography(np.array(points_img1), np.array(points_img2), method=0)  # method=0 is Direct Linear Transform (DLT)

np.save(f'data/football/homography_matrix.npy', H)