## BackGround

The current general scheme for manual packaging sites is nothing more than neglecting to check the packaging results or counting based on sensors to prevent misoperation. The above two schemes have the following disadvantages.

- For the scheme that directly ignores the inspection, every operation of the employees will have the possibility of less or more release, which increases the maintenance cost of the product and reduces the standardization of the product listing. At the same time, it brings inconvenience to end users.
- For the sensor-based counting solution, every employee needs to scan every attachment every time, which increases the difficulty of the operation and the total production time for the employee.

To fulfilling those two issues, we Solemnly introduced  this artificial intelligence project(mentiond with PackingAI on the following document). 

## General Introduction

The software consists of two parts. The first part is the weight file of deep learning and related modules (dlls, so etc.) of deep learning, and the second part is general structure software.

For the first part, the weight file of deep learning is the result file trained for specific application scenarios, and the deep learning related module are modules for loading and using the weight file. After the weight file is loaded by the relevant module of deep learning, a specific data stream can be identified for this specific scenarios.

the software is base on JulesTk which is an opensource MVC framework in python. the software have the following functionality:

 1. interpretate the configration file "AppConfig.xml" and show them on GUI.
 2. handle the whole process.
 3. show realtime vedio of operation.
 4. error report.

## Requirements

- Intel CPU i5 or above
- Windows 10 operation system
- Nvidia GTx 2060 or above
- CUDA 10.0
- CUDNN 7.6.5
- python 3.7 or above

## Install process

***some of the install packages could be found on share folder \\\\cnctu04211\departments\SEWC_Shared_Folder\002 PU\08 ERFA Team Folder\05 AI & Data analysis\AI software-YOLO ***

1. install python 3.7 or above. add the installed path into the OS environment. access https://www.python.org/ for more information.
2. install CUDA 10.0. access https://developer.nvidia.com/cuda-downloads for mor information.
3. install CUDNN 7.6.5. access https://docs.nvidia.com/deeplearning/cudnn/install-guide/ for mor information.
4. download code from https://code.siemens.com/jinsong.chen/packingai. or clone code with git.  

>- 4.1 clone code from https://code.siemens.com/jinsong.chen/packingai(optional) 
>>>a. install git, access more information from https://git-scm.com/  
>>>b. open terminal through git.  
>>>c. run command "ssh-keygen.exe" on terminal  
>>>d. update your publickey to "code.siemens.com"  
>>>e. clone code with command "git clone git@code.siemens.com:YOURNAME/packingai.git"  

5. upload "yolov4-hmi-packing.weight" file to your local project "YOUR_PROJECT_LOCATION/MODEL\yolo\config".  
6. test yolo environment with command "python YOUR_PROJECT_LOCATION/MODEL/yolo/darknet_video.py". when everything about yolo is ready, you will see the realtime video on your monitor.  
7. upload julesTK-pictched2020.zip to your computer. and unzip it then run command "python setup.py install" to install julesTK.
8. install the following python package through command "pip install ...":
>> opencv-python  
>> pillow  
>> pyserial  
>> zeep  

9. run command "python YOUR_PROJECT_LOCATION/PackingAI.py" to run the software.
