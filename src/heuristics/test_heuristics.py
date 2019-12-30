import subprocess,os,sys
sys.path.append('src/experiment')
import run

if __name__=='__main__':
  base_dir='/home/pi/workspace/python/esp/log/heuristics'
  zk_connector='129.59.105.42:2181'
  zk_dir='/test'

  for nc in [0,10,20,30,1000]:
    for method in ['const','sum','lpp']:
      for vnum in range(1,4):
        log_dir='%s/nc%d/g%d/%s'%(base_dir,nc,vnum,method)
        print(log_dir)
        #run experiment 
        exp=run.Experiment(log_dir,zk_connector,zk_dir,log_dir)
        exp.run()
       
        #create placement
        #if not os.path.exists(log_dir):
        #  os.makedirs(log_dir)
        #res=subprocess.check_output(['python3.6', 'src/heuristics/place.py',\
        #  'dags/app/g%d.txt'%(vnum),method,'%d'%(nc),log_dir])
        #with open('%s/placement_log.txt'%(log_dir),'w') as f:
        #  for line in res.decode().split('\n'):
        #    f.write(line+'\n')
