import os,collections
import metadata

def parse(log_dir):
  port=5000
  node_vids=collections.defaultdict(list)
  gid_connectors={}
  vid_desc={}
  graphs=os.listdir('%s/dags'%(log_dir))
  for graph in graphs:
    gid=graph.split('.')[0]
    with open('%s/dags/%s'%(log_dir,graph),'r') as inp:
      next(inp)#skip header
      for vertex_description in inp:
        parts=vertex_description.rstrip().split(';') #node;vid;vtype;upstream;rate
        node=parts[0]
        vid=parts[1]
        vtype=parts[2]
        desc=';'.join(parts[1:])
        vid_desc['%s_%s'%(gid,vid)]=desc
        node_vids[node].append('%s_%s'%(gid,vid))
        if vtype!='snk':
          v_connector='%s:%s:%d'%(vid,metadata.node_ip[node],port)
          if gid in gid_connectors:
            gid_connectors[gid]=gid_connectors[gid]+','+v_connector
          else:
            gid_connectors[gid]=v_connector
          port+=1

  node_vdesc={}
  for node,vids in node_vids.items():
    node_vdesc[node]={}
    for vid in vids:
      gid=vid.split('_')[0]
      node_vdesc[node][vid]='%s/%s'%(vid_desc[vid],gid_connectors[gid])

  return node_vdesc
