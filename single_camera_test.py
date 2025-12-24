import cv2
import mediapipe as mp
import time

# Mediapipe setup
mp_facedetector = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

# Open single camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Cannot open camera!")
    print("Make sure:")
    print("1. Camera is connected")
    print("2. No other app is using the camera")
    print("3. Camera permissions are granted")
    exit()

print("Camera opened successfully!")
print("Press 'q' to quit")

# Main loop with face detection
with mp_facedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Failed to read frame")
            break

        start = time.time()

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = face_detection.process(frame_rgb)

        # Convert back to BGR
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Draw face detections
        if results.detections:
            for detection in results.detections:
                mp_draw.draw_detection(frame, detection)
                bBox = detection.location_data.relative_bounding_box
                h, w, c = frame.shape
                boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)
                cv2.putText(frame, f'{int(detection.score[0]*100)}%',
                           (boundBox[0], boundBox[1] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Calculate FPS
        end = time.time()
        fps = 1 / (end - start)

        cv2.putText(frame, f'FPS: {int(fps)}', (20,450),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Show frame
        cv2.imshow("Face Detection Test", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("Program ended")
