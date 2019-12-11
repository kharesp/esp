import parse,subprocess,time
import metadata
from kazoo.client import KazooClient
from kazoo.protocol.states import EventType
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.recipe.barrier import Barrier

class Experiment(object):
  def __init__(self,config_dir,zk_connector,zk_root_dir,local_log_dir):
    self.config_dir=config_dir
    self.zk_connector=zk_connector
    self.zk_root_dir=zk_root_dir
    self.local_log_dir=local_log_dir
    self.node_vertices,self.gid_vcount=parse.parse(config_dir)
    self.zk=KazooClient(hosts=zk_connector)
    self.zk.start()

  def run(self):
    start_ts=time.time()
    #kill any pre-existing vertices on hosts
    print('Killing pre-exiting vertices...')
    self.kill()

    #clean logs
    print('Deleting previous logs...')
    self.clean_logs()
   
    #configure zk tree and watches
    print('Setting up zk tree...')
    self.configure_zk()
    self.configure_watches()

    #execute vertices
    print('About to start vertices...')
    self.execute()
 
    #wait for experiment to finish
    print('Waiting on experiment to finish...')
    self.end_barrier.wait()
    print('Experiment has finished')

    #collect logs
    print('Collecting logs...')
    self.collect_logs()
 
    print('Summarizing results...')
    #summarize results
    self.summarize()

    #clean-up
    self.shutdown()
    end_ts=time.time()
    print('Experiment took:%f min'%((end_ts-start_ts)/(60000.0)))
  
  def kill(self):
    subprocess.check_call(['ansible-playbook',\
      'playbooks/kill.yml',\
      '--limit',','.join(self.node_vertices.keys())])

  def clean_logs(self):
    subprocess.check_call(['ansible-playbook',\
      'playbooks/clean.yml',\
      '--limit',','.join([x for x in self.node_vertices.keys()]),\
      '--extra-vars=dir=%s'%(metadata.remote_log_dir)])

  def configure_zk(self):
    #clean /joined, /exited, /barriers paths
    if self.zk.exists('%s/joined'%(self.zk_root_dir)):
      self.zk.delete('%s/joined'%(self.zk_root_dir),recursive=True)
    if self.zk.exists('%s/exited'%(self.zk_root_dir)):
      self.zk.delete('%s/exited'%(self.zk_root_dir),recursive=True)
    if self.zk.exists('%s/barriers'%(self.zk_root_dir)):
      self.zk.delete('%s/barriers'%(self.zk_root_dir),recursive=True)

    #create graph_ids under /joined and /exited
    for gid in self.gid_vcount.keys():
      self.zk.ensure_path('%s/joined/%s'%(self.zk_root_dir,gid))
      self.zk.ensure_path('%s/exited/%s'%(self.zk_root_dir,gid))

    #create barrier paths and barriers
    self.zk.ensure_path('%s/barriers/start'%(self.zk_root_dir))
    self.zk.ensure_path('%s/barriers/end'%(self.zk_root_dir))
    self.start_barrier=Barrier(client=self.zk,path='%s/barriers/start'%(self.zk_root_dir))
    self.end_barrier=Barrier(client=self.zk,path='%s/barriers/end'%(self.zk_root_dir))

  def configure_watches(self):
    self.joined_count=0
    self.exited_count=0
    self.joined={gid:0 for gid in self.gid_vcount.keys()}
    self.exited={gid:0 for gid in self.gid_vcount.keys()}

    def _joined_endpoint_listener(children,event):
      if event and event.type==EventType.CHILD:
        if 'joined' in event.path:
          joined_dag=event.path.split('/')[-1]
          self.joined[joined_dag]=len(children)
          if (self.joined[joined_dag]==self.gid_vcount[joined_dag]):
            self.joined_count+=1
            if (self.joined_count==len(self.gid_vcount)):
              print('All vertices have joined. Removing start barrier')
              self.start_barrier.remove()
            return False

    def _exited_endpoint_listener(children,event):
      if event and event.type==EventType.CHILD:
        if 'exited' in event.path:
          exited_dag=event.path.split('/')[-1]
          self.exited[exited_dag]=len(children)
          if (self.exited[exited_dag]==self.gid_vcount[exited_dag]):
            self.exited_count+=1
            if (self.exited_count==len(self.gid_vcount)):
              print('All vertices have exited. Removing end barrier')
              self.end_barrier.remove()
            return False

    for gid in self.gid_vcount.keys():
      ChildrenWatch(client=self.zk,\
        path='%s/joined/%s'%(self.zk_root_dir,gid),\
        func=_joined_endpoint_listener,send_event=True)
      ChildrenWatch(client=self.zk,\
        path='%s/exited/%s'%(self.zk_root_dir,gid),\
        func=_exited_endpoint_listener,send_event=True)

  def execute(self):
    for node,vertices in self.node_vertices.items():
      subprocess.check_call(['ansible-playbook','playbooks/vertex.yml',\
        '--limit',node,\
        '--extra-vars=map=%s \
        zk_connector=%s \
        zk_dir=%s \
        log_dir=%s'%(str(vertices).replace(" ",""),\
        self.zk_connector,self.zk_root_dir,metadata.remote_log_dir)])

  def collect_logs(self):
    subprocess.check_call(['ansible-playbook','playbooks/copy.yml',\
      '--limit',','.join([x for x in self.node_vertices.keys()]),\
      "--extra-vars=src_dir=%s/ \
      dest_dir=%s/ ignore='err'"%(metadata.remote_log_dir,self.local_log_dir)])

    files=[f for f in os.listdir(self.local_log_dir) if os.path.isfile('%s/%s'%(self.local_log_dir,f))]
    for gid in self.gid_vcount.keys():
      if not os.path.exists('%s/data/%s'%(self.local_log_dir,gid)):
        os.makedirs('%s/data/%s'%(self.local_log_dir,gid))
    if not os.path.exists('%s/util'%(self.local_log_dir)):
      os.makedirs('%s/util'%(self.local_log_dir))
    for file_name in files:
      if file_name.startswith('util') or file_name.startswith('nw'):
        shutil.move('%s/%s'%(self.local_log_dir,file_name),'%s/util/'%(self.local_log_dir))
      for gid in self.gid_vcount.keys():
        if file_name.startswith(gid):
          shutil.move('%s/%s'%(self.local_log_dir,file_name),'%s/data/%s/'%(self.local_log_dir,graph_id))

  def summarize(self): 
    pass

  def shutdown(self):
    self.zk.stop()

Experiment('log/1','192.168.88.87:2181','/test').run()
