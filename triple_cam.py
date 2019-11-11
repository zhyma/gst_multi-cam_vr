import cv2
from multiprocessing import Process
import time
import numpy as np
import os
from find_device import get_device

def send():
    width = 1280
    height = 360

    dev_pana, dev_webcam = get_device()
    print dev_pana,
    print dev_webcam

    cap_webcam = []
    for i in dev_webcam:
        cap_webcam.append(cv2.VideoCapture(
            'ksvideosrc device-index=' + str(i) + ' ! video/x-raw,width=640,height=360,framerate=30/1 ! decodebin ! videoconvert ! appsink'))
        # fps = cap_webcam.get(cv2.CAP_PROP_FPS)
        # print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    cap_pana = cv2.VideoCapture(
        'ksvideosrc device-index=' + str(dev_pana) + ' ! image/jpeg,width=1280,height=720,framerate=30/1 ! decodebin ! videoconvert ! appsink')
    fps = cap_pana.get(cv2.CAP_PROP_FPS)
    print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)

    out_send = cv2.VideoWriter(
        'appsrc! videoconvert ! video/x-raw,format=YUY2 ! jpegenc! rtpjpegpay ! udpsink host=127.0.0.1 port=5000 sync=false',
        cv2.CAP_GSTREAMER, 0, 25, (width, height))

    if not cap_pana.isOpened() or not out_send.isOpened():
        print('VideoCapture or VideoWriter not opened')
        exit(0)

    flag = 0
    while True:
        if flag == 0:
            ret, p_frame = cap_pana.read()
            frame = p_frame[178:p_frame.shape[0] - 182, 0:p_frame.shape[1]]
            out_send.write(frame)

        else:
            ret, w_frame = cap_webcam[flag-1].read()
            black = np.zeros((height, 320, 3), np.uint8)
            frame = np.concatenate((black, w_frame[0:w_frame.shape[0], 0:w_frame.shape[1]], black), axis=1)
            out_send.write(frame)

        if not ret:
            print('empty frame')
            break

        cv2.imshow('send', frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            if flag < len(cap_webcam):
                flag += 1
            else:
                flag = 0

    for i in cap_webcam:
        i.release()
    cap_pana.release()
    out_send.release()

if __name__ == '__main__':
    start_time = time.time()
    s = Process(target=send)
    # r = Process(target=receive)
    s.start()
    # r.start()
    s.join()
    # r.join()

    cv2.destroyAllWindows()
