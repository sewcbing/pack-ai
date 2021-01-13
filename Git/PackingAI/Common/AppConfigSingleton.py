# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
from Common.Singleton import Singleton
__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class AppConfigSingleton(metaclass = Singleton):
    def __init__(self):
        self.__PatchValidationList = []
        self.__VisionIgnoredListFixed = []
        self.__SessionStartPoint = []
        self.__SessionContent = []
        self.__SessionEndPoint = []
        self.__FidInputRegExp = []

        DOMTree = xml.dom.minidom.parse("AppConfig.xml")
        collection = DOMTree.documentElement
        
        DEBUG = collection.getElementsByTagName("Debug")[0]
        self.__debugFlg = DEBUG.childNodes[0].data

        
        VALIDATION = collection.getElementsByTagName("PatchValidation")[0]
        content =  VALIDATION.getElementsByTagName("Interval")[0]
        self.__PatchValidationInterval = content.childNodes[0].data
        content =  VALIDATION.getElementsByTagName("Picture")[0]
        self.__PatchValidationPicture = content.childNodes[0].data
        for items in VALIDATION.getElementsByTagName("Item"):
            name = items.getElementsByTagName("Name")[0]
            value = items.getElementsByTagName("Value")[0]
            contet = (name.childNodes[0].data, value.childNodes[0].data)
            self.__PatchValidationList.append(contet)

        SESSION = collection.getElementsByTagName("SessionInfo")[0]

        content =  SESSION.getElementsByTagName("ErrorTolerance")[0]
        self.__sessionErrorTolerance = content.childNodes[0].data

        detectInfo = SESSION.getElementsByTagName("Detections")[0]
        for items in detectInfo.getElementsByTagName("Item"):
            name = items.getElementsByTagName("Name")[0]
            countRef = items.getElementsByTagName("CountRef")[0]
            contet = (name.childNodes[0].data, countRef.childNodes[0].data)
            self.__SessionContent.append(contet)

        endInfo = SESSION.getElementsByTagName("EndPoints")[0]
        for items in endInfo.getElementsByTagName("Item"):
            name = items.getElementsByTagName("Name")[0]
            countRef = items.getElementsByTagName("CountRef")[0]
            contet = (name.childNodes[0].data, countRef.childNodes[0].data)
            self.__SessionEndPoint.append(contet)

        MES = collection.getElementsByTagName("MES")[0]
        content =  MES.getElementsByTagName("U_FIO")[0]
        self.__UFioNum = content.childNodes[0].data
        content =  MES.getElementsByTagName("KFT_FIO")[0]
        self.__KTFFioNum = content.childNodes[0].data
        UART = MES.getElementsByTagName("UART")[0]
        Port = UART.getElementsByTagName("Port")[0]
        self.__UARTPort = Port.childNodes[0].data
        PortRate = UART.getElementsByTagName("PortRate")[0]
        self.__UARTPortRate = PortRate.childNodes[0].data
        TimeOut = UART.getElementsByTagName("TimeOut")[0]
        self.__UARTTimeout = TimeOut.childNodes[0].data
        
        CONFIG = collection.getElementsByTagName("YOLO_Config")[0]
        content =  CONFIG.getElementsByTagName("StructureFilePath")[0]
        self.__YoloConfigPath = content.childNodes[0].data
        content =  CONFIG.getElementsByTagName("WeightPath")[0]
        self.__YoloWeightPath = content.childNodes[0].data
        content =  CONFIG.getElementsByTagName("MetaPath")[0]
        self.__YoloMetaPath = content.childNodes[0].data
        content = CONFIG.getElementsByTagName("VisionIgnoreds")[0]
        for item in content.getElementsByTagName("Name"):
            self.__VisionIgnoredListFixed.append(item.childNodes[0].data)
        
        INPUT = collection.getElementsByTagName("FIDINPUT")[0]
        
        for item in INPUT.getElementsByTagName("RegExp"):
            self.__FidInputRegExp.append(item.childNodes[0].data)


    @property
    def yoloConfigPath(self):
        return self.__YoloConfigPath

    @property
    def yoloWeightPath(self):
        return self.__YoloWeightPath
    
    @property
    def yoloMetaPath(self):
        return self.__YoloMetaPath
    
    @property
    def sessionErrorTolerance(self):
        return self.__sessionErrorTolerance
    
    @property
    def sessionStartPointList(self):
        return self.__SessionStartPoint

    @property
    def sessionContentList(self):
        return self.__SessionContent

    @property
    def sessionEndPointList(self):
        return self.__SessionEndPoint

    @property
    def visionIgnoredListFixed(self):
        return self.__VisionIgnoredListFixed
    
    @property
    def fidInputRegularExpression(self):
        return self.__FidInputRegExp
    
    @property
    def debugFlg(self):
        return self.__debugFlg
    
    @property
    def UFIONumber(self):
        return self.__UFioNum

    @property
    def KFTFIONumber(self):
        return self.__KTFFioNum

    @property
    def patchValidationInterval(self):
        return self.__PatchValidationInterval

    @property
    def patchValidationPicture(self):
        return self.__PatchValidationPicture

    @property
    def patchValidationList(self):
        return self.__PatchValidationList

    @property
    def UARTPortName(self):
        return self.__UARTPort

    @property
    def UARTPortRate(self):
        return self.__UARTPortRate
    
    @property
    def UARTPortTimeOut(self):
        return int(self.__UARTTimeout)


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
