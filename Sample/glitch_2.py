import cv2
import numpy as np

def glitch_effect_rgb(img, strength=20):
    if strength <= 0:
        return img.copy()

    b, g, r = cv2.split(img)
    h, w = img.shape[:2]

    for i in range(0, h, 5):
        shift = np.random.randint(-strength, strength)
        if shift > 0:
            b[i] = np.roll(b[i], shift)
        else:
            r[i] = np.roll(r[i], -shift)

    glitched = cv2.merge([b, g, r])
    return glitched


def empty(a): pass

# Create window & sliders
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 300)
cv2.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Glitch Strength", "Trackbars", 0, 50, empty)  # New control

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("❌ Camera not found.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        continue

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")
    glitch_strength = cv2.getTrackbarPos("Glitch Strength", "Trackbars")  # Read value

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    glitch = glitch_effect_rgb(result, glitch_strength)

    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", glitch)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
