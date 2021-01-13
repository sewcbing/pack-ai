# -*- coding: utf-8 -*-
import copy
from Common.Singleton import Singleton
from julesTk import ThreadSafeObject

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class VisionDetecedSingleton(ThreadSafeObject, metaclass = Singleton):
    def __init__(self):
        ThreadSafeObject.__init__(self)
        self.__detectedResult = []
        self.__ignoreItem = []
        
    def getFirstNode(self):
        return self.__detectedResult[0]
    
    @ThreadSafeObject.thread_safe
    def popFromPooling(self):
        if len(self.__detectedResult) is 0:
            return None
        return self.__detectedResult.pop(0)
    
    @ThreadSafeObject.thread_safe
    def pushToPooling(self, result):
        if not isinstance(result,list):
            raise ValueError("Expected a list value, not {}".format(type(result)))
        self.__detectedResult.append(result)

    @ThreadSafeObject.thread_safe
    def clearPooling(self):
        self.__detectedResult.clear()

    @ThreadSafeObject.thread_safe
    def fetchIgnoreContent(self):
        cpy = copy.deepcopy(self.__ignoreItem)
        return cpy

    @ThreadSafeObject.thread_safe
    def setIgnoreContent(self, name):
        if not isinstance(name,str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        if name in self.__ignoreItem:
            return
        self.__ignoreItem.append(name)
    
    @ThreadSafeObject.thread_safe
    def clearIgnoreContent(self):
        self.__ignoreItem = []

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