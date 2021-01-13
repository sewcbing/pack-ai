# -*- coding: utf-8 -*-
from julesTk import model
import threading
from MODEL.SessionStates import SessionStates, SessionProcessing, SessionPreFinish, SessionStoped, SessionError,SessionPostProcess,SessionPreProcess,APPSTUS
from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const
from julesTk import ThreadSafeObject
from multiprocessing import Event

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class CheckItemRef():
    def __init__(self, name, state):
        if not isinstance(name, str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        if not isinstance(state, int):
            raise ValueError("Expected a string value, not {}".format(type(state)))

        self.__name = name
        self.__state = state
    
    @property
    def name(self):
        return self.__name
    
    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected a int value, not {}".format(type(value)))
        self.__state = value

class StateMachineModel(model.Model, threading.Thread):
    def __init__(self):
        super(StateMachineModel, self).__init__()
        self.daemon = True
        self._lock = threading.RLock()

        self.__fidInputString = "None"
        self.__errorMessage = "None"
        self.__States = APPSTUS.SESSION_STOPED
        self.__checkedItemStatusMap = {}
        self.__endItemStatusMap = {}
        self.__InputEvent = Event()

        self.__stopFlg = False
        self.__appConfigSingleton = AppConfigSingleton()
        self.__sessionStates = SessionStoped()

        for item in self.__appConfigSingleton.sessionContentList:
            self.__checkedItemStatusMap[item[0]] = CheckItemRef(item[0], const.NOT_FINISHED)

        for item in self.__appConfigSingleton.sessionEndPointList:
            self.__endItemStatusMap[item[0]] = CheckItemRef(item[0], const.NOT_FINISHED)


    def changeSessionState(self, obj):
        self.__sessionStates = obj
        if obj.__class__.__base__.__name__ is not "SessionStates":
            raise ValueError("Expected a subclass SessionStates value, not {}".format(type(obj)))
        self.States = obj.State

    def run(self):
        while 1:
            if self.__stopFlg == True:
                print("State Machine model stopped")
                break
            self.__sessionStates.Action(self)
    
    @property
    def checkedItemStatusMap(self):
        return self.__checkedItemStatusMap

    @model.Model.thread_safe
    def setCheckedItemStatusByName(self, name, value = const.NOT_FINISHED):
        try:
            self.checkedItemStatusMap[name].state = value

        except KeyError:
            raise ValueError("try to assign one unknow key")


    @model.Model.thread_safe
    def setAllCheckedItemStatusFinished(self):
        for key in self.checkedItemStatusMap.keys():
            self.checkedItemStatusMap[key].state = const.FINISHED

    def isAllCheckedItemStatusFinished(self):
        ret = True
        for item in self.checkedItemStatusMap.items():
            if item[1].state is not const.FINISHED:
                ret = False
                break
        return ret

    @model.Model.thread_safe
    def cleanAllCheckedItemStatus(self):
        for key in self.checkedItemStatusMap.keys():
            self.checkedItemStatusMap[key].state = const.NOT_FINISHED
        
    @property
    def endPointItemStatusMap(self):
        return self.__endItemStatusMap

    @model.Model.thread_safe
    def setEndPointItemStatusByName(self, name, value = const.NOT_FINISHED):
        try:
            self.endPointItemStatusMap[name].state = value

        except KeyError:
            raise ValueError("try to assign one unknow key")


    @model.Model.thread_safe
    def setAllEndPointItemStatusFinished(self):
        for key in self.endPointItemStatusMap.keys():
            self.endPointItemStatusMap[key].state = const.FINISHED

    def isAllEndPointItemStatusFinished(self):
        ret = True
        for item in self.endPointItemStatusMap.items():
            if item[1].state is not const.FINISHED:
                ret = False
                break
        return ret

    @model.Model.thread_safe
    def cleanAllEndPointItemStatus(self):
        for key in self.endPointItemStatusMap.keys():
            self.endPointItemStatusMap[key].state = const.NOT_FINISHED
    
    @property
    def fidInputString(self):
        return self.__fidInputString

    @fidInputString.setter
    @model.Model.thread_safe
    def fidInputString(self,obj):
        if not isinstance(obj, str):
            raise ValueError("Expected a str value, not {}".format(type(obj)))
        self.__fidInputString = obj
        self.__InputEvent.set()
    
    def cleanFidInputEvent(self):
        self.__InputEvent.clear()

    def isFidInputAvalible(self):
        return self.__InputEvent.wait(0.1)


    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    @model.Model.thread_safe
    def errorMessage(self,obj):
        if obj is None:
            obj = "None"
        if not isinstance(obj, str):
            raise ValueError("Expected a str value, not {}".format(type(obj)))
        self.__errorMessage = obj
    
    def cleanErrorMessage(self):
        self.errorMessage = "None"
       
    def isErrorMessageAvalible(self):
        return self.errorMessage != "None"

    @property
    def States(self):
        return self.__States 
    
    @States.setter
    @model.Model.thread_safe
    def States(self, num):
        if not isinstance(num, APPSTUS):
            raise ValueError("Expected a APPSTUS value, not {}".format(type(num)))
        self.__States = num

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