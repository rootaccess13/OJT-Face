
import cv2
import logging as log
from datetime import datetime
from con import Connection as con
from time import sleep
from dotenv import load_dotenv
from recognizer import RecognizerInstance
import os

#env
load_dotenv()

class Main:
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
        self.names = ["None", "Kiko", "Paulo", "Mccarry"]
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("trainer/trainer.yml")
        self.facecascadePath = os.path.abspath("haarcascade_frontalface_default.xml")
        self.smilecascadePath = os.path.abspath("haarcascade_smile.xml")
        self.faceCascade = cv2.CascadeClassifier(self.facecascadePath)
        self.smileCascade = cv2.CascadeClassifier(self.smilecascadePath)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # names related to ids: example ==> Marcelo: id=1,  etc
        self.names = ["None", "Kiko", "Paulo", "Mccarry"]

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
            # recog = RecognizerInstance(self.recognizer, self.faceCascade,self.smileCascade, con(self.dbname, self.user, self.password, self.host, self.port))
            recog = RecognizerInstance(self.recognizer, self.faceCascade, con(self.dbname, self.user, self.password, self.host, self.port))

            img = recog.recognize(img)
            print(img)
            cv2.imshow("camera", img)
            k = cv2.waitKey(10) & 0xFF
            if k == 27:  # press 'ESC' to quit
                break
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        self.cam.release()
        cv2.destroyAllWindows()
        


if __name__ == "__main__":
    Main().run()
