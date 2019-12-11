import sys,time,collections
sys.path.append('src/dag')
import vertex
import numpy as np

class Sink(vertex.Vertex):
  def __init__(self,vid,graph,upstream_operators,zk_connector,zk_dir,log_dir):
    super(Sink,self).__init__(vid,graph,upstream_operators,zk_connector,zk_dir,log_dir)
    self.path_latency=collections.defaultdict(list)

  def vfunction(self,update):
    receive_ts=time.time()
    parts=update.split(',')
    idx=int(parts[1])
    ts=parts[2]
    path=parts[3]
    path_latency_ms=(receive_ts-float(ts))*1000
    self.path_latency[path].append((idx,path_latency_ms))

  def clean_up(self):
    for path in self.path_latency.keys():
      with open('%s/%s_latency_%s.csv'%(self.log_dir,self.graph.gid,path),'w') as f:
        f.write('sample_id,latency(ms)\n')
        for (idx,l) in self.path_latency[path]:
          f.write('%d,%f\n'%(idx,l))
