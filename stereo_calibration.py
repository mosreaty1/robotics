import cv2 as cv
import numpy as np
import glob

# Chessboard dimensions (number of internal corners in rows and columns)
rows = 6
columns = 9
frameSize = None

# Prepare object points (3D points in real world)
objp = np.zeros((rows * columns, 3), np.float32)
objp[:, :2] = np.mgrid[0:columns, 0:rows].T.reshape(-1, 2)

# Arrays to store object points and image points for both cameras
objpoints = []  # 3D points in real world
imgpointsL = []  # 2D points for left camera
imgpointsR = []  # 2D points for right camera

# Load left and right camera images
images_left = glob.glob('images/stereoLeft/*.png')
images_right = glob.glob('images/stereoright/*.png')

# Check if both sets of images exist
if len(images_left) == 0 or len(images_right) == 0:
    print("Error: No images found in stereoLeft or stereoright directories.")
    exit()

# Ensure both directories have the same number of images
if len(images_left) != len(images_right):
    print("Error: Mismatch in number of images between left and right cameras.")
    exit()

# Process images for both cameras
for fnameL, fnameR in zip(images_left, images_right):
    imgL = cv.imread(fnameL)
    imgR = cv.imread(fnameR)

    if imgL is None or imgR is None:
        print(f"Failed to load images: {fnameL} or {fnameR}")
        continue

    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    if frameSize is None:
        frameSize = (grayL.shape[1], grayL.shape[0])  # Set frame size once

    # Find chessboard corners for both cameras
    retL, cornersL = cv.findChessboardCorners(grayL, (columns, rows), None)
    retR, cornersR = cv.findChessboardCorners(grayR, (columns, rows), None)

    if retL and retR:
        objpoints.append(objp)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)

        # Draw and display corners for debugging
        cv.drawChessboardCorners(imgL, (columns, rows), cornersL, retL)
        cv.drawChessboardCorners(imgR, (columns, rows), cornersR, retR)
        cv.imshow('Corners Left', imgL)
        cv.imshow('Corners Right', imgR)
        cv.waitKey(500)
    else:
        print(f"Chessboard not detected in: {fnameL} or {fnameR}")

cv.destroyAllWindows()

# Perform calibration for each camera
if len(objpoints) > 0 and len(imgpointsL) > 0 and len(imgpointsR) > 0:
    # Left camera calibration
    retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(
        objpoints, imgpointsL, frameSize, None, None
    )
    print("Left Camera Calibration Successful!")
    print(f"Camera Matrix (Left):\n{cameraMatrixL}")
    print(f"Distortion Coefficients (Left):\n{distL}")

    # Right camera calibration
    retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(
        objpoints, imgpointsR, frameSize, None, None
    )
    print("Right Camera Calibration Successful!")
    print(f"Camera Matrix (Right):\n{cameraMatrixR}")
    print(f"Distortion Coefficients (Right):\n{distR}")

    # Stereo calibration
    retStereo, cameraMatrixL, distL, cameraMatrixR, distR, R, T, E, F = cv.stereoCalibrate(
        objpoints,
        imgpointsL,
        imgpointsR,
        cameraMatrixL,
        distL,
        cameraMatrixR,
        distR,
        frameSize,
        flags=cv.CALIB_FIX_INTRINSIC
    )
    print("Stereo Calibration Successful!")
    print(f"Rotation Matrix (R):\n{R}")
    print(f"Translation Vector (T):\n{T}")
    print(f"Essential Matrix (E):\n{E}")
    print(f"Fundamental Matrix (F):\n{F}")

else:
    print("Error: Not enough valid points for calibration.")
