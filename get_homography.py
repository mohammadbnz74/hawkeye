import numpy as np
import cv2

def transform_point(H, point):
    """Apply homography transformation to a single point."""
    x, y = point
    transformed = np.dot(H, np.array([x, y, 1]))
    transformed /= transformed[2]  # Normalize by w
    return transformed[:2]  # Return (x, y) as a tuple

i = 3
# Example points: Four points from Image 1 and Image 2
H = np.load(f'data/video_input{i}_matrix.npy')
H = np.linalg.inv(H)# Compute the homography matrix

# Compute the homography matrix

image1 = cv2.imread("data/tennis_court.jpg")
image2 = cv2.imread(f"data/frame_input{i}.jpg")

height, width = image1.shape[:2]

# Warp Image 1 to Image 2’s perspective
warped_image1 = cv2.warpPerspective(image2, H, (width, height))

mask = (warped_image1 > 0).astype(np.uint8)  # Non-black pixels are 1

# Blend images: Replace only the masked area in image2
blended = image1.copy()
blended[mask == 1] = warped_image1[mask == 1]
# blended = cv2.resize(blended, (width//4,height//4))
blended = cv2.resize(blended, (400,600))
cv2.imshow('', blended)
cv2.waitKey(0)