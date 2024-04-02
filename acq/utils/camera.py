

import nidaqmx
import numpy as np
import cv2


import acq


class Camera:

    def __init__(self, savepath, use_trig=False, cam_id=0):

        self.cam_id = cam_id
        self.savepath = savepath
        self.use_trig = use_trig

        self.preview = True

        self.began_acq = False


    def cam_startup(self):

        self.cap = cv2.VideoCapture(self.cam_id)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(
            self.savepath,
            fourcc,
            60.0,
            (640, 480)
        )

        self.timestamps = []


    def capture(self):

        while self.cap.isOpened():

            frame_ret, frame = self.cap.read()

            if not frame_ret:

                print("Can't receive frame (stream end?). Exiting ...")
                break

            elif frame_ret:

                self.timestamps.append(self.cap.get(cv2.CAP_PROP_POS_MSEC))

            # horizontal & vertical flip
            frame = cv2.flip(frame, -1)

            self.out.write(frame)

            if self.preview is True:
                cv2.imshow('CameraFrame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

        
    def preview(self):
        # preview the camera feed without recording, TTL, etc.

        self.cap = cv2.VideoCapture(self.cam_id)

        while self.cap.isOpened():
                
            ret, frame = self.cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            elif ret:

                # horizontal & vertical flip
                frame = cv2.flip(frame, -1)

                cv2.imshow('CameraFrame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

    def record(self):

        self.cam_startup()

        if self.use_trig is True:
            acq.wait_for_trig()

        self.capture()

