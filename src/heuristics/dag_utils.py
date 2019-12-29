import numpy as np

def get_source_vertices(adj):
  #source vertices have a column of all zeros, i.e., no in-going edge
  source_vertices= np.where(~adj.any(axis=0))[0]
  return source_vertices

def get_sink_vertices(adj):
  #sink vertices have a row of all zeros, i.e., no out-going edge
  sink_vertices= np.where(~adj.any(axis=1))[0]
  return sink_vertices

def find_all_paths_for_vertex(vertex,dag):
  def compute(v):
    out_deg=np.nonzero(dag[v,:])[0]
    if len(out_deg)==0:
      return [[v]]
    else:
      partial_paths=[]
      for x in out_deg:
        forward_paths=compute(x)
        for p in forward_paths:
          partial_paths.append([v]+p)
      return partial_paths
  return compute(vertex)

def find_all_paths(dag):
  paths=[]
  source_vertices=np.where(~dag.any(axis=0))[0]
  for v in source_vertices:
    for p in find_all_paths_for_vertex(v,dag):
      paths.append(p)
  return paths
