import argparse,sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,source,opencv,sink,metadata

def execute(gid,vdesc,zk_connector,zk_dir,log_dir):
  vparams,connectors=vdesc.split('/')
  vid_connector={}
  for connector in connectors.split(','):
    vid,ip,port=connector.split(':')
    vid_connector[vid]=vertex.ZmqConnector(ip,int(port))
  graph=vertex.Graph(gid,vid_connector)

  vid,vtype,upstream_vertices,rate,count=vparams.split(';')

  upstream_vertex_list=None
  if upstream_vertices:
    upstream_vertex_list=upstream_vertices.split(',')
  
  if vtype=='src':
    v=source.Source(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir,metadata.data_dir,rate,count)
    v.execute()
  elif vtype=='lpr':
    v=opencv.LPR(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='eqh':
    v=opencv.EqHist(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='clahe':
    v=opencv.ClaheHist(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='bf':
    v=opencv.BilateralFilter(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='seg':
    v=opencv.Segment(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='fib':
    v=opencv.Bogus(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  elif vtype=='snk':
    v=sink.Sink(vid,graph,upstream_vertex_list,zk_connector,zk_dir,log_dir)
    v.execute()
  else:
    print('Invalid Vertex Type')

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to launch a vertex')
  parser.add_argument('gid',help='graph id')
  parser.add_argument('vdesc',help='vertex descriptor string in the form of vparams/connectors')
  parser.add_argument('zk_connector',help='zk_connector')
  parser.add_argument('zk_dir',help='root path for zk tree')
  parser.add_argument('log',help='log directory')
  args=parser.parse_args()
  execute(args.gid,args.vdesc,args.zk_connector,args.zk_dir,args.log)
