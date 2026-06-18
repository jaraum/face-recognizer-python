import face_recognition
import cv2
import numpy as np

webcam = cv2.VideoCapture(0)

# change to MJPG tomake it able to run on wsl
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
webcam.set(cv2.CAP_PROP_FOURCC, fourcc)

wjc_image = face_recognition.load_image_file("image.png")
wjc_face_encoding = face_recognition.face_encodings(wjc_image)[0]

known_face_encodings = [
    wjc_face_encoding,
]
known_face_names = [
    "wjc"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

counter = 0
while True:
    ret, bgr_frame = webcam.read()
    
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
    bounding_boxes = face_recognition.face_locations(rgb_frame)
    
    if counter%8 == 0:
        bounding_boxes = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, bounding_boxes)
        
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]


            face_names.append(name)
    counter+= 1
    
    
    if bounding_boxes:
        box = bounding_boxes[0]
        print(box)
        (top, right, bottom, left) = box
        # Draw a box around the face
        cv2.rectangle(bgr_frame, (left, top), (right, bottom), (255, 0, 0), 2)   #format: image, (x1,y1), (x2,y2), bgr_color, thickness
         # Draw a label with a name below the face
        cv2.rectangle(bgr_frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(bgr_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
    cv2.imshow('webcam', bgr_frame)
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vedio_capture.release()
cv2.destoryAllWindows()