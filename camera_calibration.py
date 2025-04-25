import cv2
import numpy as np

# Load your frame (update the path)
image = cv2.imread("data/football/frame.jpg")
h, w = image.shape[:2]
clone = image.copy()
clone = cv2.resize(clone, (w//2,h//2))
clicked_points = []

# Define real-world coordinates (meters)
# Example: corners of the pitch in (X, Y)
# Adjust based on the points you click
world_points = np.array([
    [105/2, 68],          # bottom-left corner
    [88.5, 68-54.16],        # bottom-right
    [105/2, 68-24.85],       # top-right
    [16.5, 68-54.16]          # top-left
], dtype=np.float32)

# Mouse callback to collect 4 points
def click_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x*2, y*2])
        cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Click 4 field points", clone)

cv2.imshow("Click 4 field points", clone)
cv2.setMouseCallback("Click 4 field points", click_point)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Check if 4 points were clicked
if len(clicked_points) != 4:
    raise Exception("You must click exactly 4 points!")

image_points = np.array(clicked_points, dtype=np.float32)

# Compute homography
H, _ = cv2.findHomography(image_points, world_points*8)
np.save(f'./homography_matrix.npy', H)
# Warp the image to a top-down view (size = field in meters * scale)
scale = 8  # pixels per meter
output_size = (int(105 * scale), int(68 * scale))  # width, height

warped = cv2.warpPerspective(image, H, output_size)
# warped = cv2.resize(warped, (1000,800))
# Show result
cv2.imshow("Top-down View", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

scale = 8  # pixels per meter
output_size = (int(68 * scale), int(105 * scale), 3)  # width, height
image = np.zeros(output_size)
for i, pt in enumerate(world_points):
    x,y = pt
    print(i,x,y)
    cv2.circle(image, (int(x*8),int(y*8)), 3, (i*50,i*50,i*50), -1)

    cv2.imshow('', image)
    cv2.waitKey()

'''