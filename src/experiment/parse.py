import os,collections
import metadata

def parse(log_dir):
  port=5000
  
  #mapping of a node and hosted vertices
  node_vids=collections.defaultdict(list)
  #mapping of a graph to the zmq connectors of the graph vertices
  gid_connectors={}
  #mapping of a vertex to its parameterization string
  vid_params={}
  #mapping of gid to number of vertices in the graph 
  gid_vertices={}

  graphs=os.listdir('%s/dags'%(log_dir))
  for graph in graphs:
    gid=graph.split('.')[0]
    v_count=0
    with open('%s/dags/%s'%(log_dir,graph),'r') as inp:
      next(inp)#skip header
      for vertex_parameterization in inp:
        parts=vertex_parameterization.rstrip().split(';') #node;vid;vtype;upstream;rate;count
        node=parts[0]
        vid=parts[1]
        vtype=parts[2]
        params=';'.join(parts[1:])
        vid_params['%s_%s'%(gid,vid)]=params
        node_vids[node].append('%s_%s'%(gid,vid))
        if vtype!='snk':
          v_connector='%s:%s:%d'%(vid,metadata.node_ip[node],port)
          if gid in gid_connectors:
            gid_connectors[gid]=gid_connectors[gid]+','+v_connector
          else:
            gid_connectors[gid]=v_connector
          port+=1
        v_count=+1
      gid_vertices[gid]=v_count

  node_vdesc={}
  for node,vids in node_vids.items():
    node_vdesc[node]={}
    for vid in vids:
      gid=vid.split('_')[0]
      node_vdesc[node][vid]='%s/%s'%(vid_params[vid],gid_connectors[gid])

  return (node_vdesc,gid_vertices)
