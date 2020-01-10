import os,glob
import numpy as np

def makespan(log_dir,msg_count):
  if not os.path.exists('%s/summary'%(log_dir)):
    os.makedirs('%s/summary'%(log_dir))
  graphs=os.listdir('%s/data'%(log_dir))
  for gid in graphs:
    makespan_latencies=[]
    files=glob.glob('%s/data/%s/%s_latency*.csv'%(log_dir,gid,gid))
    fhandlers=[open(f,'r') for f in files]
    for fh in fhandlers: 
      next(fh)
    for msg_id in range(msg_count):
      path_latencies=[]
      for fh in fhandlers:
        mid,latency=next(fh).split(',')
        path_latencies.append(float(latency))
      makespan_latencies.append(max(path_latencies))

    sorted_latency=np.sort(makespan_latencies)
    l_90th= np.percentile(sorted_latency,90)
    with open('%s/summary/makespan_%s.csv'%(log_dir,gid),'w') as outf:
      outf.write('%f\n'%(l_90th))
