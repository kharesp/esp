import numpy as np
import dag_utils,collections
from sklearn.externals import joblib

op_exec={'noop': 15,
  'fib': 25,
  'bf': 35,
  'eqh': 15,
  'clahe': 20,
  'seg': 15,
  'lpr': 270,
}
k_model={
  1:'k1_nn1_80_fv_fp.pkl',
  2:'k2_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  3:'k3_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  4:'k4_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  5:'k5_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  6:'k6_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  7:'k7_nn2_40_40_bv_bsp_vf_pf_fv_fp.pkl',
  8:'k8_nn2_40_40_bv_bsp_vf_pf_fv_fp.pkl',
}
k_scaler={
  1:'k1_scaler_nn1_80_fv_fp.pkl',
  2:'k2_scaler_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  3:'k3_scaler_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  4:'k4_scaler_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  5:'k5_scaler_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  6:'k6_scaler_nn1_80_bv_bsp_vf_pf_fv_fp.pkl',
  7:'k7_scaler_nn2_40_40_bv_bsp_vf_pf_fv_fp.pkl',
  8:'k8_scaler_nn2_40_40_bv_bsp_vf_pf_fv_fp.pkl',
}


class Greedy:
  def __init__(self):
    self.scalers={}
    self.models={}
    for k in range(1,9):
      self.scalers[k]=joblib.load('models/regression/k%d/%s'%(k,k_scaler[k]))
      self.models[k]=joblib.load('models/regression/k%d/%s'%(k,k_model[k]))

  def get_params(self,dag):
    params={}
    with open(dag,'r') as inf:
      lines=inf.readlines()
    for line in lines[1:]:
      vid,vtype,upstream=line.strip().split(';')
      params[int(vid[1:])]=vtype
    return params

  def get_adj_mat(self,dag):
    with open(dag,'r') as inf:
      lines=inf.readlines()
    mat=np.zeros((len(lines)-1,len(lines)-1))
    for line in lines[1:]:
      vid,vtype,upstream=line.strip().split(';')
      if upstream:
        for upstream_vertex in upstream.split(','):
          mat[int(upstream_vertex[1:])][int(vid[1:])]=1
    return mat

  def replicas(self,adj):
    vertices=np.shape(adj)[0]
    rep={}
    for x in range(vertices):  
      patterns=set()
      for path in [p for p in dag_utils.find_all_paths(adj) if (x in p)]:
        idx=path.index(x)
        partial_path=','.join([str(path[i]) for i in range(idx)])
        patterns.add(partial_path)
      rep[x]=len(patterns)
    return rep

  def bfs(self,adj,sources):
    vertices=np.shape(adj)[0]
    bfs_order=[]
    queue=[]
    visited={x:False for x in range(vertices)}
    for s in sources:
      visited[s]=True
      queue.append(s)
    while len(queue)>0:
      v=queue.pop(0)
      bfs_order.append(v)
      for next_v in np.nonzero(adj[v,:])[0]:
        if visited[next_v]==False:
          queue.append(next_v)
          visited[next_v]=True
    return bfs_order 

  def get_interference_chains_for_partial_path(self,adj,paths,pp):
    interference=[]
    track_rep=self.replicas(adj)
    for x in pp:
      track_rep[x]-=1
    pp_s=','.join([str(x) for x in pp])
    for path in paths:
      path_s=','.join([str(x) for x in path])
      if path_s.startswith(pp_s):
        continue
      ipath=[]
      for x in path:
        if (track_rep[x]>0):
          ipath.append(x)
          track_rep[x]-=1
      interference.append(ipath)
    return interference
      
  def get_interference_chains_for_paths(self,adj,paths):
    interference={}
    for curr_path in paths:
      track_rep=self.replicas(adj)
      curr_path_s=','.join([str(x) for x in curr_path])
      interference[curr_path_s]=[]
      for x in curr_path:
        track_rep[x]-=1
      for path in paths:
        path_s=','.join([str(x) for x in path])
        if path_s==curr_path_s:
          continue
        ipath=[]
        for x in path:
          if (track_rep[x]>0):
             ipath.append(x)
             track_rep[x]-=1
        interference[curr_path_s].append(ipath)
    return interference

  def get_partial_paths_per_node(self,paths,vertex_node):
    path_node_pp={}
    for idx,path in enumerate(paths):
      node_pp={}
      prev_node=vertex_node[path[0]]
      pp=[]
      for v in path:
        curr_node=vertex_node[v]
        if curr_node==prev_node:
          pp.append(v)
        else:
          if prev_node in node_pp:
            node_pp[prev_node].extend(pp)
          else:
            node_pp[prev_node]=pp
          pp=[v]
          prev_node=curr_node
      if prev_node in node_pp:
        node_pp[prev_node].extend(pp)
      else:
        node_pp[prev_node]=pp
      path_node_pp['p%d'%(idx+1)]=node_pp
    
    #res={n:[] for n in set(vertex_node.values())} 
    res=collections.defaultdict(list)
    for node_pp in path_node_pp.values():
      for node,pp in node_pp.items():
        res[node].append(pp)
    return res 

  def compute_path_latency(self,method,curr_path,interference,vertex_node,params,network,adj):
    interference_paths=interference[','.join([str(i) for i in curr_path])]
    sources=list(np.where(~adj.any(axis=0))[0])
    sinks=list(np.where(~adj.any(axis=1))[0])
    #print('Computing path latency for path:%s with interference:%s'%\
    #  (curr_path,interference_paths))

    node_pp=self.get_partial_paths_per_node(interference_paths,vertex_node)

    curr_path_latency=0
    prev_node=vertex_node[curr_path[0]]
    pp=[]
    for x in curr_path:
      curr_node=vertex_node[x]
      if curr_node==prev_node:
        pp.append(x)
      else:
        prev_node_vertices=[]
        for vertex,node in vertex_node.items():
          if node==prev_node:
            prev_node_vertices.append(vertex)
        prev_node_sub_graph=adj[np.ix_(prev_node_vertices,prev_node_vertices)]
        #get all paths in sub-graph
        paths=dag_utils.find_all_paths(prev_node_sub_graph)
        corrected_paths=[[prev_node_vertices[x] for x in p ]for p in paths]
        corrected_paths=[[x for x in p if ((x not in sources) and (x not in sinks))] for p in corrected_paths]
        interference=self.get_interference_chains_for_partial_path(adj,corrected_paths,pp)
        curr_path_latency+=(self.predict(method,pp,interference,params)+network)
        prev_node=curr_node
        pp=[x]
    prev_node_vertices=[]
    for vertex,node in vertex_node.items():
      if node==prev_node:
        prev_node_vertices.append(vertex)
    prev_node_sub_graph=adj[np.ix_(prev_node_vertices,prev_node_vertices)]
    #get all paths in sub-graph
    paths=dag_utils.find_all_paths(prev_node_sub_graph)
    corrected_paths=[[prev_node_vertices[x] for x in p ]for p in paths]
    corrected_paths=[[x for x in p if ((x not in sources) and (x not in sinks))] for p in corrected_paths]
    interference=self.get_interference_chains_for_partial_path(adj,corrected_paths,pp)
    
    curr_path_latency+=self.predict(method,pp,interference,params)
    return curr_path_latency
  
  def predict(self,method,foreground_chain,interference_chains,params):
    print('Predicting latency for pp:%s with interference:%s'%\
      (foreground_chain,interference_chains))
    if method=='lpp':
      return self.predict_lpp(foreground_chain,interference_chains,params)
    elif method=='const':
      return self.predict_const(foreground_chain,interference_chains,params)
    elif method=='sum':
      return self.predict_sum(foreground_chain,interference_chains,params)

  def predict_const(self,foreground_chain,interference_chains,params):
    return sum([op_exec[params[x]] for x in foreground_chain])
  
  def predict_sum(self,foreground_chain,interference_chains,params):
    k=len(interference_chains)+1
    if k<=4:
      res=sum([op_exec[params[x]] for x in foreground_chain])
      print(res)
      return res
    else:
      total_proc=sum([op_exec[params[x]] for x in foreground_chain])
      for background_chain in interference_chains:
        total_proc+=sum([op_exec[params[x]] for x in background_chain])
      res= len(foreground_chain)*(total_proc/4.0)
      print(res)
      return res

  def predict_lpp(self,foreground_chain,interference_chains,params):
    k=len(interference_chains)+1
    feature_vector=self.get_feature_vector(foreground_chain,interference_chains,params)
    scaler=self.scalers[k]
    model=self.models[k]
    if k==1:
      return model.predict(scaler.transform(feature_vector))[0]
    else:
      return np.exp(model.predict(scaler.transform(feature_vector))[0])

  def get_feature_vector(self,foreground_chain,interference_chains,params):
    fv=len(foreground_chain)
    fp=sum([op_exec[params[x]] for x in foreground_chain])
    if len(interference_chains)==0:
      return [[fv,fp]]
    else:
      bv=sum([len(linear_chain) for linear_chain in interference_chains])
      bsp=sum([sum([op_exec[params[x]] for x in linear_chain]) for linear_chain in interference_chains])
      vf=(fv*1.0)/(fv+bv)
      pf=(fp*1.0)/(fp+bsp)
      return [[bv,bsp,vf,pf,fv,fp]]

  def place(self,dag,method,network):
    #get adjacency matrix for graph description
    adj=self.get_adj_mat(dag)
    #get vertex type for each vertex
    params=self.get_params(dag)
    number_of_vertices=np.shape(adj)[0]
    sources=list(np.where(~adj.any(axis=0))[0])
    sinks=list(np.where(~adj.any(axis=1))[0])
    vertex_replicas=self.replicas(adj)
    
    bfs_order=self.bfs(adj,sources)

    
    placement={}
    for idx,v in enumerate(bfs_order):
      print('\n\n**************************************************')
      print('Placing vertex:%d'%(v))
      if (v in sources) or (v in sinks):
        continue
      sub_graph_vertices=sorted([bfs_order[x] for x in range(idx+1)])

      sub_graph=adj[np.ix_(sub_graph_vertices,sub_graph_vertices)]
      

      paths=dag_utils.find_all_paths(sub_graph)
      #get all paths in sub-graph
      corrected_paths=[[sub_graph_vertices[x] for x in p ]for p in paths]
      #drop source and sink vertices from corrected paths
      corrected_paths=[[x for x in p if ((x not in sources) and (x not in sinks))] for p in corrected_paths]

      #create interference paths for each path 
      interference=self.get_interference_chains_for_paths(adj,corrected_paths)
      
      #compute each path's latency when current vertex v is placed on each eligible physical node
      node_makespan={}
      for node in list(placement.keys())+['node%d'%(len(placement)+1)]:
        print('\nTesting placement of vertex:%d on node:%s'%(v,node))
        feasibility_for_node=True
        vertex_node={}
        vertex_node[v]=node
        for host,vertices in placement.items(): 
          for vertex in vertices:
            vertex_node[vertex]=host
        node_pp=self.get_partial_paths_per_node(corrected_paths,vertex_node)
        print('Partial paths are:\n%s'%(node_pp))
        if len(node_pp[node])>8:
          feasibility_for_node=False
          print('Not feasible to place vertex:%d on node:%s'%(v,node))
          continue

        configuration_latencies=[]
        for curr_path in corrected_paths:
          #compute this path's latency
          curr_path_latency=self.compute_path_latency(method,curr_path,interference,vertex_node,params,network,adj)
          print('Latency for path:%s is %f'%(curr_path,curr_path_latency))
          configuration_latencies.append(curr_path_latency)
        node_makespan[node]=max(configuration_latencies)

      #select node which gives minimum makespan of sub-dag 
      print(node_makespan)
      selected_node=min(node_makespan.items(),key=lambda x: x[1])[0]
      print('Placing vertex:%d on selected node:%s'%(v,selected_node))
      
      if selected_node not in placement:
        placement[selected_node]=[v]
      else:
        placement[selected_node].append(v)
    return placement
          
if __name__=='__main__':
  dag='dags/test/t1/repr/g1.txt'
  adj=Greedy().get_adj_mat(dag)
  params=Greedy().get_params(dag)
  print(Greedy().place(dag,'lpp',30))