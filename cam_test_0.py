import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print("Camera OK?" if ret else "Camera NOT working")
cap.release()
