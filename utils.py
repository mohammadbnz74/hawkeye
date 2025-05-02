import cv2
import numpy as np


def select_points(event, x, y, flags, param):
    """Callback function to store selected points."""
    coords = param
    if event == cv2.EVENT_LBUTTONDOWN:
        coords[0] = x
        coords[1] = y

def get_four_points(img, window_name):
    """Function to get four points from an image."""
    xy = [0, 0]
    points = []

    img_display = img.copy()
    h, w = img.shape[:2]
    # img_display = cv2.resize(img_display, (w//2, h//2))

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
            # points.append((xy[0]*2, xy[1]*2))  # scale back to original image size
            points.append((xy[0], xy[1]))  # scale back to original image size
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


def line_intersections_with_borders(line, width, height):
    borders = [
        np.cross(line, [1, 0, 0]),         # Left border (x = 0)
        np.cross(line, [1, 0, -width+1]),  # Right border (x = width-1)
        np.cross(line, [0, 1, 0]),         # Top border (y = 0)
        np.cross(line, [0, 1, -height+1])  # Bottom border (y = height-1)
    ]

    points = []
    for pt in borders:
        if pt[2] != 0:
            x, y = pt[0]/pt[2], pt[1]/pt[2]
            if 0 <= x < width and 0 <= y < height:
                points.append((int(x), int(y)))

    if len(points) >= 2:
        return points[:2]  # Return two valid intersection points
    return None


def clamp_point(pt, width, height):
    x = int(np.clip(pt[0], 0, width - 1))
    y = int(np.clip(pt[1], 0, height - 1))
    return (x, y)

def transform_line(H, line):
    H_inv_T = np.linalg.inv(H).T
    return H_inv_T @ line

def transform_point(H, point):
    x_, y_ = point
    transformed = np.dot(H, np.array([x_, y_, 1]))
    transformed /= transformed[2]
    return transformed[:2]

def compute_line(p1, p2):
    return np.cross(np.append(p1, 1), np.append(p2, 1))

def compute_intersection(l1, l2):
    pt = np.cross(l1, l2)
    if pt[2] == 0:
        return None  # Parallel lines
    return pt[:2] / pt[2]
