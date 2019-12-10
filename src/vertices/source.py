import sys,glob,time,rx,cv2
sys.path.append('src/dag')
sys.path.append('src/rxzmq')
import vertex,opencv,rxzmq

class Source(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir,data_dir,rate,message_count): 
    super(Source,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.data_dir=data_dir
    self.rate=int(rate)
    self.sleep_interval_s=1.0/self.rate
    self.message_count=int(message_count)

  def publish(self):
    def _publish(observer,scheduler=None):
      count=0
      try:
        img_files=glob.glob('%s/*%s'%(self.data_dir,'.jpg'))
        while count<self.message_count:
          for img_file in sorted(img_files):
            img=cv2.imread(img_file,0)
            img_str=opencv.serialize_img(img,'.jpg')
            msg_str='%d,%d,%f,%s,%s'%(rxzmq.MSG_TYPE_DATA,\
              count,time.time(),self.vid,img_str)
            observer.on_next(msg_str)
            print('Sent img:%d %s'%(count,img_file))
            time.sleep(self.sleep_interval_s)
            count+=1
            if count==self.message_count:
              break
        observer.on_completed()
      except Exception as err:
        observer.on_error(err)
    return rx.Observable(_publish)
