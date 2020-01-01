from openalpr import Alpr
import cv2,time,imutils,glob,os,time,sys
import numpy as np

img_files=glob.glob('ocr_plates/selected_plates/*.jpg')
alpr=Alpr('us','/etc/openalpr/openalpr.conf','/home/pi/workspace/python/openalpr/runtime_data')

for idx,img_file in enumerate(sorted(img_files)):
  #read image
  img=cv2.imread(img_file,0)
  h,w,c=img.shape
  
  #ocr on original grey-scale
  res1=alpr.recognize_ndarray(gray)['results']
  
  if len(res1)==0: 
    print('img:%s plate:'%(img_file))
  else:
    print('img:%s plate:%s'%(img_file,res1[0]['plate']))
