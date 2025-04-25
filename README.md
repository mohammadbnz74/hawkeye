# hawkeye
i have calculated the homography matrix using the points in the frame and real values of a football pitch (i also have a top view of this pitch called field.jpg)
i can warp image to top view and vice versa
i used the matrix to convert real world parallel lines to lines in the image plane using warp_lines.py
i now want to use these lines to calculate and draw the vanishing point on the image

i also studied the code from this repository https://github.com/antoinekeller/soccer_tracker which calculates the key points and key lines using classic cv algorithms which can not be generalized (i give multiple frames with no output) but i found out that i need key features from frames in order to be able to calculate camera pose