import os

def get_device():
    cam_info = os.popen('gst-device-monitor-1.0 Video/Source').read().split('\n')

    cam_idx = 0
    cam_web = []
    cam_pana = -1
    for line in cam_info:
        if line[1:5]=='name':
            if line[9:14]=='Jabra':
                cam_pana = cam_idx
                print line[9:],
                print cam_idx
            elif line[9:17]=='Logitech':
                cam_web.append(cam_idx)
                print line[9:],
                print cam_idx

            cam_idx+=1

    return cam_pana, cam_web

if __name__=='__main__':
    print get_device()