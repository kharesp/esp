import numpy as np
operators=['noop','fib','bf','eqh','clahe','seg_no_write','lpr','bf_lpr','eqh_lpr','clahe_lpr']
op_vertex={'noop':'v1',
  'fib':'v1',
  'bf':'v1',
  'eqh':'v1',
  'clahe':'v1',
  'seg_no_write':'v1',
  'lpr':'v1',
  'bf_lpr':'v2',
  'eqh_lpr':'v2',
  'clahe_lpr':'v2',
}

header='op,mean_latency_sh,mean_latency_dist,std_latency_sh,std_latency_dist,90th_sh,90th_dist,tot_latency_sh,tot_latency_dist,tot_std_sh,tot_std_dist,tot_90th_sh,tot_90th_dist'

with open('log/operator_benchmark/summary.csv','w') as outf:
  outf.write(header+'\n')
  for op in operators:
    lat_sh={}
    lat_dist={}
  
    tot_sh={} 
    tot_dist={}
  
    with open('log/operator_benchmark/single_host/%s/summary/g1_vertices.csv'%(op),'r') as inp:
      next(inp)
      for line in inp:
        if line.startswith(op_vertex[op]):
          vid,l_mean,l_std,l_90th=line.strip().split(',')
          lat_sh['mean_lat']=float(l_mean)
          lat_sh['std_lat']=float(l_std)
          lat_sh['90th_lat']=float(l_90th)
  
    with open('log/operator_benchmark/distributed/%s/summary/g1_vertices.csv'%(op),'r') as inp:
      next(inp)
      for line in inp:
        if line.startswith(op_vertex[op]):
          vid,l_mean,l_std,l_90th=line.strip().split(',')
          lat_dist['mean_lat']=float(l_mean)
          lat_dist['std_lat']=float(l_std)
          lat_dist['90th_lat']=float(l_90th)
  
    with open('log/operator_benchmark/single_host/%s/summary/summary_g1.csv'%(op),'r') as inp:
      next(inp)
      vid,l_mean,l_std,l_90th=next(inp).strip().split(',')
      tot_sh['mean_lat']=float(l_mean)
      tot_sh['std_lat']=float(l_std)
      tot_sh['90th_lat']=float(l_90th)
        
    with open('log/operator_benchmark/distributed/%s/summary/summary_g1.csv'%(op),'r') as inp:
      next(inp)
      vid,l_mean,l_std,l_90th=next(inp).strip().split(',')
      tot_dist['mean_lat']=float(l_mean)
      tot_dist['std_lat']=float(l_std)
      tot_dist['90th_lat']=float(l_90th)
  
    outf.write('%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'%(op,
      lat_sh['mean_lat'],lat_dist['mean_lat'],
      lat_sh['std_lat'],lat_dist['std_lat'],
      lat_sh['90th_lat'],lat_dist['90th_lat'],
      tot_sh['mean_lat'],tot_dist['mean_lat'],
      tot_sh['std_lat'],tot_dist['std_lat'],
      tot_sh['90th_lat'],tot_dist['90th_lat']))
  
    #print('op:%s\nmean latency(op)[sh,dist,diff]:%f,%f,%f\n90th latency(op)[sh,dist,diff]:%f,%f,%f\nmean latency(tot)[sh,dist,diff]:%f,%f,%f,\n90th_latency(tot)[sh,dist,diff]:%f,%f,%f\n'%(op,
    #  lat_sh['mean_lat'],lat_dist['mean_lat'],lat_dist['mean_lat']-lat_sh['mean_lat'],
    #  lat_sh['90th_lat'],lat_dist['90th_lat'],lat_dist['90th_lat']-lat_sh['90th_lat'],
    #  tot_sh['mean_lat'],tot_dist['mean_lat'],tot_dist['mean_lat']-tot_sh['mean_lat'],
    #  tot_sh['90th_lat'],tot_dist['90th_lat'],tot_dist['90th_lat']-tot_sh['90th_lat']))

    print('op:%s avg latency(sh+dist):%f, 90th latency(sh+dist):%f'%(op,np.mean([lat_sh['mean_lat'],lat_dist['mean_lat']]),np.mean([lat_sh['90th_lat'],lat_dist['90th_lat']])))
