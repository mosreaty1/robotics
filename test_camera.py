import cv2

# Test camera access
print("Testing camera access...")

# Try camera 0
print("\nTrying Camera 0...")
cap0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if cap0.isOpened():
    print("✓ Camera 0 is accessible")
    ret, frame = cap0.read()
    if ret:
        print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
    cap0.release()
else:
    print("✗ Camera 0 failed to open")

# Try camera 1
print("\nTrying Camera 1...")
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if cap1.isOpened():
    print("✓ Camera 1 is accessible")
    ret, frame = cap1.read()
    if ret:
        print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
    cap1.release()
else:
    print("✗ Camera 1 failed to open")

print("\n" + "="*50)
print("RESULT: You need 2 working cameras for stereo vision")
print("="*50)
