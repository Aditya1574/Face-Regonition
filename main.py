import cmake
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import win32com.client as wincom

video_capture = cv2.VideoCapture(0)
speak = wincom.Dispatch("SAPI.SpVoice")
#load known faces

Adityas_image = face_recognition.load_image_file("faces/aditya.jpeg")
Adityas_encoding = face_recognition.face_encodings(Adityas_image)[0] #gives the first face

chris_image = face_recognition.load_image_file("faces/chris.jpeg")
chris_encoding  = face_recognition.face_encodings(chris_image)[0] #first image

Adhyas_image = face_recognition.load_image_file("faces/Adhya.jpg")
Adhyas_encoding = face_recognition.face_encodings(Adhyas_image)[0] #gives the first face

Kratis_image = face_recognition.load_image_file("faces/Krati.jpg")
Kratis_encoding = face_recognition.face_encodings(Kratis_image)[0] #gives the first face

Neerajs_image = face_recognition.load_image_file("faces/Neeraj.jpg")
Neerajs_encoding = face_recognition.face_encodings(Neerajs_image)[0] #gives the first face

Paris_image = face_recognition.load_image_file("faces/Pari.jpg")
Paris_encoding = face_recognition.face_encodings(Paris_image)[0] #gives the first face

Ritus_image = face_recognition.load_image_file("faces/Ritu.jpg")
Ritus_encoding = face_recognition.face_encodings(Ritus_image)[0] #gives the first face

Shrutis_image = face_recognition.load_image_file("faces/Shruti.jpg")
Shrutis_encoding = face_recognition.face_encodings(Shrutis_image)[0] #gives the first face

known_face_encoding  = [Adityas_encoding,chris_encoding,Adhyas_encoding,Kratis_encoding,Neerajs_encoding,Paris_encoding,Ritus_encoding,Shrutis_encoding]

known_face_names = ["Aditya","Chris","Adhya","Krati","Neeraj","Pari","Ritu","Shruti"]

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
    # if frame is None:
    #     print(f"Cannot Reocrd Image _ =  {_}")
    #     break
    # else:
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

        #add name if the person is present
        if name in known_face_names:
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # bottomLeftCornerOfText = (10,100)
            # fontScale = 1.5
            # fontColor = (255,0,0)
            # thickess = 3
            # lineType = 2
            # cv2.putText(frame, name + " Hello ", bottomLeftCornerOfText,font,fontScale,fontColor, thickess, lineType)
            text = f"Hello, {name} i recognise you"
            speak.Speak(text)

    cv2.imshow("Attendace",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()