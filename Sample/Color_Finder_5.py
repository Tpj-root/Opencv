import cv2
import numpy as np
import tkinter as tk
from threading import Thread

# Default HSV ranges
default_ranges = {
    "green":  [35, 85, 100, 255, 100, 255],
    "red":    [0, 10, 100, 255, 100, 255],   # red needs special handling
    "blue":   [90, 130, 100, 255, 100, 255],
    "yellow": [20, 30, 100, 255, 100, 255],
    "orange": [10, 20, 100, 255, 100, 255],
    "white":  [0, 180, 0, 30, 200, 255]
}

selected_color = "green"
hsv_values = default_ranges["green"][:]  # copy, not reference

# Trackbar updater
def update_hsv():
    hsv_values[0] = hue_min.get()
    hsv_values[1] = hue_max.get()
    hsv_values[2] = sat_min.get()
    hsv_values[3] = sat_max.get()
    hsv_values[4] = val_min.get()
    hsv_values[5] = val_max.get()

# GUI and slider setup
def start_gui():
    global selected_color, hue_min, hue_max, sat_min, sat_max, val_min, val_max

    def on_color_change():
        global selected_color, hsv_values
        selected_color = color_var.get()
        hsv_values[:] = default_ranges[selected_color][:]  # force fresh copy
        # Update sliders
        hue_min.set(hsv_values[0])
        hue_max.set(hsv_values[1])
        sat_min.set(hsv_values[2])
        sat_max.set(hsv_values[3])
        val_min.set(hsv_values[4])
        val_max.set(hsv_values[5])

    root = tk.Tk()
    root.title("Color Range Control")

    color_var = tk.StringVar(value=selected_color)

    for col in default_ranges:
        tk.Radiobutton(root, text=col.capitalize(), variable=color_var, value=col, command=on_color_change).pack(anchor="w")

    # Sliders
    hue_min = tk.Scale(root, from_=0, to=179, orient="horizontal", label="Hue Min", command=lambda x: update_hsv())
    hue_min.pack()
    hue_max = tk.Scale(root, from_=0, to=179, orient="horizontal", label="Hue Max", command=lambda x: update_hsv())
    hue_max.pack()
    sat_min = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Sat Min", command=lambda x: update_hsv())
    sat_min.pack()
    sat_max = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Sat Max", command=lambda x: update_hsv())
    sat_max.pack()
    val_min = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Val Min", command=lambda x: update_hsv())
    val_min.pack()
    val_max = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Val Max", command=lambda x: update_hsv())
    val_max.pack()

    on_color_change()  # set initial slider values
    root.mainloop()

# OpenCV loop
def run_opencv():
    global hsv_values, selected_color
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if selected_color == "red":
            # red split range
            lower1 = np.array([hsv_values[0], hsv_values[2], hsv_values[4]])
            upper1 = np.array([hsv_values[1], hsv_values[3], hsv_values[5]])
            lower2 = np.array([160, hsv_values[2], hsv_values[4]])
            upper2 = np.array([179, hsv_values[3], hsv_values[5]])
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower = np.array([hsv_values[0], hsv_values[2], hsv_values[4]])
            upper = np.array([hsv_values[1], hsv_values[3], hsv_values[5]])
            mask = cv2.inRange(hsv, lower, upper)

        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Selected Color View", result)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Run both GUI and OpenCV
Thread(target=run_opencv).start()
start_gui()
