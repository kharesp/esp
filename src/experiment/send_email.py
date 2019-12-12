import smtplib,time,os,argparse

def monitor(email_id,app_password,log_dirs):
  dir_count={}
  dir_status={log_dir:True for log_dir in log_dirs}

  for log_dir in log_dirs:
    dir_count[log_dir]=len(os.listdir(log_dir))

  s = smtplib.SMTP('smtp.gmail.com', 587) 
  # start TLS for security 
  s.starttls() 
  # Authentication 
  s.login(email_id, app_password) 

  iteration=0 
  while(any(dir_status.values())):
    iteration+=1
    for log_dir,status in dir_status.items():
      if status:
        updated_count=len(os.listdir(log_dir))
        if (updated_count==dir_count[log_dir]):
          print('Test:%s has failed'%(os.path.basedir(log_dir)))
          dir_status[log_dir]=False
          s.sendmail(email_id,email_id,'Subject: Test failed:{}\n\n{Please check.}'.format(os.path.basedir(log_dir)))
        else:
          dir_count[log_dir]=updated_count
    time.sleep(1800)
    if (iteration%2)==0:
      update_msg=''
      for log_dir,status in dir_status.items():
        if status:
          updated_count=len(os.listdir(log_dir))
          update_msg+='test dir:%s count:%d\n'%(os.path.basename(log_dir),updated_count)
      s.sendmail(email_id,email_id,'Subject: Test Update\n\n{}'.format(update_msg))
  s.quit()

if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to launch test monitoring script')
  parser.add_argument('emailId',help='emailId')
  parser.add_argument('password',help='app password')
  parser.add_argument('log_dirs',nargs='*',help='log dirs to monitor')
  args=parser.parse_args()
  monitor(args.emailId,args.password,args.log_dirs)
