# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:06:25 2020

@author: z003nzbe
"""

from zeep import Client

def sncheck_result(fid, fio):    #fid:serial number, fio:terminal ID
    #define webservice detail
    webservice_url = "http://mesweb.sewc.siemens.com.cn/axis2/services/snCheck?wsdl"
    client = Client(webservice_url)
    #Namespace/Binding/functionname in wsdl,
    service = client.create_service('{http://com.siemens.make.webService.snCheck/}snCheckBinding',
                                    'http://mesweb.sewc.siemens.com.cn/axis2/services/snCheck/sit')
    
    #define request xml content
    request_xml = {'fid':fid, 'fio':fio, 'ebb_appl':'snCheck_python', 'ebb_appl_v':'2.0.0_WSDL1.10_python'}
    
    #got response from webservice
    response_xml = service.sit(**request_xml)
    
    return response_xml

if __name__ == '__main__':
    res = sncheck_result('V-J1A96767', '121')
    print(res)

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