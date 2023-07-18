import cmake
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

#load known faces

Adityas_image = face_recognition.load_image_file("faces/aditya.jpeg")
Adityas_encoding = face_recognition.face_encodings(Adityas_image)[0] #gives the first face

chris_image = face_recognition.load_image_file("faces/chris.jpeg")
chris_encoding  = face_recognition.face_encodings(chris_image)[0] #first image

known_face_encoding  = [Adityas_encoding,chris_encoding]

known_face_names = ["Aditya","Chris Hemsworth"]

#list of expected students
students = known_face_names.copy()

#search the faces
face_locations = []
face_encodings = []

#get the current date and time
now  = datetime.now()

current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+",newline="")

lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)
    rbg_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    #Recognising faces
    face_locations = face_recognition.face_locations(rbg_small_frame) # take the faces from here
    face_encodings = face_recognition.face_encodings(rbg_small_frame,face_locations) # convert into encodings

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
        face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
        best_match_index = np.argmin(face_distance)

        if(matches[best_match_index]):
            name = known_face_names[best_match_index]

            cv2.imshow("Attendace",frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()