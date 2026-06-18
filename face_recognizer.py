import face_recognition
import cv2

webcam = cv2.VideoCapture(0, cv2.CAP_V4L2)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
webcam.set(cv2.CAP_PROP_FOURCC, fourcc)


while True:
    
    ret, frame = webcam.read()
    cv2.imshow('webcam', frame)
    if not ret or frame is None:
        print("警告：画面读取超时，正在重试...")
        continue
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vedio_capture.release()
cv2.destoryAllWindows()