import cv2
import numpy as np
from primesense import openni2
from primesense import _openni2 as c_api

class OpenniClass:
    def __init__(self,file_pass):
        openni2.initialize(file_pass)
        dev = openni2.Device.open_any()
        self.color_stream = dev.create_color_stream()
        self.color_stream.start()
        self.color_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, 
            resolutionX = 640, resolutionY = 480, fps = 30))
        
        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.start()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, 
            resolutionX = 640, resolutionY = 480, fps = 30))
            
    def color_update(self):
        frame = self.color_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint8)
        img.shape = (480, 640, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def depth_update(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        img.shape = (1, 480, 640)
        img1 = img.reshape(480,640,1)
        return img1
    
    def depth_update_(self,min,max):
        img = self.depth_update()
        float_ = np.zeros(img.shape[:2], dtype=np.float64)
        out = np.zeros(img.shape[:2], dtype=np.uint8)
        img[img<min] = min
        img[img>max] = min
        float_ = img.astype(np.float64)
        float_ = float_ - min
        float_ = ((max-min) - float_)/(max-min) * 255.0
        out = float_.astype(np.uint8)
        return out
    
    

    def destructor(self):
        openni2.unload()