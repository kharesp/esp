from openalpr import Alpr
import cv2,time,imutils,glob,os,time,sys
import numpy as np
sys.path.append('src/vertices')
import opencv

#Performs license plate recognition on test image files using alpr library. Different image pre-processing techniques before ocr performs differently 
#Test image files, i.e., original_plates were downloaded from http://www.zemris.fer.hr/projects/LicensePlates/english/results.shtl

img_files=glob.glob('original_plates/*.jpg')
alpr=Alpr('us','/etc/openalpr/openalpr.conf','/home/pi/workspace/python/openalpr/runtime_data')
f=open('ocr_results.csv','w')
f.write('file,oocr,eh,ehocr,eht,ehtocr,ch,chocr,cht,chtocr,bf,bfocr,bft,bftocr,res1,res2,res3,res4,res5,res6,res7\n')

for idx,img_file in enumerate(sorted(img_files)):
  print('\nprocessing img:%d %s'%(idx,img_file))
  #read image
  img=cv2.imread(img_file)
  h,w,c=img.shape
  
  #resize image
  img=cv2.resize(img,(w//2,h//2))

  #convert to grey-scale
  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  #ocr on original grey-scale
  oocr_t1=time.time()
  res1=alpr.recognize_ndarray(gray)['results']
  oocr_t2=time.time()
  oocr_l=(oocr_t2-oocr_t1)*1000

  #equalize histogram
  eh_t1=time.time()
  eq_hist=cv2.equalizeHist(gray)
  eh_t2=time.time()
  eh_l=(eh_t2-eh_t1)*1000

  #ocr after histogram equalization 
  ehocr_t1=time.time()
  res2=alpr.recognize_ndarray(eq_hist)['results']
  ehocr_t2=time.time()
  ehocr_l=(ehocr_t2-ehocr_t1)*1000

  #threshold after equalize histogram
  eht_t1=time.time()
  eq_th=cv2.adaptiveThreshold(eq_hist,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
  eht_t2=time.time()
  eht_l=(eht_t2-eht_t1)*1000

  #ocr after histogram equalization and thresholding
  ehtocr_t1=time.time()
  res3=alpr.recognize_ndarray(eq_th)['results']
  ehtocr_t2=time.time()
  ehtocr_l=(ehtocr_t2-ehtocr_t1)*1000

  #clahe histogram
  ch_t1=time.time()
  clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
  clahe_hist=clahe.apply(gray)
  ch_t2=time.time()
  ch_l=(ch_t2-ch_t1)*1000

  #ocr after clahe histogram 
  chocr_t1=time.time()
  res4=alpr.recognize_ndarray(clahe_hist)['results']
  chocr_t2=time.time()
  chocr_l=(chocr_t2-chocr_t1)*1000

  #threshold after clahe histogram
  cht_t1=time.time()
  ch_th=cv2.adaptiveThreshold(clahe_hist,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
  cht_t2=time.time()
  cht_l=(cht_t2-cht_t1)*1000

  #ocr after clahe histogram and threshold
  chtocr_t1=time.time()
  res5=alpr.recognize_ndarray(ch_th)['results']
  chtocr_t2=time.time()
  chtocr_l=(chtocr_t2-chtocr_t1)*1000

  #bilateral filter
  bf_t1=time.time()
  bf=cv2.bilateralFilter(gray,5,150,150)
  bf_t2=time.time()
  bf_l=(bf_t2-bf_t1)*1000

  #ocr after bilateral filter
  bfocr_t1=time.time()
  res6=alpr.recognize_ndarray(bf)['results']
  bfocr_t2=time.time()
  bfocr_l=(bfocr_t2-bfocr_t1)*1000

  #threshold after bilateral filter 
  bft_t1=time.time()
  bf_th=cv2.adaptiveThreshold(bf,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
  bft_t2=time.time()
  bft_l=(bft_t2-bft_t1)*1000

  #ocr after bilateral filter and threshold
  bftocr_t1=time.time()
  res7=alpr.recognize_ndarray(bf_th)['results']
  bftocr_t2=time.time()
  bftocr_l=(bftocr_t2-bftocr_t1)*1000

  """
  #contrast stretching
  #contrast stretching takes too long and therefore has not been considered for further experiments 
  cs_t1=time.time()
  minmax_img=np.zeros((gray.shape[0],gray.shape[1]),dtype='uint8')
  min_val=np.min(gray)
  max_val=np.max(gray)
  for i in range(gray.shape[0]):
      for j in range(gray.shape[1]):
          minmax_img[i,j]=255*(gray[i,j]-min_val)/(max_val-min_val)
  cs=minmax_img
  cs_t2=time.time()
  cs_l=(cs_t2-cs_t1)*1000

  #ocr after contrast stretching
  csocr_t1=time.time()
  res6=alpr.recognize_ndarray(cs)['results']
  csocr_t2=time.time()
  csocr_l=(csocr_t2-csocr_t1)*1000

  #threshold after contrast stretching
  cst_t1=time.time()
  cs_th=cv2.adaptiveThreshold(cs,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
  cst_t2=time.time()
  cst_l=(cst_t2-cst_t1)*1000

  #ocr after contrast stretching and thresholding
  cstocr_t1=time.time()
  res7=alpr.recognize_ndarray(cs_th)['results']
  cstocr_t2=time.time()
  cstocr_l=(cstocr_t2-cstocr_t1)*1000
  """

  if any([len(x) for x in [res1,res2,res3,res4,res5,res6,res7]]):
    plates=['' if len(x)==0 else x[0]['plate'] for x in [res1,res2,res3,res4,res5,res6,res7]]
    to_write='%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%s,%s,%s,%s,%s,%s,%s\n'%(os.path.basename(img_file),\
      oocr_l,\
      eh_l,ehocr_l,eht_l,ehtocr_l,\
      ch_l,chocr_l,cht_l,chtocr_l,\
      bf_l,bfocr_l,bft_l,bftocr_l,\
      plates[0],plates[1],plates[2],plates[3],plates[4],plates[5],plates[6])
    f.write(to_write)

alpr.unload()
f.close()
