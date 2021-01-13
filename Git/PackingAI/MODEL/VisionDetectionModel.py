# -*- coding: utf-8 -*-
from julesTk import model
import threading
import time
from cv2 import cv2
import copy
from PIL import Image, ImageTk, ImageFont, ImageDraw
from MODEL.yolo import darknet
import numpy as np

from Common.AppConfigSingleton import AppConfigSingleton
from Common.VisionDetecedSingleton import VisionDetecedSingleton
__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class VisionDetectionModel(model.Model, threading.Thread):
    def __init__(self):
        super(VisionDetectionModel, self).__init__()
        self.daemon = True

        self.__appConfigSingleton = AppConfigSingleton()
        self.__visDetctRstSingleton = VisionDetecedSingleton()

        self.netMain = darknet.load_net_custom(self.__appConfigSingleton.yoloConfigPath.encode(
            "ascii"), self.__appConfigSingleton.yoloWeightPath.encode("ascii"), 0, 1)  
        self.metaMain = darknet.load_meta(self.__appConfigSingleton.yoloMetaPath.encode("ascii"))

        #camera open and configuration
        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture("MODEL/yolo/test.mp4")
        #self.cap = cv2.VideoCapture("MODEL/yolo/test.webm")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS,30)
        self.cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))

        # Create an image we reuse for each detect
        self.darknet_image = darknet.make_image(darknet.network_width(self.netMain),
                                       darknet.network_height(self.netMain),3)
        self.__stopFlg = False
        self.__pauseFlg = True
        self.__font = ImageFont.truetype("./simsun.ttc", 20) #Song typeface
        
    @property
    def stopFlg(self):
        return self.__stopFlg
    
    @property
    def TypefaceFont(self):
        return self.__font

    @stopFlg.setter
    def stopFlg(self, value):
        self.__stopFlg = value
    
    @property
    def pauseFlg(self):
        return self.__pauseFlg

    @pauseFlg.setter
    @model.Model.thread_safe
    def pauseFlg(self, value):
        self.__pauseFlg = value

    def run(self):
        
        while(self.cap.isOpened()):
            if self.__stopFlg == True:
                print("Vision Detection model stopped")
                break
            
            ret, frame_read = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb,
                                        (darknet.network_width(self.netMain), darknet.network_height(self.netMain)),
                                        interpolation=cv2.INTER_LINEAR)
                                        
                darknet.copy_image_from_bytes(self.darknet_image, frame_resized.tobytes())
                if self.pauseFlg == True:
                    detections = []
                else:
                    detections = darknet.detect_image(self.netMain, self.metaMain, self.darknet_image, thresh=0.9)

                frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)

                if len(detections) is not 0:
                    self.__visDetctRstSingleton.pushToPooling(detections)
                    ign_items = copy.deepcopy(self.__appConfigSingleton.visionIgnoredListFixed)
                    for item in self.__visDetctRstSingleton.fetchIgnoreContent():
                        if item not in ign_items:
                            ign_items.append(item)

                    image = self.cvDrawBoxes(detections, frame_resized, ign_items)
                    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    self.__imgDetected = ImageTk.PhotoImage(image=image)
                else:
                    image = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
                    self.__imgDetected = ImageTk.PhotoImage(image=image)

                self.notify_observers()
        self.cap.release()

    @model.Model.thread_safe
    def fetchDetectedPicture(self):
        return self.__imgDetected

    
    def convertBack(self, x, y, w, h):
        xmin = int(round(x - (w / 2)))
        xmax = int(round(x + (w / 2)))
        ymin = int(round(y - (h / 2)))
        ymax = int(round(y + (h / 2)))
        return xmin, ymin, xmax, ymax


    def cvDrawBoxes(self, detections, img, ign):
        for detection in detections:
            #print(detection[0].decode())
            if self.__appConfigSingleton.debugFlg == "OFF":
                if detection[0].decode() in ign:
                    #print(detection[0].decode() + " is ignored")
                    continue
            else:
                print(detection[0].decode())
                
            x, y, w, h = detection[2][0],\
                detection[2][1],\
                detection[2][2],\
                detection[2][3]
            xmin, ymin, xmax, ymax = self.convertBack(
                float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)

            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((xmin, ymin),  
                        detection[0].decode() + " [" + str(round(detection[1] * 100, 2)) + "]", 
                        font = self.TypefaceFont, fill = (0, 255, 0, 0))
            img = np.array(img_pil)

        return img
        
#The MIT License (MIT)Copyright (C) <2020> <Siemens (DI FA MF SEWC PU ENG3)>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
#and associated documentation files (the "Software"), to deal in the Software without restriction, 
#including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
#subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions 
#of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
#TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
#CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.