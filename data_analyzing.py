import matplotlib.pyplot as plt
import numpy as np
import csv
import tool.wavfilter as wf

# with open('axis_test.csv', 'r') as csv_file:
with open('10_24__17_26.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data = []
    for row in csv_reader:
        num_array = [float(i) for i in row[:7]]
        if len(num_array) < 7:
            continue
        for i in range(4, 7):
             if num_array[i] > 180:
                 num_array[i] = num_array[i]-360
        data = data + num_array

data_array = np.array(data)
data_array = np.reshape(data_array, (-1, 7))

# get velocity
v_list = []
for i in range(1, len(data_array)):
    dt = (data_array[i, 0]-data_array[i-1, 0])/(10000.0*1000.0)
    v = [dt]
    v += [(data_array[i, j] - data_array[i - 1, j]) / dt for j in range(1, 4)]
    v += [(data_array[i, j] - data_array[i - 1, j]) / (dt * 6)for j in range(4, 7)] # degree/s to rpm
    v_list = v_list + v

v_array = np.array(v_list)
v_array = np.reshape(v_array, (-1, 7))

# plt.plot(v_array[:, 0], color='black')
gauss = wf.gaussFilter(11, 5)
# plt.plot(wf.calcFilter(v_array[:, 4], gauss), color='r')  # pitch
# plt.plot(wf.calcFilter(v_array[:, 5], gauss), color='g')  # yaw
# plt.plot(wf.calcFilter(v_array[:, 6], gauss), color='b')  # roll
# plt.plot(v_array[:, 4], color='r')  # pitch
# plt.plot(v_array[:, 5], color='g')  # yaw
# plt.plot(v_array[:, 6], color='b')  # roll
## -- ##
# plt.plot(data_array[:, 1], color='r')  # ??
# plt.plot(data_array[:, 2], color='g')  # ??
# plt.plot(data_array[:, 3], color='b')  # ??
plt.plot(data_array[:, 4], color='r')  # pitch
plt.plot(data_array[:, 5], color='g')  # yaw
plt.plot(data_array[:, 6], color='b')  # roll
plt.show()