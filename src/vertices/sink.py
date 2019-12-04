import sys,time,collections
sys.path.append('src/dag')
import vertex
import numpy as np

class Sink(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,log_dir):
    super(Sink,self).__init__(vid,graph,upstream_operators)
    self.log_dir=log_dir
    self.path_latency=collections.defaultdict(list)
    self.results_f=open('%s/latency_%s_%s.csv'%(log_dir,graph.gid,vid),'w')
    self.results_f.write('path,latency(ms),std_dev\n')

  def vfunction(self,update):
    receive_ts=time.time()
    code,idx,ts,path,img_str=update.split(',')
    path_latency_ms=(receive_ts-float(ts))*1000
    self.path_latency[path].append(path_latency_ms)

  def clean_up(self):
    for path in self.path_latency.keys():
      path_latency=np.mean(self.path_latency[path])
      path_std_dev=np.std(self.path_latency[path])
      self.results_f.write('%s,%f,%f\n'%(path,path_latency,path_std_dev))
    self.results_f.close()
