import cv2
import numpy as np

def glitch_effect(img, strength=10):
    glitched = img.copy()
    h, w, _ = img.shape
    for i in range(0, h, 10):
        dx = np.random.randint(-strength, strength)
        start_col = max(0, dx)
        end_col = min(w - start_col, w)
        src_end = min(w, w - dx) if dx > 0 else w
        if end_col > 0:
            glitched[i:i+5, start_col:start_col+end_col] = img[i:i+5, 0:end_col]
    return glitched

def empty(a):
    pass

# Create window & sliders
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("❌ Camera not found. Check connection or try different index.")
    exit()

while True:
    success, img = cap.read()
    if not success or img is None:
        print("⚠️ Failed to read from camera.")
        continue

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get values from trackbars
    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Create mask and result
    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    glitch = glitch_effect(result)

    # Show output
    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", glitch)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
