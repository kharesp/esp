import argparse,os,sys
sys.path.append('src/experiment')
import run
from ml_parameterization import generate_graph_description

def test_colocation(k,start_tid,src_snk_node,intermediate_node,zk_connector,zk_dir,log_dir):
  with open('%s/parameterization/k%d'%(log_dir,k),'r') as inpf:
    for idx,param_str in enumerate(inpf):
      if (idx+1)<start_tid:
        continue
      print('\n\n\nExecuting Test:%d'%(idx+1))
      print(param_str)
      test_dir='%s/k%d/%d'%(log_dir,k,idx+1)
      if not os.path.exists(test_dir):
        os.makedirs(test_dir)
      if not os.path.exists('%s/dags'%(test_dir)):
        os.makedirs('%s/dags'%(test_dir))
      generate_graph_description(param_str,src_snk_node,intermediate_node,'%s/dags'%(test_dir))
      exp=run.Experiment(test_dir,zk_connector,zk_dir,test_dir)
      exp.run()
      

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to run parameterized experiments for model learning')
  parser.add_argument('k',help='k-colocation',type=int)
  parser.add_argument('start_tid',help='parameterization idx to execute onwards from',type=int)
  parser.add_argument('src_snk_node',help='node on which source and sink vertices will be hosted')
  parser.add_argument('intermediate_node',help='node on which intermediate vertices will be hosted')
  parser.add_argument('zk_connector',help='zk_connector')
  parser.add_argument('zk_dir',help='root path for zk tree')
  parser.add_argument('log_dir',help='log directory')
  args=parser.parse_args()
  test_colocation(args.k,args.start_tid,args.src_snk_node,args.intermediate_node,args.zk_connector,args.zk_dir,args.log_dir)
