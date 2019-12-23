import sys
sys.path.append('src/benchmarks')
import os,argparse,collections
import ml_parameterization

op_exec={'noop': 15,
  'fib': 25,
  'bf': 35,
  'eqh': 15,
  'clahe': 20,
  'seg': 15,
  'lpr': 270,
}

def extract_features(k,intermediate_node,start,end,log_dir,out_dir):
  tests=os.listdir('%s/k%d'%(log_dir,k))
  with open('%s/parameterization/k%d'%(log_dir,k),'r') as params,\
    open('%s/k%d.csv'%(out_dir,k),'w') as outf:
    #outf.write('idx,fv,fproc,bv,bproc,flat_mean,flat_90th,cpu(%),iowait(%),mem(%),nw(kB/s)\n')
    outf.write('idx,fv,fproc,bv,bproc,flat_mean,flat_90th,v0,v1,v2,v3\n')
    for i in range(1,len(tests)+1): 
      param_str=next(params)
      if i<start:
        continue
      if i>end:
        break
       
      linear_chains=param_str.strip().split('/') 
      path_params={}
      for linear_chain in linear_chains:
        vcount,path,ops=linear_chain.split(';')
        processing_intervals=[op_exec[op] for op in ops.split(',')]
        while len(processing_intervals)<ml_parameterization.max_vertices_per_chain:
          processing_intervals.append(0)
        
        path_params['v0-'+path]={'vcount':int(vcount),\
          'proc': processing_intervals}
      
      path_latency={}
      with open('%s/k%d/%d/summary/summary_g1.csv'%(log_dir,k,i),'r') as latf:
        next(latf)
        for line in latf:
          path,lat_mean,lat_std,lat_90th=line.strip().split(',')
          path_latency[path]={'90th':float(lat_90th),'mean':float(lat_mean)}

      #util=collections.defaultdict(lambda: 0)
      #if os.path.exists('log/model_learning/k%d/%d/summary/summary_util.csv'%(k,i)):
      #  with open('log/model_learning/k%d/%d/summary/summary_util.csv'%(k,i),'r') as uf:
      #    next(uf)
      #    for line in uf:
      #      if line.startswith(intermediate_node):
      #        node,cpu,iowait,mem,systat_mem,nw=line.strip().split(',')
      #        util['cpu']=float(cpu)
      #        util['iowait']=float(iowait)
      #        util['mem']=float(mem)
      #        util['nw']=float(nw)

      for path,latency in path_latency.items():
        fv=path_params[path]['vcount']
        fproc=sum(path_params[path]['proc'])
        bv=0
        bproc=0
        for other_path in path_latency.keys():
          if path==other_path:
            continue
          bv+=path_params[other_path]['vcount']
          bproc+=sum(path_params[other_path]['proc'])
        #outf.write('%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f\n'%(i,fv,fproc,bv,bproc,\
        #  latency['mean'],latency['90th'],util['cpu'],util['iowait'],util['mem'],util['nw']))
        outf.write('%d,%d,%d,%d,%d,%f,%f,%d,%d,%d,%d\n'%(i,fv,fproc,bv,bproc,\
          latency['mean'],latency['90th'],path_params[path]['proc'][0],\
          path_params[path]['proc'][1],path_params[path]['proc'][2],\
          path_params[path]['proc'][3]))
      #if not any(util.values()):
      #  print('Test:%d summary_util not available'%(i))

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to extract model learning features')
  parser.add_argument('k',help='k colocation',type=int)
  parser.add_argument('intermediate_node',help='node on which intermediate vertices were hosted')
  parser.add_argument('start',type=int,help='start exp number')
  parser.add_argument('end',type=int,help='end exp number')
  parser.add_argument('log_dir',help='log dir')
  parser.add_argument('out_dir',help='output dir')
  args=parser.parse_args()
  extract_features(args.k,args.intermediate_node,args.start,args.end,args.log_dir,args.out_dir) 
