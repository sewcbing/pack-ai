# -*- coding: utf-8 -*-
from julesTk import view
from tkinter import *
import io
from PIL import Image
from PIL import ImageTk
from Common.AppConfigSingleton import AppConfigSingleton

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class ValidationView(view.View):
    def __init__(self, parent, controller):
        super(ValidationView, self).__init__(parent, controller)
        self.__appConfig = AppConfigSingleton()
        self.__entryWidgetList = []

    def _prepare(self):
        i = 1
        view.tk.Label(self, font=("黑体", 20), text= "请验证如下附件的版本号").grid(row = i, column = 1, columnspan = 3, sticky = "N")
        for item in self.__appConfig.patchValidationList:
            i += 1
            view.tk.Label(self, font=("黑体", 10), text= item[0], height=3, width=20).grid(row = i, column = 1, sticky = "E")
            entry = view.tk.Entry(self, font=("黑体", 10))
            entry.grid(row = i, column = 2, sticky = "E", pady=15)
            self.add_widget(item[0],entry)
            self.__entryWidgetList.append(entry)
        btn = view.tk.Button(self, font=("黑体", 20), text = "确认", height=3, width=5, command = self.buttonClicked)
        btn.grid(row = 1, rowspan = 5, column = 3, padx = 10)
        self.add_widget("button",btn)

        img = Image.open(self.__appConfig.patchValidationPicture)
        
        self.photo = ImageTk.PhotoImage(img.resize((500,500)))
        view.tk.Label(self,image=self.photo,bg="white").grid(row = 1,rowspan = 60, column = 4, padx = 10,pady = 10)

        self.__entryWidgetList[0].focus_set()
        for entry in self.__entryWidgetList:
            entry.bind("<Return>", self.enterKeyPressEvent)

    def enterKeyPressEvent(self, event):
        self.controller.switchFocus(self)

    def buttonClicked(self):
        self.controller.checkVersion(self)

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