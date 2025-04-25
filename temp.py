import numpy as np
import cv2

# Example Homography (replace with yours)
H = np.load('data/football/homography_matrix.npy')
# Two lines in the world (both parallel in world, but not collinear)
A1 = np.array([0, 0, 1])
A2 = np.array([1000, 0, 1])
B1 = np.array([0, 10, 1])
B2 = np.array([1000, 10, 1])

# Project to image
a1 = H @ A1
a2 = H @ A2
a1 /= a1[2]
a2 /= a2[2]

b1 = H @ B1
b2 = H @ B2
b1 /= b1[2]
b2 /= b2[2]

# Get lines from point pairs
line1 = np.cross(a1, a2)
line2 = np.cross(b1, b2)

# Vanishing point = intersection of these two image lines
vp = np.cross(line1, line2)
vp /= vp[2]
# Show on a blank image
img = np.ones((600, 800, 3), dtype=np.uint8) * 255
vp_pt = (int(vp[0]), int(vp[1]))
cv2.circle(img, vp_pt, 8, (0, 0, 255), -1)
cv2.putText(img, "Vanishing Point", (vp_pt[0]+10, vp_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

cv2.imshow("Vanishing Point", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
