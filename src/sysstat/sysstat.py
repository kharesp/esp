from kazoo.client import KazooClient
from kazoo.recipe.barrier import Barrier
import datetime,subprocess,argparse,os,sys
sys.path.append('src/experiment')
import metadata

def collect_system_stats(zk_connector,zk_dir,log_dir):
  zk=KazooClient(hosts=zk_connector)
  zk.start()
  start_barrier=Barrier(client=zk,path='%s/barriers/start'%(zk_dir))
  end_barrier=Barrier(client=zk,path='%s/barriers/end'%(zk_dir))

  ip_addr=os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
  hostname=metadata.ip_node[ip_addr]

  start_barrier.wait()
  start_ts=datetime.datetime.now().strftime('%H:%M:%S')

  end_barrier.wait()
  end_ts=datetime.datetime.now().strftime('%H:%M:%S')

  res=subprocess.check_output(['sadf', '-s', start_ts, '-e', end_ts, '-Uhd', '--','-ur'])
  with open('%s/util_%s.csv'%(log_dir,hostname),'w') as f:
    for line in res.decode().split('\n'):
      f.write(line+'\n')

  res=subprocess.check_output(['sadf', '-s', start_ts, '-e', end_ts, '-Uhd', '--', '-n','DEV'])
  with open('%s/nw_%s.csv'%(log_dir,hostname),'w') as f:
    for line in res.decode().split('\n'):
      f.write(line+'\n')


if __name__=='__main__':
  parser=argparse.ArgumentParser(description='script to collect system statistics')
  parser.add_argument('zk_connector',help='zk_connector')
  parser.add_argument('zk_dir',help='root path for zk tree')
  parser.add_argument('log_dir',help='log dir where stats will be stored')
  args=parser.parse_args()
  collect_system_stats(args.zk_connector,args.zk_dir,args.log_dir)
