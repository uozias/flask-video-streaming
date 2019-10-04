import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    full_width = 0
    full_height = 0
    div = 0.2
    size =  (200, 200)
    quality = 30
   
    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        Camera.full_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH) 
        Camera.full_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
      
        Camera.size = (int(Camera.full_width * Camera.div), int(Camera.full_height * Camera.div))

        while True:
            # read current frame
            _, img = camera.read()

            #Create Half Size Image
            #new_img = cv2.resize(img, dsize=Camera.size)

            # encode as a jpeg image and return it
            img = cv2.resize(img,Camera.size)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), Camera.quality]
            yield cv2.imencode('.jpg', img, encode_param)[1].tobytes()
