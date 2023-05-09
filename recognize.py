

import cv2
import logging as log
from datetime import datetime
from con import Connection as con
from time import sleep
from dotenv import load_dotenv
import os

#env
load_dotenv()

class FaceRecognition:
    def __init__(self):
        self.dbname = os.environ.get("DB_NAME")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASSWORD")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.log = log.getLogger("webcam")
        self.log.setLevel(log.INFO)
        handler = log.FileHandler("webcam.log")
        self.log.addHandler(handler)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("trainer/trainer.yml")
        self.cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # names related to ids: example ==> Marcelo: id=1,  etc
        self.names = ["None", "Kiko", "Paulo", "Mccarry", "Z", "W"]

        # Initialize and start realtime video capture
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)  # set video width
        self.cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        self.minW = int(0.1 * self.cam.get(3))
        self.minH = int(0.1 * self.cam.get(4))

    def run(self):
        while True:
            ret, img = self.cam.read()
            img = cv2.flip(img, 1)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(self.minW, self.minH),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                id, confidence = self.recognizer.predict(gray[y : y + h, x : x + w])

                if confidence < 60:
                    name = self.names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    if name in ["Kiko", "Paulo"]:
                        #check if user already attended
                        query = f"SELECT COUNT(*) FROM accounts WHERE emp_id = '{id}'"

                        result = con.select(self, query, id)
                        print(result)
                        if result is not None:
                            query = f"INSERT INTO accounts (name, emp_id, time_in, time_out, date) VALUES ('{name}', '{id}', '{self.time}', '00:00:00', '{self.today}')"
                            con.insert(self, query)
                            self.log.info(f"{name} is attended! - {datetime.now()}")
                            print(f"{name} already attended! - {datetime.now()}")
                        else:
                            print(f"{name} attended! - {datetime.now()}")

                else:
                    name = "Unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                log_message = f"{name} is attended!" if name in ["Kiko", "Paulo"] else "Unknown person detected."
                self.log.info(log_message + str(datetime.now()))

                cv2.putText(
                    img, str(name), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2
                )
                cv2.putText(
                    img,
                    str(confidence),
                    (x + 5, y + h - 5),
                    self.font,
                    1,
                    (255, 255, 0),
                    1,
                )


            cv2.imshow("camera", img)

            k = cv2.waitKey(10) & 0xFF  # Press 'ESC' for


if __name__ == "__main__":
    FaceRecognition().run()
