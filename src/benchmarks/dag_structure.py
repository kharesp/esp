import sys,argparse
sys.path.append('src/experiment')
import run

if __name__=='__main__':
  parser=argparse.ArgumentParser(description='Script to test impact of DAG structures on latency')
  parser.add_argument('zk_connector',help='zk connector')
  args=parser.parse_args()

  base_dir='/home/pi/workspace/python/esp/dags/'
  fork_structures=['f1/original','f1/p1','f1/p2','f2/original','f2/p1','f2/p2','f2/p3','f3/original','f3/p1','f3/p2','f3/p3','f3/p4']
  
  for fork_structure in fork_structures:
    print('\n\n\nTesting structure:%s'%(fork_structure))
    test_dir='%s/fork/%s'%(base_dir,fork_structure)
    exp=run.Experiment(test_dir,args.zk_connector,zk_dir,test_dir)
    exp.run()
