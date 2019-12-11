import os
import pandas as pd
import numpy as np

def latency(log_dir):
  if not os.path.exists('%s/summary'%(log_dir)):
    os.makedirs('%s/summary'%(log_dir))

  graphs=os.listdir('%s/data'%(log_dir))
  for gid in graphs:
    path_summary={}
    vid_summary={}
    files=os.listdir('%s/data/%s'%(log_dir,gid))
    for file_name in files:
      if file_name.startswith('%s_latency'%(gid)):
        data=pd.read_csv('%s/data/%s/%s'%(log_dir,gid,file_name),delimiter=',',skiprows=1,names=['sample_id','latency'])
        path=file_name.rpartition('_')[2].partition('.')[0]
        l_mean=np.mean(data['latency'])
        l_std=np.std(data['latency'])
        sorted_latency=np.sort(data['latency'])
        l_90th=latency_90th= np.percentile(sorted_latency,90)
        path_summary[path]={'mean':l_mean,'std':l_std,'90th':l_90th}
      else:
        data=pd.read_csv('%s/data/%s/%s'%(log_dir,gid,file_name),delimiter=',',skiprows=1,names=['sample_id','latency'])
        vid=file_name.rpartition('_')[2].partition('.')[0]
        l_mean=np.mean(data['latency'])
        l_std=np.std(data['latency'])
        sorted_latency=np.sort(data['latency'])
        l_90th=latency_90th= np.percentile(sorted_latency,90)
        vid_summary[vid]={'mean':l_mean,'std':l_std,'90th':l_90th}

    with open('%s/summary/summary_%s.csv'%(log_dir,gid),'w') as of:
      of.write('path,mean_latency,std_latency,90th_latency\n')
      for path,summary in path_summary.items():
        of.write('%s,%f,%f,%f\n'%(path,summary['mean'],summary['std'],summary['90th']))
    with open('%s/summary/%s_vertices.csv'%(log_dir,gid),'w') as of:
      of.write('vid,mean_latency,std_latency,90th_latency\n')
      for vid,summary in vid_summary.items():
        of.write('%s,%f,%f,%f\n'%(vid,summary['mean'],summary['std'],summary['90th']))

latency('log/1')
