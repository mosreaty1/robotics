import cv2

# Initialize cameras
cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)

# Counter for saved images
num = 0

# Desired image size (width, height)
resize_width = 640
resize_height = 480

while cap.isOpened():

    # Capture frames from both cameras
    succes1, img = cap.read()
    succes2, img2 = cap2.read()
    k = cv2.waitKey(5)

    if k == 27:  # Exit on ESC key
        break
    elif k == ord('s'):  # Save images on 's' key press
        if succes1 and succes2:
            # Resize images to the same size
            img_resized = cv2.resize(img, (resize_width, resize_height))
            img2_resized = cv2.resize(img2, (resize_width, resize_height))

            # Save resized images
            cv2.imwrite('images/stereoLeft/imageL' + str(num) + '.png', img_resized)      
            cv2.imwrite('images/stereoright/imageR' + str(num) + '.png', img2_resized)
            print(f"Images saved: imageL{num}.png and imageR{num}.png")
            num += 1
        else:
            print("Failed to capture images from one or both cameras.")

    # Resize images for display
    if succes1:
        img_display = cv2.resize(img, (resize_width, resize_height))
        cv2.imshow('Img 1', img_display)
    if succes2:
        img2_display = cv2.resize(img2, (resize_width, resize_height))
        cv2.imshow('Img 2', img2_display)

# Release resources
cap.release()
cap2.release()
cv2.destroyAllWindows()
