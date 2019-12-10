import cv2,sys,base64
#from openalpr import Alpr
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
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(GaussianBlur,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.GaussianBlur(img,(15,15),0)
    res_str=serialize_img(res,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class MedianBlur(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(MedianBlur,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.medianBlur(img,5)
    res_str=serialize_img(res,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class BilateralFilter(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(BilateralFilter,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)

  def vfunction(self,update):
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res=cv2.bilateralFilter(img,5,75,75)
    res_str=serialize_img(res,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class GrayScale(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(GrayScale,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    res_str=serialize_img(grey,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Resize(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Resize,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    h,w,l=img.shape
    res=cv2.resize(img,(w//2,h//2))
    res_str=serialize_img(res,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Threshold(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Threshold,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    #grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,2)
    res_str=serialize_img(thresh,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class CarDetect(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(CarDetect,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.car_cascade=cv2.CascadeClassifier('cars.xml')
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    cars=self.car_cascade.detectMultiScale(img,1.1,1)
    for (x,y,w,h) in cars:
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    res_str=serialize_img(img,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Add(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Add,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.values_map={}
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    self.values_map[path]=deserialize_img(img_str)
    if len(self.values_map)==2:
      imgs=list(self.values_map.values())
      added_img=cv2.addWeighted(imgs[0],1,imgs[1],1,0)
      res_str=serialize_img(added_img,'.jpg')
      return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)
    else:
      return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,img_str)

class NoOp(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(NoOp,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    res_str=serialize_img(img,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class Bogus(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Bogus,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
  
  def fib(self,count): 
    def compute(n):
      if n<=1:
        return n
      else:
        return fib(n-1)+fib(n-2)
    return compute(count)

  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    for i in range(5):
      self.fib(22)
    res_str=serialize_img(img,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class EqHist(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(EqHist,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    eq_hist=cv2.equalizeHist(img)
    res_str=serialize_img(eq_hist,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class ClaheHist(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(ClaheHist,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    clahe_hist=clahe.apply(img)
    res_str=serialize_img(clahe_hist,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)

class LPR(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(LPR,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.alpr=Alpr('us','/etc/opanalpr/openalpr.conf','/home/pi/workspace/python/openalpr/runtime_data')
  
  def clean_up(self):
    alpr.unload()

  def vfunction(self,update): 
    code,idx,ts,path,img_str=update.split(',')
    img=deserialize_img(img_str)
    results=alpr.recognize_ndarray(img)['results']
    recognized_lps=''
    if len(results)>0:
      for plate in results:
        license_number=plate['plate']
        coords=plate['coordinates']
        x=[coord['x'] for coord in coords]
        y=[coord['y'] for coord in coords]
        recognized_lp+='%s;%d;%d;%d;%d/'%(license_number,min(x),max(x),min(y),max(y))
    
    res_str=serialize_img(img,'.jpg')
    return '%s,%s,%s,%s-%s,%s,%s'%(code,idx,ts,path,self.vid,res_str,recognized_lps)

class Segment(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Segment,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
 
  def vfunction(self,update): 
    parts=update.split(',')
    code,idx,ts,path,img_str=parts[0],parts[1],parts[2],parts[3],parts[4]
    img=deserialize_img(img_str)
    if len(parts)==6:
      plates=parts[-1].split('/')
      for plate in plates:
        lp,min_x,max_x,min_y,max_y=plate.split(';')
        seg=img[min_y:max_y+1,min_x:max_x+1] 
        cv2.imwrite('%s/%s_%s.jpg'%(self.log_dir,lp,path),seg)
        cv2.rect(img,(min_x,min_y),(max_x,max_y),(255,0,0),3)
    else:
      #dummy load since no license plates were found
      h,w=img.shape()
      min_y=h//2
      max_y=min_y+50
      min_x=w//2
      max_x=min_x+100
      seg=img[min_y:max_y+1,min_x:max_x+1] 
      cv2.imwrite('%s/none_%s.jpg'%(self.log_dir,path),seg)
      cv2.rect(img,(min_x,min_y),(max_x,max_y),(255,0,0),3)

    res_str=serialize_img(img,'.jpg')
    return '%s,%s,%s,%s-%s,%s'%(code,idx,ts,path,self.vid,res_str)
