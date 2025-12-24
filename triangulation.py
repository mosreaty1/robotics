import sys
import cv2
import numpy as np
import time


def find_depth(right_point, left_point, frame_right, frame_left, baseline,f, alpha):

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    else:
        print('Left and right camera frames do not have the same pixel width')
        # Use average width if they don't match
        avg_width = (width_right + width_left) / 2
        f_pixel = (avg_width * 0.5) / np.tan(alpha * 0.5 * np.pi/180)

    x_right = right_point[0]
    x_left = left_point[0]

    # CALCULATE THE DISPARITY:
    disparity = x_left-x_right      #Displacement between left and right frames [pixels]

    # CALCULATE DEPTH z:
    # Avoid division by zero
    if disparity == 0:
        return 0

    zDepth = (baseline*f_pixel)/disparity             #Depth in [cm]

    return abs(zDepth)
