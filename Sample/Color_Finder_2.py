import cv2
import numpy as np

# Define HSV color ranges
colors = {
    "green":  ([35, 100, 100], [85, 255, 255]),
    "red1":   ([0, 100, 100], [10, 255, 255]),
    "red2":   ([160, 100, 100], [179, 255, 255]),  # Red spans edges
    "blue":   ([90, 100, 100], [130, 255, 255]),
    "yellow": ([20, 100, 100], [30, 255, 255]),
    "orange": ([10, 100, 100], [20, 255, 255]),
    "white":  ([0, 0, 200], [180, 30, 255])
}

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    output = frame.copy()

    for name, (lower, upper) in colors.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        mask = cv2.inRange(hsv, lower_np, upper_np)

        if name == "red1":
            mask1 = mask
        elif name == "red2":
            mask2 = mask
            mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(output, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Detected Colors", output)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
