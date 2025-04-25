import cv2
import numpy as np

def select_points(event, x, y, flags, param):
    """Callback function to store selected points."""
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img[x,y])
        cv2.imshow("image", img)


# Load the image
image = cv2.imread('data/football/field.jpg')
print(image.shape)
# image = cv2.resize(image, (600,400))
x0 = 30
for i in range(22):
    x = x0+i*39
    cv2.line(image, (x,0), (x,3000), (0,255,255), 1)
    print(x)
cv2.imshow('', image)
key = cv2.waitKeyEx()
'''
x = 1000
y = 10
while True:
    img_copy = image.copy()
    cv2.line(img_copy, (0,y), (600,y), (0,255,255), 1)
    cv2.line(img_copy, (x,0), (x,400), (255,0,70), 1)
    cv2.imshow('', img_copy)
    key = cv2.waitKeyEx()
    if key == 113:  # ESC key to exit
        break
    elif key == 65362:  # Up arrow key
        y-=1
    elif key == 65364:  # Down arrow key
        y+=1
    elif key == 65361:  # Left arrow key
        x-=1
    elif key == 65363:  # Right arrow key
        x+=1
    print(x,y)
'''