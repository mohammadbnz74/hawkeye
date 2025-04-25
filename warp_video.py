import numpy as np
import cv2

i = 2
# Example points: Four points from Image 1 and Image 2
H = np.load(f'data/football/homography_matrix.npy')
H = np.linalg.inv(H)
image1 = cv2.imread("data/football/field.jpg")
cap = cv2.VideoCapture(f'data/football/output.mp4')
ret, frame = cap.read()
height, width = frame.shape[:2]
warped_image1 = cv2.warpPerspective(image1, H, (width, height))

while ret:
    ret, frame = cap.read()
    # Warp Image 1 to Image 2’s perspective
    mask = (warped_image1 > 0).astype(np.uint8)  # Non-black pixels are 1

    # Blend images: Replace only the masked area in image2
    blended = frame.copy()
    blended[mask == 1] = warped_image1[mask == 1]
    blended = cv2.resize(blended, (width//4,height//4))
    cv2.imshow('', blended)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
