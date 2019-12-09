import cv2,sys,base64
import numpy as np
sys.path.append('src/dag')
import vertex

def deserialize_img(img_str):
  b64=base64.b64decode(img_str)
  arr=np.fromstring(b64,dtype=np.uint8)
  img=cv2.imdecode(arr,0)
  return img

def serialize_img(img,encoding):
  en,encoded_img=cv2.imencode(encoding,img)
  b64=base64.b64encode(encoded_img)
  return b64.decode('ascii')

class GaussianBlur(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(GaussianBlur,self).__init__(vid,graph,upstream_operators)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.GaussianBlur(img,(15,15),0)
    res_str=serialize_img(res,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class MedianBlur(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(MedianBlur,self).__init__(vid,graph,upstream_operators)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.medianBlur(img,5)
    res_str=serialize_img(res,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class BilateralFilter(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(BilateralFilter,self).__init__(vid,graph,upstream_operators)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.bilateralFilter(img,3,75,75)
    res_str=serialize_img(res,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class GrayScale(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(GrayScale,self).__init__(vid,graph,upstream_operators)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    res_str=serialize_img(grey,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Resize(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(Resize,self).__init__(vid,graph,upstream_operators)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    h,w,l=img.shape
    res=cv2.resize(img,(w//2,h//2))
    res_str=serialize_img(res,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Threshold(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(Threshold,self).__init__(vid,graph,upstream_operators)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    #grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,2)
    res_str=serialize_img(thresh,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class CarDetect(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(CarDetect,self).__init__(vid,graph,upstream_operators)
    self.car_cascade=cv2.CascadeClassifier('cars.xml')
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    cars=self.car_cascade.detectMultiScale(img,1.1,1)
    for (x,y,w,h) in cars:
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    res_str=serialize_img(img,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Add(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(Add,self).__init__(vid,graph,upstream_operators)
    self.values_map={}
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    self.values_map[path]=deserialize_img(img_str)
    if len(self.values_map)==2:
      imgs=list(self.values_map.values())
      added_img=cv2.addWeighted(imgs[0],1,imgs[1],1,0)
      res_str=serialize_img(added_img,'.bmp')
      return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)
    else:
      return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,img_str)

class NoOp(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators):
    super(NoOp,self).__init__(vid,graph,upstream_operators)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res_str=serialize_img(img,'.bmp')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)
