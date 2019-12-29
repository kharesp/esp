import random

operators=['bf','eqh','clahe','seg','fib','lpr']
max_vertices_per_chain=4
publication_rate=1
msg_count=200

def generate_params(k,count):
  combinations=set()
  all_lpr_chains=set()

  while len(combinations)<count:
    parameterization_str=''
    vid=1
    chainId_lpr={}
    for chain in range(1,k+1):
      num_vertices=random.randint(1,max_vertices_per_chain)
      ops=[]
      for opcount in range(num_vertices):
        sel_op=operators[random.randint(0,len(operators)-1)]
        while (sel_op=='lpr') and (sel_op in ops):
          sel_op=operators[random.randint(0,len(operators)-1)]
        ops.append(sel_op)
      if 'lpr' in ops:
        chainId_lpr[chain]=True
      else:
        chainId_lpr[chain]=False
        
      parameterization_str+='%d;%s;%s/'%(num_vertices,\
        '-'.join(['v%d'%(i+vid) for i in range(num_vertices)]),\
        ','.join(ops))
      vid+=num_vertices

    combinations.add(parameterization_str.strip('/'))
    if all(chainId_lpr.values()):
      all_lpr_chains.add(parameterization_str.strip('/'))
  return (combinations,all_lpr_chains) 

def write_params(k,count,log_dir):
  params,all_lpr=generate_params(k,count)
  with open('%s/k%d'%(log_dir,k),'w') as of:
    for param_str in all_lpr:
      of.write('%s\n'%(param_str))
    for param_str in (params-all_lpr):
      of.write('%s\n'%(param_str))


def generate_graph_description(parameterization_str,\
  src_snk_node,intermediate_node,log_dir):
  with open('%s/g1.txt'%(log_dir),'w') as of:
    of.write('node;vid;vtype;upstream;rate;count\n')
    of.write('%s;v0;src;;%d;%d\n'%(src_snk_node,publication_rate,msg_count))
    path_descriptions=parameterization_str.strip().split('/')
    total_vertices=0 
    snk_upstream=[]
    for path_description in path_descriptions:
      vcount,path,vtypes=path_description.split(';')
      total_vertices+=int(vcount)
      vids=path.split('-')
      snk_upstream.append(vids[-1])
      ops=vtypes.split(',')
      for idx,vid in enumerate(vids):
        if idx==0:
          of.write('%s;%s;%s;v0;%d;%d\n'%(intermediate_node,vid,\
            ops[idx],publication_rate,msg_count))
        else:
          of.write('%s;%s;%s;%s;%d;%d\n'%(intermediate_node,vid,\
            ops[idx],vids[idx-1],publication_rate,msg_count))
    of.write('%s;v%d;snk;%s;%d;%d\n'%(src_snk_node,total_vertices+1,\
      ','.join(snk_upstream),publication_rate,msg_count))
