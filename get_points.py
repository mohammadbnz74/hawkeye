import cv2
import numpy as np
from glob import glob
from utils import *

# Load images
image1_path = "data/football/field.jpg"
field = cv2.imread(image1_path)
h,w = field.shape[:2]
images = glob('data/football/frames/*.jpg')
for image2_path in images:
    name = image2_path.split('/')[-1][:-4]
    image = cv2.imread(image2_path)
    print("Select four points in the second image...")
    points_img2 = get_four_points(image, "Image 2")

    print("Select four points in the first image...")
    points_img1 = get_four_points(field, "Image 1")

    H, status = cv2.findHomography(np.array(points_img2), np.array(points_img1), method=0)

    np.save(f'data/football/homography_matrixes/{name}.npy', H)

    
    warped = cv2.warpPerspective(image, H, (w,h))
    cv2.imshow('', warped)
    if cv2.waitKey() & 0xFF == ord('q'):
        break
