import rx,zmq,sys,time
import numpy as np
from typing import NamedTuple,Dict
sys.path.append('src/rxzmq')
from rxzmq import from_topic,to_topic
from rx.operators import do_action
from kazoo.client import KazooClient

VERTEX_TYPE_SOURCE=0
VERTEX_TYPE_INTERMEDIATE=1
VERTEX_TYPE_SINK=2
DEBUG_COUNT=10

class ZmqConnector(NamedTuple):
  ip_addr: str
  port: int

class Graph(NamedTuple):
  gid: str
  operators: Dict[str,ZmqConnector]

class Vertex:
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    self.vid=vid
    self.graph=graph
    self.count=0
    self.log_dir=log_dir

    self.zk_connector=zk_connector
    self.zk_dir=zk_dir
    self.zk=KazooClient(hosts=zk_connector)
    self.zk.start()

    if not upstream_operators:
      self.vertex_type=VERTEX_TYPE_SOURCE
    else:
      if not vid in self.graph.operators:
        self.vertex_type=VERTEX_TYPE_SINK
      else:
        self.vertex_type=VERTEX_TYPE_INTERMEDIATE
      self.compute_times=[]
      self.output_file=open('%s_%s.csv'%(graph.gid,vid),'w')
      self.output_file.write('compute latency(ms),std_dev\n')
      self.incoming_topic=from_topic(['%s_%s'%(graph.gid,op) for op in upstream_operators],\
        [graph.operators[op].ip_addr for op in upstream_operators],\
        [graph.operators[op].port for op in upstream_operators])

    self.zk.ensure_path('%s/joined/%s/%s'%(zk_dir,graph.gid,vid))

  def publish(self):
    #creates an observable of data samples published by this source vertex
    pass
 
  def vfunction(self,value):
    #encodes the function this vertex performs on incoming data samples
    pass 

  def clean_up(self):
    #specifies any clean-up this vertex needs to do before exiting
    pass
 
  def compute(self):
    def _compute(source):
      def subscribe(observer,scheduler=None):
        def on_next(value):
          receive_ts=time.time()
          r=self.vfunction(value)
          finish_ts=time.time()
          self.count+=1
          if (self.count%DEBUG_COUNT==0):
            print('vertex:%s_%s processed sample:%d'%(self.graph.gid,self.vid,self.count))
          self.compute_times.append((finish_ts-receive_ts)*1000)
          observer.on_next(r)
        def on_error(err):
          self.shutdown()
          observer.on_error(err)
        def on_completed():
          self.shutdown()
          observer.on_completed()
        return source.subscribe(on_next,on_error,on_completed,scheduler)
      return rx.create(subscribe)
    return _compute

  def execute(self):
    if self.vertex_type==VERTEX_TYPE_SOURCE:
      self.publish().pipe(to_topic('%s_%s'%(self.graph.gid,self.vid),
        self.graph.operators[self.vid].ip_addr,
        self.graph.operators[self.vid].port)).subscribe()
    else:
      processed_stream=self.incoming_topic.pipe(self.compute())
      if self.vertex_type==VERTEX_TYPE_INTERMEDIATE:
        processed_stream.pipe(to_topic('%s_%s'%(self.graph.gid,self.vid),
          self.graph.operators[self.vid].ip_addr,
          self.graph.operators[self.vid].port)).subscribe()
      elif self.vertex_type==VERTEX_TYPE_SINK:
        processed_stream.subscribe()

  def shutdown(self):
    if self.vertex_type==VERTEX_TYPE_INTERMEDIATE or self.vertex_type==VERTEX_TYPE_SINK:
      mean_compute_time=np.mean(self.compute_times)
      std_compute_time=np.std(self.compute_times)
      self.output_file.write('%f,%f\n'%(mean_compute_time,std_compute_time))
      self.output_file.close()
    self.zk.ensure_path('%s/exited/%s/%s'%(self.zk_dir,self.graph.gid,self.vid))
    self.zk.stop()
    self.clean_up()
