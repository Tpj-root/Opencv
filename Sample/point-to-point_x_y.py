import cv2
import numpy as np

# Open camera
cap = cv2.VideoCapture(0)

# Create black image to draw trail
trail = np.zeros((480, 640, 3), dtype=np.uint8)

# Open file to save data
file = open("led_path.txt", "w")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 5:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            cv2.circle(trail, center, 2, (0, 255, 0), -1)

            # Save (x,y) to file
            file.write(f"{center[0]},{center[1]}\n")

    combined = cv2.addWeighted(frame, 0.5, trail, 0.5, 0)
    cv2.imshow("LED Tracker", combined)

    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

file.close()
cap.release()
cv2.destroyAllWindows()
