import cv2
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
print("Camera OK?" if ret else "Camera NOT working")
cap.release()
