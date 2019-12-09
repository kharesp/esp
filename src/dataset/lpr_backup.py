from openalpr import Alpr
import cv2,time,imutils,glob,os,time,sys
import numpy as np
sys.path.append('src/vertices')
import opencv


#timg='selected_license_plates/P6040055.jpg'
img_files=glob.glob('original_plates/*.jpg')
alpr=Alpr('us','/etc/openalpr/openalpr.conf','/home/pi/workspace/python/openalpr/runtime_data')

for idx,img_file in enumerate(sorted(img_files)):
  #print('\n\n For image:%d %s'%(idx,img_file))
#for idx in range(1000):
  img=cv2.imread(img_file)
  #img=cv2.imread(img_file)
  h,w,c=img.shape
  #print('original img shape:')
  #print(img.shape)

  img=cv2.resize(img,(w//2,h//2))
  #print('Resized img shape:')
  #print(img.shape)

  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ##contrast stretching
  #minmax_img=np.zeros((gray.shape[0],gray.shape[1]),dtype='uint8')
  #min_val=np.min(gray)
  #max_val=np.max(gray)
  #for i in range(gray.shape[0]):
  #    for j in range(gray.shape[1]):
  #        minmax_img[i,j]=255*(gray[i,j]-min_val)/(max_val-min_val)
  #contrast_stretched=minmax_img

  ##equalize histogram
  #eq_hist=cv2.equalizeHist(gray)

  ##clahe histogram
  #clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
  #clahe_hist=clahe.apply(gray)

  #th=cv2.adaptiveThreshold(eq_hist,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  #t1=time.time()
  #res1=alpr.recognize_ndarray(eq_hist)['results']
  #t2=time.time()
  #rt1=(t2-t1)*1000
  #
  #t1=time.time()
  #res2=alpr.recognize_ndarray(th)['results']
  #t2=time.time()
  #rt2=(t2-t1)*1000

  #if len(res1)>0:
  #    print('img:%s plate:%s time:%f'%(img_file,res1[0]['plate'],rt1))
  #if len(res2)>0:
  #    print('with thresholding-img:%s plate:%s time:%f'%(img_file,res2[0]['plate'],rt2))
  t1=time.time()
  gray=cv2.bilateralFilter(gray,5,150,150)
  t2=time.time()
  bfl=(t2-t1)*1000
  #th=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  #gray=cv2.GaussianBlur(gray,(15,15),0)
  #gray=cv2.medianBlur(gray,5)
  #print('Gray-scale shape:')
  #print(gray.shape)

  #t1=time.time()
  #img_str=opencv.serialize_img(gray,'.jpg')
  #t2=time.time()
  #print('Serialize img:%f'%((t2-t1)*1000))

  #t1=time.time()
  #img_c=opencv.deserialize_img(img_str)
  #t2=time.time()
  #print('De-Serialize img:%f'%((t2-t1)*1000))

  #t1=time.time()
  #edge=cv2.Canny(gray,30,200)
  #t2=time.time()
  #print('Edge detection:%f'%((t2-t1)*1000))

  #t1=time.time()
  #cnts=cv2.findContours(edge.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  #cnts=imutils.grab_contours(cnts)
  #cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:10]
  #lpCnt=None
  #found=False

  #for c in cnts:
  #  peri=cv2.arcLength(c,True)
  #  approx=cv2.approxPolyDP(c,0.018*peri,True)
  #  if len(approx)==4:
  #    lpCnt=approx
  #    found=True
  #    break

  #if not found:
  #  continue
  #
  #t1=time.time()
  #mask=np.zeros(gray.shape,np.uint8)
  #new_img=cv2.drawContours(mask,[lpCnt],0,255,-1)
  #new_img=cv2.bitwise_and(img,img,mask=mask)
  #(x, y) = np.where(mask == 255)
  #(topx, topy) = (np.min(x), np.min(y))
  #(bottomx, bottomy) = (np.max(x), np.max(y))
  #cropped = gray[topx:bottomx+1, topy:bottomy+1]
  #t2=time.time()
  #print('segmenting:%f'%((t2-t1)*1000))

  #cropped=cv2.adaptiveThreshold(cropped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
  t1=time.time()
  res1=alpr.recognize_ndarray(gray)
  t2=time.time()
  rt1=(t2-t1)*1000
  if len(res1['results'])>0:
      plate_str=res1['results'][0]['plate']
      coords=res1['results'][0]['coordinates']
      x=[coord['x'] for coord in coords]
      y=[coord['y'] for coord in coords]
      t1=time.time()
      cropped=gray[min(y):max(y)+1,min(x):max(x)+1]
      print(max(y)-min(y))
      print(max(x)-min(x))
      t2=time.time()
      print('time to draw rect:%f\n'%((t2-t1)*1000))
   

      #print('img:%s plate:%s time:%f bfl:%f'%(img_file,res1[0]['plate'],rt1,bfl))

  """
  t1=time.time()
  res2=alpr.recognize_ndarray(contrast_stretched)['results']
  t2=time.time()
  rt2=(t2-t1)*1000

  t1=time.time()
  res3=alpr.recognize_ndarray(eq_hist)['results']
  t2=time.time()
  rt3=(t2-t1)*1000

  t1=time.time()
  res4=alpr.recognize_ndarray(clahe_hist)['results']
  t2=time.time()
  rt4=(t2-t1)*1000
  #print('OCR:%f'%((t2-t1)*1000))

  #if len(res['results'])>0:
  #    print('THIS ONE!!!!')
  #    print('%d %s'%(idx,img_file))
  #    print(res['results'])
  #if len(res['results'])==0:
  #    print(img_file)
  if len(res1)>0 and len(res2)>0 and len(res3)>0 and len(res4)>0:
    print('\n'+img_file)
    if len(res1)>0:
        print('original:%s time:%f'%(res1[0]['plate'],rt1))
    else:
        print('original:  time:%f'%(rt1))

    if len(res2)>0:
        print('contrast_stretched:%s time:%f'%(res2[0]['plate'],rt2))
    else:
        print('contrast_stretched:  time:%f'%(rt2))

    if len(res3)>0:
        print('eq_hist:%s time:%f'%(res3[0]['plate'],rt3))
    else:
        print('eq_hist:  time:%f'%(rt3))

    if len(res4)>0:
        print('clahe_hist:%s time:%f'%(res4[0]['plate'],rt4))
    else:
        print('clahe_hist:  time:%f'%(rt4))
  """
alpr.unload()
