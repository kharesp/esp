import argparse,sys
sys.path.append('src/dag')
import vertex

def execute(gid,vdesc):
  vparams,connectors=vdesc.split('/')
  #vid_connector={}
  #for connector in connectors.split(','):
  #  vid,ip,port=connector.split(':')
  #  vid_connector[vid]=vertex.ZmqConnector(ip,int(port))
  #graph=vertex.Graph(gid,vid_connector)

  
  

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to launch a vertex')
  parser.add_argument('gid',help='graph id')
  parser.add_argument('vdesc',help='vertex descriptor string in the form of vdesc/connectors')
  args=parser.parse_args()
  execute(args.gid,args.vdesc)
