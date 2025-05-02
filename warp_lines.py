import numpy as np
import cv2
from utils import *
import os


def draw_line_to_vp(canvas, line_segment, vp_canvas):
    if line_segment is None:
        return
    p1, p2 = line_segment
    d1 = np.linalg.norm(np.array(p1) - np.array(vp_canvas))
    d2 = np.linalg.norm(np.array(p2) - np.array(vp_canvas))
    
    # Draw from the farther point toward the vanishing point
    if d1 > d2:
        start = p1
    else:
        start = p2

    cv2.line(canvas, start, vp_canvas, (0, 255, 255), 1)


field = cv2.imread('data/football/field.jpg')
h_field, w_field = field.shape[:2]
x0 = 30
y1, y2 = 0, h_field - 1

homography_dir = 'data/football/homography_matrixes'
image_dir = 'data/football/frames'

for pth in os.listdir(homography_dir):
    name = pth[:-4]
    matrix_pth = os.path.join(homography_dir, name + '.npy')

    H = np.load(matrix_pth)
    H = np.linalg.inv(H)

    image_pth = os.path.join(image_dir, name + '.jpg')
    image = cv2.imread(image_pth)
    height, width = image.shape[:2]

    lines = []

    for x in [0,37,134,347,419,493,704,801,840]:
        # x = x0 + i * 39
        original_line = compute_line((x, y1), (x, y2))
        line = transform_line(H, original_line)
        lines.append(line)
    # Compute vanishing point from line intersections
    vp = None
    count = 0
    sum_vp = np.zeros(2)
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            pt = compute_intersection(lines[i], lines[j])
            if pt is not None and -5 * width < pt[0] < 6 * width and -5 * height < pt[1] < 6 * height:
                sum_vp += pt
                count += 1

    if count > 0:
        vp = sum_vp / count
        vp_int = vp.astype(int)

        # Calculate required margins
        left_margin = max(0, -vp_int[0])
        right_margin = max(0, vp_int[0] - width)
        top_margin = max(0, -vp_int[1])
        bottom_margin = max(0, vp_int[1] - height)

        # New canvas size
        canvas_w = width + left_margin + right_margin
        canvas_h = height + top_margin + bottom_margin

        # Create new canvas and paste the original image
        canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
        canvas[top_margin:top_margin + height, left_margin:left_margin + width] = image

        # Update image and vanishing point position relative to new canvas
        # image = canvas
        vp_int_canvas = (vp_int[0] + left_margin, vp_int[1] + top_margin)

        # Draw the vanishing point
        cv2.circle(canvas, vp_int_canvas, 6, (0, 0, 255), -1)

        for line in lines:
            segment = line_intersections_with_borders(line, canvas_w, canvas_h)
            if segment:
                for seg in segment:
                    cv2.circle(image, seg, 50, (200,100,200), -1)
            draw_line_to_vp(canvas, segment, vp_int_canvas)
 
        canvas_display = cv2.resize(canvas, (800,600))
        cv2.imshow('Vanishing Point (Extended)', canvas_display)
    else:
        cv2.imshow('Vanishing Point', image)

    key = cv2.waitKey()
    if key == ord('q'):
        break
