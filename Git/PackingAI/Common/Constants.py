# -*- coding: utf-8 -*-
__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class Constants():
    class ConstError(TypeError): pass

    class ConstCaseError(ConstError): pass

    def __setattr__(self, key, value):
        print()
        if key in self.__dict__.keys():
            # 存在性验证
            raise self.ConstError("Can't change a const variable: '%s'" % key)

        if not key.isupper():
            # 语法规范验证
            raise self.ConstCaseError("Const variable must be combined with upper letters:'%s'" % key)

        self.__dict__[key] = value

const = Constants()

const.NOT_START_COLOR = "black"
const.NOT_START_STRING = " 未开始"

const.PREPROCESS_COLOR = "green"
const.PREPROCESS_STRING = " MES通信中..."

const.PROCESSING_COLOR = "green"
const.PROCESSING_STRING = " 检测中..."

const.POSTPROCESS_COLOR = "green"
const.POSTPROCESS_STRING = " MES通信中..."

const.PREFINISH_COLOR = "green"
const.PREFINISH_STRING = " 探测包装结束..."

const.ERROR_COLOR = "red"
const.ERROR_STRING = " 出错"

const.ITEM_RESET_COLOR = "white"
const.ITEM_FINISHED_COLOR = "green"
const.ITEM_ERROR_COLOR = "red"

const.NOT_FINISHED = 0
const.FINISHED = 1
const.ERROR = 2
const.MULTI_OBJ_ERROR = 3

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