import sys,time,collections
sys.path.append('src/dag')
import vertex
import numpy as np

class Sink(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Sink,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.path_latency=collections.defaultdict(list)
    self.results_f=open('%s/latency_%s_%s.csv'%(self.log_dir,graph.gid,vid),'w')
    self.results_f.write('path,latency(ms),std_dev\n')

  def vfunction(self,update):
    receive_ts=time.time()
    parts=update.split(',')
    ts=parts[2]
    path=parts[3]
    path_latency_ms=(receive_ts-float(ts))*1000
    self.path_latency[path].append(path_latency_ms)

  def clean_up(self):
    for path in self.path_latency.keys():
      path_latency=np.mean(self.path_latency[path])
      path_std_dev=np.std(self.path_latency[path])
      self.results_f.write('%s,%f,%f\n'%(path,path_latency,path_std_dev))
    self.results_f.close()
