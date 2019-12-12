import argparse,os,sys
sys.path.append('src/experiment')
import run
from ml_parameterization import generate_graph_description

def test_parameterization(k,start_tid,src_snk_node,intermediate_node,zk_connector,zk_dir,log_dir):
  with open('log/model_learning/parameterization/k%d'%(k),'r') as if:
    for idx,param_str in enumerate(if):
      if (idx+1)<start_tid:
        continue
      test_dir='%s/%d'%(log_dir,idx+1)
      if not os.path.exists(test_dir):
        os.makedirs(test_dir)
      if not os.path.exists('%s/dags'%(test_dir)):
        os.makedirs('%s/dags'%(test_dir))
      generate_graph_description(param_str,src_snk_node,intermediate_node,'%s/dags'%(test_dir))
      exp=run.Experiment(test_dir,zk_connector,zk_dir,test_dir)
      break
      

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to run parameterized experiments for model learning')
  parser.add_argument('k',help='k-colocation')
  parser.add_argument('start_tid',help='parameterization idx to execute onwards from')
  parser.add_argument('src_snk_node',help='node on which source and sink vertices will be hosted')
  parser.add_argument('intermediate_node',help='node on which intermediate vertices will be hosted')
  parser.add_argument('zk_connector',help='zk_connector')
  parser.add_argument('zk_dir',help='root path for zk tree')
  parser.add_argument('log',help='log directory')
  args=parser.parse_args()
  (args.gid,args.vdesc,args.zk_connector,args.zk_dir,args.log)
