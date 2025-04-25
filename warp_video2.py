import numpy as np
import cv2

i = 2
# Example points: Four points from Image 1 and Image 2
H = np.load(f'./homography_matrix.npy')
image1 = cv2.imread("data/football/field.jpg")
image1 = cv2.resize(image1, (105*8, 68*8))
cap = cv2.VideoCapture(f'data/football/output.mp4')
height, width = image1.shape[:2]
while True:
    ret, frame = cap.read()
    warped_image1 = cv2.warpPerspective(frame, H, (width, height))

    # Warp Image 1 to Image 2’s perspective
    mask = (warped_image1 > 0).astype(np.uint8)  # Non-black pixels are 1

    # Blend images: Replace only the masked area in image2
    blended = image1.copy()
    blended[mask == 1] = warped_image1[mask == 1]
    # blended = cv2.resize(blended, (width//4,height//4))
    cv2.imshow('', blended)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
