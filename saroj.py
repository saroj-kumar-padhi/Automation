import datetime
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from voiceAssistent import Voice


def presentation():
    from cvzone.HandTrackingModule import HandDetector
    
    import cv2
    import os
    import numpy as np

    # Parameters
    width, height = 1280, 720
    gestureThreshold = 300
    folderPath = "Presentation"

    # Camera Setup
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Hand Detector
    detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

    # Variables
    imgList = []
    delay = 30
    buttonPressed = False
    counter = 0
    drawMode = False
    imgNumber = 0
    delayCounter = 0
    annotations = [[]]
    annotationNumber = -1
    annotationStart = False
    hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

    # Get list of presentation images
    pathImages = sorted(os.listdir(folderPath), key=len)
    print(pathImages)

    while True:
        # Get image frame
        success, img = cap.read()
        img = cv2.flip(img, 1)
        pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
        imgCurrent = cv2.imread(pathFullImage)

        # Find the hand and its landmarks
        hands, img = detectorHand.findHands(img)  # with draw
        # Draw Gesture Threshold line
        cv2.line(img, (0, gestureThreshold),
                 (width, gestureThreshold), (0, 255, 0), 10)

        if hands and buttonPressed is False:  # If hand is detected

            hand = hands[0]
            # cx, cy = hand["center"]
            lmList = hand["lmList"]  # List of 21 Landmark points
            # List of which fingers are up
            fingers = detectorHand.fingersUp(hand)

            # Constrain values for easier drawing
            xVal = int(np.interp(lmList[8][0], [
                       width // 2, width], [0, width]))
            yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
            indexFinger = xVal, yVal

            # if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(imgCurrent, indexFinger,
                           12, (0, 0, 255), cv2.FILLED)

            if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                print(annotationNumber)
                annotations[annotationNumber].append(indexFinger)
                cv2.circle(imgCurrent, indexFinger,
                           12, (0, 0, 255), cv2.FILLED)

            else:
                annotationStart = False

            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

        else:
            annotationStart = False

        if buttonPressed:
            counter += 1
            if counter > delay:
                counter = 0
                buttonPressed = False

        for i, annotation in enumerate(annotations):
            for j in range(len(annotation)):
                if j != 0:
                    cv2.line(imgCurrent, annotation[j - 1],
                             annotation[j], (0, 0, 200), 12)

        imgSmall = cv2.resize(img, (ws, hs))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:hs, w - ws: w] = imgSmall

        cv2.imshow("Slides", imgCurrent)
        cv2.imshow("Image", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break


def eye():
    import cv2
    import mediapipe as mp
    import pyautogui
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark

            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.008:
                print(left[0].y - left[1].y)
                pyautogui.click()
                pyautogui.sleep(0)
        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(980, 525)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 981, 560))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icons/tuse.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(280, 40, 491, 441))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("icons/gifloader.gif"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("gif")
        self.movie = QMovie("icons/gifloader.gif")
        self.label_2.setMovie(self.movie)
        self.movie.start()
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(790, 40, 150, 130))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("presentation/stop button.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 170, 241, 100))
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      "color:white;\n"
                                      "font: 16pt \"MS Shell Dlg 2\";\n"
                                      "}\n"
                                      "QPushButton::pressed{\n"
                                      "background-color:black;\n"
                                      "}")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 70, 231, 100))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
                                        "color:white;\n"
                                        "font: 16pt \"MS Shell Dlg 2\";\n"
                                        "}\n"
                                        "QPushButton::pressed{\n"
                                        "background-color:black;\n"
                                        "}")
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 260, 251, 125))
        self.pushButton_3.clicked.connect(presentation)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
                                        "color:white;\n"
                                        "font: 16pt \"MS Shell Dlg 2\";\n"
                                        "}\n"
                                        "QPushButton::pressed{\n"
                                        "background-color:black;\n"
                                        "}")
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 370, 241, 120))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
                                        "color:white;\n"
                                        "font: 16pt \"MS Shell Dlg 2\";\n"
                                        "}\n"
                                        "QPushButton::pressed{\n"
                                        "background-color:black;\n"
                                        "}")
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 470, 261, 71))
        self.pushButton_5.setStyleSheet("QPushButton{\n"
                                        "color:white;\n"
                                        "font: 16pt \"MS Shell Dlg 2\";\n"
                                        "}\n"
                                        "QPushButton::pressed{\n"
                                        "background-color:black;\n"
                                        "}")
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_4.clicked.connect(eye)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        now = datetime.datetime.now()
        self.pushButton.setText(_translate("Form", str(
            now.hour)+':'+str(now.minute)+':'+str(now.second)))
        date_object = datetime.date.today()
        self.pushButton_2.setText(_translate(
            "Form", str(date_object)))
        self.pushButton_3.setText(_translate("Form", "Presentation"))
        self.pushButton_4.setText(_translate("Form", "Eye Detector"))
        self.pushButton_5.setText(_translate("Form", "Malout"))


def _run_alexa():
    voice = Voice()
    voice.wishMe()
    while True:
        voice.run_alexa()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    t = threading.Thread(target=_run_alexa, name="name",)
    t.start()
    sys.exit(app.exec_())
