import threading
import cv2
import os
import numpy as np
from find_device import get_device

class videoThread(threading.Thread):
    def __init__(self, threadID, name, ip_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.t = 0
        self.width = 1280
        self.height = 360

        dev_pana, dev_webcam = get_device()
        print dev_pana,
        print dev_webcam

        self.cap_webcam = []
        for i in dev_webcam:
            self.cap_webcam.append(cv2.VideoCapture(
                'ksvideosrc device-index=' + str(i) + ' ! video/x-raw,width=640,height=360,framerate=30/1 ! decodebin ! videoconvert ! appsink'))
            # fps = cap_webcam.get(cv2.CAP_PROP_FPS)
            # print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
        self.cap_pana = cv2.VideoCapture(
            'ksvideosrc device-index=' + str(dev_pana) + ' ! image/jpeg,width=1280,height=720,framerate=30/1 ! decodebin ! videoconvert ! appsink')
        fps = self.cap_pana.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)

        self.out_send = cv2.VideoWriter(
            'appsrc! videoconvert ! video/x-raw,format=YUY2 ! jpegenc! rtpjpegpay ! udpsink host=127.0.0.1 port=5000 sync=false',
            cv2.CAP_GSTREAMER, 0, 25, (self.width, self.height))

        if not self.cap_pana.isOpened() or not self.out_send.isOpened():
            print('VideoCapture or VideoWriter not opened')
            exit(0)

        self.running = True

    def run(self):
        flag = 0
        print 'video is up'
        while self.running:
            if flag == 0:
                ret, p_frame = self.cap_pana.read()
                frame = p_frame[178:p_frame.shape[0] - 182, 0:p_frame.shape[1]]
                self.out_send.write(frame)

            else:
                ret, w_frame = self.cap_webcam[flag-1].read()
                black = np.zeros((self.height, 320, 3), np.uint8)
                frame = np.concatenate((black, w_frame[0:w_frame.shape[0], 0:w_frame.shape[1]], black), axis=1)
                self.out_send.write(frame)

            if not ret:
                print('empty frame')
                break

            cv2.imshow('send', frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('s'):
                if flag < len(self.cap_webcam):
                    flag += 1
                else:
                    flag = 0

        running = False
        self.cap_pana.release()
        for i in self.cap_webcam:
            i.release()
        self.out_send.release()
        cv2.destroyAllWindows()
        threading.Thread.exit()
