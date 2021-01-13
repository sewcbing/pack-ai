# -*- coding: utf-8 -*-
import threading
import time
import serial 
from Common.Singleton import Singleton
from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const
from MODEL.NumberCounterHelper import ComponentNumberCounterHelper, EndObjectNumberCounterHelper
from MODEL.webcall.webservice_snCheck import sncheck_result
from enum import Enum

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class APPSTUS(Enum):
    SESSION_STOPED = 1
    SESSION_PREPROCESS = 2
    SESSION_PROCESSING = 3
    SESSION_POSTPROCESS = 4
    SESSION_PREFINISHED = 5
    SESSION_ERROR = 6

class SessionStates(metaclass = Singleton):
    def ___init__(self):
        pass

    def Action(self, obj):
        from MODEL.StateMachineModel import StateMachineModel
        if not isinstance(obj, StateMachineModel):
            raise ValueError("Expected a StateMachineModel value, not {}".format(type(obj)))
    @property
    def State(self):
        raise NotImplementedError

class SessionStoped(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        self.__appConfigSingleton = AppConfigSingleton()
        pass

    @property
    def State(self):
        return APPSTUS.SESSION_STOPED    

    def Action(self, obj):
        super(SessionStoped, self).Action(obj)
        while (obj.isFidInputAvalible() == False):
            time.sleep(0.2)
        obj.cleanFidInputEvent()
        obj.changeSessionState(SessionPreProcess())
        obj.notify_observers()
            
class SessionPreProcess(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        self.__appConfigSingleton = AppConfigSingleton()
        pass
    
    @property
    def State(self):
        return APPSTUS.SESSION_PREPROCESS

    def Action(self, obj):
        super(SessionPreProcess, self).Action(obj)
        
        print("do sncheck U with FID {}".format(obj.fidInputString))
        #snCheck with obj.fidInputString
        # try:
        #     response = sncheck_result(obj.fidInputString,self.__appConfigSingleton.UFIONumber)
        #     if response.retStatus==True:
        #         print("success!!")
        #     else:
        #         raise RuntimeError("Interlock failed" + response.retMessage)
        # except:
        #     import traceback, sys
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #     exceptionInfo = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        #     obj.errorMessage = "sncheck失败 FID：" +  obj.fidInputString + "    FIO: " + self.__appConfigSingleton.UFIONumber + "\n" + exceptionInfo
        #     obj.changeSessionState(SessionError())
        #     obj.notify_observers()
        #     print("failed!!")
        #     return

        # print("send start signal to BarCode rooter, fid {}".format(obj.fidInputString))
        # #send "sit+Fid" to BCR, start signal
        # try:
        #     ser=serial.Serial(self.__appConfigSingleton.UARTPortName, 
        #                 self.__appConfigSingleton.UARTPortRate,
        #                 timeout=self.__appConfigSingleton.UARTPortTimeOut)
        #     ser.write(("\rsit+" + obj.fidInputString + '\r').encode("ASCII"))
        #     ser.close()
        #     print("success!!")
        # except:
        #     import traceback, sys
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #     exceptionInfo = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        #     obj.errorMessage = "发送开始信号 “SIT+FID” 失败 FID：" +  obj.fidInputString + "\n详细信息：" + exceptionInfo
        #     obj.changeSessionState(SessionError())
        #     obj.notify_observers()
        #     print("failed!!")
        #     return

        # obj.changeSessionState(SessionProcessing())
        obj.notify_observers()       

class SessionProcessing(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        self.__adjuster = ComponentNumberCounterHelper()
        pass
    
    @property
    def State(self):
        return APPSTUS.SESSION_PROCESSING

    def Action(self, obj):
        super(SessionProcessing, self).Action(obj)
        if obj.isFidInputAvalible() == True:
            obj.changeSessionState(SessionPreProcess())
            obj.notify_observers()
            self.__adjuster.reset()
            obj.cleanAllCheckedItemStatus()
            obj.cleanAllEndPointItemStatus()
            obj.cleanFidInputEvent()

        if obj.isAllCheckedItemStatusFinished() is True:
            obj.changeSessionState(SessionPostProcess())
            obj.notify_observers()
            self.__adjuster.reset()

        for item in self.__adjuster.caculate():
            if item.Flag == const.FINISHED:
                obj.setCheckedItemStatusByName(item.name, const.FINISHED)
                obj.notify_observers()
            if item.Flag == const.MULTI_OBJ_ERROR:
                obj.setCheckedItemStatusByName(item.name, const.MULTI_OBJ_ERROR)
                obj.errorMessage = "检测到多个" +  item.name
                obj.changeSessionState(SessionError())
                obj.notify_observers()
                self.__adjuster.reset()

class SessionPostProcess(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        self.__appConfigSingleton = AppConfigSingleton()
        pass
    
    @property
    def State(self):
        return APPSTUS.SESSION_POSTPROCESS

    def Action(self, obj):
        super(SessionPostProcess, self).Action(obj)
        
        print("send finish signal with FID {}".format(obj.fidInputString))
        try:
            ser=serial.Serial(self.__appConfigSingleton.UARTPortName, 
                        self.__appConfigSingleton.UARTPortRate,
                        timeout=self.__appConfigSingleton.UARTPortTimeOut)
            ser.write(("\rsit+\r").encode("ASCII"))
            ser.close()
            print("success!!")
        except:
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exceptionInfo = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            obj.errorMessage = "发送结束信号 “SIT+”失败 FID：" +  obj.fidInputString +" /n详细信息：" + exceptionInfo
            obj.changeSessionState(SessionError())
            obj.notify_observers()
            print("Failed!!")
            return
        
        time.sleep(0.5)

        print("do sncheck KFT with FID {}".format(obj.fidInputString))
        #snCheck KFT with obj.fidInputString
        try:
            response = sncheck_result(obj.fidInputString,self.__appConfigSingleton.KFTFIONumber)
            if response.retStatus==True:
                print("success!!")
            else:
                raise RuntimeError("Interlock failed" + response.retMessage)
        except:
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exceptionInfo = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            obj.errorMessage = "sncheck失败 FID：" +  obj.fidInputString + "    FIO: " + self.__appConfigSingleton.KFTFIONumber + "\n" + exceptionInfo
            obj.changeSessionState(SessionError())
            obj.notify_observers()
            print("failed!!")
            return
        time.sleep(0.5)

        print("send print label signal with FID {}".format(obj.fidInputString))
        try:
            ser=serial.Serial(self.__appConfigSingleton.UARTPortName, 
                        self.__appConfigSingleton.UARTPortRate,
                        timeout=self.__appConfigSingleton.UARTPortTimeOut)
            ser.write(("\rsikit+" + obj.fidInputString + '\r').encode("ASCII"))
            ser.close()
            print("success!!")
        except:
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exceptionInfo = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            obj.errorMessage = "发送结束信号 sikit+”失败 FID：" +  obj.fidInputString +" /n详细信息：" + exceptionInfo
            obj.changeSessionState(SessionError())
            obj.notify_observers()
            print("Failed!!")
            return

        obj.changeSessionState(SessionPreFinish())
        obj.notify_observers()

class SessionPreFinish(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        self.__adjuster = EndObjectNumberCounterHelper()
        from Common.VisionDetecedSingleton import VisionDetecedSingleton
        self.__visDetctRstSingleton = VisionDetecedSingleton()
        pass
    
    @property
    def State(self):
        return APPSTUS.SESSION_PREFINISHED

    def Action(self, obj):
        super(SessionPreFinish, self).Action(obj)

        while obj.isAllEndPointItemStatusFinished() is False:
            for item in self.__adjuster.caculate():
                if item.Flag == const.FINISHED:
                    obj.setEndPointItemStatusByName(item.name, const.FINISHED)
        self.__adjuster.reset()
        obj.cleanAllCheckedItemStatus()
        obj.cleanAllEndPointItemStatus()
        obj.changeSessionState(SessionStoped())
        obj.notify_observers()

class SessionError(SessionStates):
    def __init__(self):
        SessionStates.__init__(self)
        pass

    @property
    def State(self):
        return APPSTUS.SESSION_ERROR

    def Action(self, obj):
        super(SessionError, self).Action(obj)

        while (obj.isErrorMessageAvalible() == True):
            time.sleep(0.2)
        
        print("send finish signal with FID {}".format(obj.fidInputString))
        try:
            ser=serial.Serial(self.__appConfigSingleton.UARTPortName, 
                        self.__appConfigSingleton.UARTPortRate,
                        timeout=self.__appConfigSingleton.UARTPortTimeOut)
            ser.write(("\rsit+\r").encode("ASCII"))
            ser.close()
            print("success!!")
        except:
            pass
        obj.cleanAllCheckedItemStatus()
        obj.cleanAllEndPointItemStatus()
        obj.changeSessionState(SessionStoped())
        obj.notify_observers()


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