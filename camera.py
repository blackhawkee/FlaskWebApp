import base64
import os

import cv2
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

    def get_frame_string(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)
        return base64.b64encode(jpeg.tobytes())

        # return np.array(jpeg.tobytes).tostring()

    def get_frame_file(self):
        ret, frame = self.video.read()
        directory = 'temp/'

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        # ret, jpeg = cv2.imwrite('test.png', frame)
        img_name = "{}{}.png".format('test', 1)
        cv2.imwrite(os.path.join(directory, img_name), frame)
        print("{} written!".format(img_name))
        return 'temp/' + img_name

        # return np.array(jpeg.tobytes).tostring()