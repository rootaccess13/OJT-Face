import cv2
from datetime import datetime
import logging as log
from con import Connection as con
import os
from decider import Decider
from smtp import SendEmail
from dotenv import load_dotenv

load_dotenv()

class RecognizerInstance:

    # def __init__(self, recognizer, face_detector, smile_detector, connection):
    def __init__(self, recognizer, face_detector, connection):
        self.recognizer = recognizer
        self.face_detector = face_detector
        # self.smile_detector = smile_detector
        self.connection = connection
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.log = log.basicConfig(filename="recognizer.log", level=log.INFO)
        self.names = ["None", "Kiko", "Paulo", "Mccarry"]
        self.time = datetime.now().strftime("%H:%M:%S")
        self.decider = Decider()


    def recognize(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(0.1 * img.shape[1]), int(0.1 * img.shape[0])),
        )



        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 2)
            id, confidence = self.recognizer.predict(gray[y : y + h, x : x + w])
            name = self.names[id]
            check = con.checkUser(self.connection, id)
            formatted_dates = [d[0].strftime("%Y-%m-%d") for d in check]
            print(formatted_dates)
            # smile = self.smile_detector.detectMultiScale(
            #     gray, scaleFactor=1.7, minNeighbors=20, minSize=(10, 10)
            # )
            # for (sx, sy, sw, sh) in smile:
            #     cv2.rectangle(img, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)
            #     cv2.putText(
            #         img,
            #         "Smile",
            #         (sx + 5, sy - 5),
            #         cv2.FONT_HERSHEY_SIMPLEX,
            #         1,
            #         (0, 255, 0),
            #         1,
            #         cv2.LINE_AA,
            #     )

            if not formatted_dates:
                continue
            else:

                if self.today != formatted_dates[-1]:
                    print("Not in Database - Inserting ...")
                    try:
                        # send = SendEmail()
                        # send.send(os.environ.get("RECEIVER_EMAIL"), "Hello, {0} has arrived at {1}".format(name, self.time))
                        
                        res = con.insert(self.connection,"INSERT INTO accounts (emp_id, name, date, time_in, time_out) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(id, name, self.today, self.time, '00:00:00'))
                        print(res)
                    except Exception as e:
                        print(e)
                else:
                    print("Already in Database - Updating ...")



            if confidence < 100 and confidence > 50:

                if name in self.names:
                    confidence = "  {0}%".format(round(100 - confidence))
                    name = name
                    print("Recognized: {0}".format(name))
                
            elif confidence < 30:
                confidence = "Unrecognized"
                name = "Unknown"

            
            cv2.putText(
                img,
                str(name),
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                img,
                str(confidence),
                (x + 5, y + h - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                1,
            )
        return img


