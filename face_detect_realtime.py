import face_recognition
import cv2
import numpy as np


# Load a sample picture and learn how to recognize it.
sontung_image = face_recognition.load_image_file("D:\miAi\ComputerVision\FaceRecognition\sontung.jpg")
sontung_face_encoding = face_recognition.face_encodings(sontung_image)[0]

# Load a second sample picture and learn how to recognize it.
ducphuc_image = face_recognition.load_image_file("D:\miAi\ComputerVision\FaceRecognition\ducphuc.jpg")
ducphuc_face_encoding = face_recognition.face_encodings(ducphuc_image)[0]

domixi_image= face_recognition.load_image_file("D:\miAi\ComputerVision\FaceRecognition\domixi.jpg")
domixi_face_encoding = face_recognition.face_encodings(domixi_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    sontung_face_encoding,
    ducphuc_face_encoding,
    domixi_face_encoding
]
known_face_names = [
    "Son Tung",
    "Duc Phuc",
    "Do Mixi"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


capture = cv2.VideoCapture(0)

while True:
    
    # Grab a single frame of video
    ret, frame = capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 4, bottom - 4), font, 1, (0,0,255), 2)


    # Display the resulting image
    cv2.imshow('RealTime', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
capture.release()
cv2.destroyAllWindows()
