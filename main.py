import cv2
from multiprocessing import Process
import time
import numpy as np
import os
import data_record as dr
import video_stream as vs

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from tool.calc3d import rotation, new_axis
from tool.arrow import Arrow3D

from matplotlib import animation
import time


if __name__ == '__main__':
    ip_addr = '127.0.0.1'
    start_time = time.time()

    v_thread = vs.videoThread(0, 'videoT', ip_addr)
    v_thread.start()

    d_thread = dr.dataThread(1, 'dataT', ip_addr)
    d_thread.start()
