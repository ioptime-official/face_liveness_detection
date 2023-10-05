from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
from modules.list_random import output_list
import numpy as np
import sys
from PyQt5.QtCore import Qt

class StartPage(QDialog):
    def __init__(self):
        super(StartPage, self).__init__()
        loadUi("app_pages\\liveness_start.ui", self)
        self.start.clicked.connect(self.start_clicked)
        self.pixmap = QPixmap('images\\0002_Detect-Spoofing-Attempts.png')
        scaled_pixmap = self.pixmap.scaled(self.start_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.start_image.setPixmap(scaled_pixmap)

    def start_clicked(self):
        LogIn_page = TestingPage()
        widget.addWidget(LogIn_page)
        widget.setCurrentWidget(LogIn_page)

class ResultPage(QDialog):
    def __init__(self):
        super(ResultPage, self).__init__()
        loadUi("app_pages\\liveness_tryagain.ui", self)
        self.return_2.clicked.connect(self.return_2_clicked)
        self.pixmap = QPixmap('images\\equipment-authorization.png')
        scaled_pixmap = self.pixmap.scaled(self.ver_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ver_image.setPixmap(scaled_pixmap)

    def return_2_clicked(self):
        start_page = StartPage()
        widget.addWidget(start_page)
        widget.setCurrentWidget(start_page)

class TestingPage(QDialog):
    def __init__(self):
        super(TestingPage, self).__init__()
        loadUi("app_pages\\liveness_main.ui", self)
        self.cap = cv2.VideoCapture(0)  # Open the default camera (change the index if needed)
        self.initialize_liveness_detection()

    def initialize_liveness_detection(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # Load liveness detection actions
        self.actions = output_list()
        self.current_action_index = 0

        # Start the camera feed
        self.start_camera()

    def start_camera(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 30)  # Update at approximately 30 FPS

    def stop_camera(self):
        self.cap.release()
        self.timer.stop()

    def success(self):
        self.stop_camera()
        LogIn_page = ResultPage()
        widget.addWidget(LogIn_page)
        widget.setCurrentWidget(LogIn_page)

    def update_frame(self):
        ellipse_center = (320, 240)  # Center coordinates (x, y)
        ellipse_semiaxes = (160, 130)  # Semiaxes (a and b)
        ellipse_angle = 90
        
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mask = np.zeros_like(frame, dtype=np.uint8)
            cv2.ellipse(mask, ellipse_center, ellipse_semiaxes, ellipse_angle, 0, 360, (255, 255, 255), -1) 
            frame= cv2.bitwise_and(frame, mask)
                # Also convert the color space from BGR to RGB
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            results = self.face_mesh.process(frame)
            frame.flags.writeable = True

            ########
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            img_h, img_w, img_c = frame.shape
            face_3d = []
            face_2d = []
            actions = self.actions
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                            # Get the 2D Coordinates
                            face_2d.append([x, y])

                            # Get the 3D Coordinates
                            face_3d.append([x, y, lm.z])       
                    
                    # Convert it to the NumPy array
                    face_2d = np.array(face_2d, dtype=np.float64)

                    # Convert it to the NumPy array
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # The camera matrix
                    focal_length = 1 * img_w

                    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                            [0, focal_length, img_w / 2],
                                            [0, 0, 1]])

                    # The distortion parameters
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                
                    # See where the user's head tilting
                    if y < -10:
                        text = "Look Left"
                    elif y > 10:
                        text = "Look Right"
                    elif x < -10:
                        text = "Look Down"
                    elif x > 10:
                        text = "Look Up"
                    else:
                        text = "Look Forward"

                    # Display the nose direction
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y * 10) , int(nose_2d[1] - x * 10))
                    #cv2.line(frame, p1, p2, (255, 0, 0), 3)

                    #####

                    if self.current_action_index < len(actions):
                        self.current_action = self.actions[self.current_action_index]
                        self.actions_label.setText(self.current_action)
                       # cv2.putText(image, "Required action: " + self.current_action, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                        if text.lower() == self.current_action.lower():
                            #Shuffling should be here
                            
                            self.current_action_index += 1  # Move to the next action

                            if self.current_action_index < len(self.actions):
                                # Display the next action
                                next_action = actions[self.current_action_index]
                    else:
                            self.success()

              # Convert to RGB format
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.camera_tag.setPixmap(pixmap)

    def closeEvent(self, event):
        self.stop_camera()

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = StartPage()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(680)
widget.show()
sys.exit(app.exec_())