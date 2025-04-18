import cv2
import numpy as np

def select_points(event, x, y, flags, param):
    """Callback function to store selected points."""
    coords = param
    if event == cv2.EVENT_LBUTTONDOWN:
        coords[0] = x
        coords[1] = y

def get_four_points(image_path, window_name):
    """Function to get four points from an image."""
    xy = [0, 0]
    points = []

    img = cv2.imread(image_path)
    img_display = img.copy()
    h, w = img.shape[:2]
    img_display = cv2.resize(img_display, (w//2, h//2))

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", select_points, xy)

    while True:
        img_copy = img_display.copy()
        cv2.circle(img_copy, (xy[0], xy[1]), 2, (0, 0, 255), -1)
        cv2.imshow("Image", img_copy)

        key = cv2.waitKeyEx()
        if key == 113:  # 'q' key to exit
            break
        elif key == 115:  # 's' key to select point
            points.append((xy[0]*2, xy[1]*2))  # scale back to original image size
            print(f"Selected: {points[-1]}")
            if len(points) == 4:
                break
        elif key == 65362:  # Up arrow
            xy[1] = max(0, xy[1]-1)
        elif key == 65364:  # Down arrow
            xy[1] = min(img_display.shape[0]-1, xy[1]+1)
        elif key == 65361:  # Left arrow
            xy[0] = max(0, xy[0]-1)
        elif key == 65363:  # Right arrow
            xy[0] = min(img_display.shape[1]-1, xy[0]+1)

    cv2.destroyAllWindows()
    return points

# Load images
image1_path = "data/football/field.jpg"
print("Select four points in the first image...")
points_img1 = get_four_points(image1_path, "Image 1")

image2_path = "data/football/frame.jpg"
print("Select four points in the second image...")
points_img2 = get_four_points(image2_path, "Image 2")

H, status = cv2.findHomography(np.array(points_img1), np.array(points_img2), method=0)

np.save('data/football/homography_matrix.npy', H)
