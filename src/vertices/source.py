import sys,glob,time,rx,cv2
sys.path.append('src/dag')
sys.path.append('src/rxzmq')
import vertex,opencv,rxzmq

class Source(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,data_dir,encoding,rate): 
    super(Source,self).__init__(vid,graph,upstream_operators)
    self.data_dir=data_dir
    self.encoding=encoding
    self.rate=rate
    self.sleep_interval_s=1.0/self.rate

  def publish(self):
    def _publish(observer,scheduler=None):
      try:
        img_files=glob.glob('%s/*%s'%(self.data_dir,self.encoding))
        for idx,img_file in enumerate(sorted(img_files)):
          img=cv2.imread(img_file)
          img_str=opencv.serialize_img(img,self.encoding)
          msg_str='%d,%d,%f,%s,%s'%(rxzmq.MSG_TYPE_DATA,\
            idx,time.time(),self.vid,img_str)
          observer.on_next(msg_str)
          time.sleep(self.sleep_interval_s)
          if idx==100:
            break
        observer.on_completed()
      except Exception as err:
        observer.on_error(err)
    return rx.Observable(_publish)
