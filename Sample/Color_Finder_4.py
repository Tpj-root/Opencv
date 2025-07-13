import cv2
import numpy as np
import tkinter as tk
from threading import Thread

# Define HSV color ranges
colors = {
    "green":  ([35, 100, 100], [85, 255, 255]),
    "red1":   ([0, 100, 100], [10, 255, 255]),
    "red2":   ([160, 100, 100], [179, 255, 255]),
    "blue":   ([90, 100, 100], [130, 255, 255]),
    "yellow": ([20, 100, 100], [30, 255, 255]),
    "orange": ([10, 100, 100], [20, 255, 255]),
    "white":  ([0, 0, 200], [180, 30, 255])
}

selected_color = "green"  # default

# Threaded video display
def run_opencv():
    global selected_color
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = np.zeros_like(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

        if selected_color == "red":
            lower1 = np.array(colors["red1"][0])
            upper1 = np.array(colors["red1"][1])
            lower2 = np.array(colors["red2"][0])
            upper2 = np.array(colors["red2"][1])
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower, upper = colors[selected_color]
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Selected Color", result)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI setup
def start_gui():
    global selected_color
    root = tk.Tk()
    root.title("Color Selector")

    def on_select():
        global selected_color
        selected_color = color_var.get()

    color_var = tk.StringVar(value="green")

    for col in ["green", "red", "blue", "yellow", "orange", "white"]:
        tk.Radiobutton(root, text=col.capitalize(), variable=color_var,
                       value=col, command=on_select).pack(anchor="w")

    tk.Label(root, text="Press ESC in OpenCV window to quit").pack()
    root.mainloop()

# Run GUI + OpenCV in parallel
Thread(target=run_opencv).start()
start_gui()
