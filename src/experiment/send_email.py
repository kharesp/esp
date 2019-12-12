import smtplib,time,os,argparse

def monitor(email_id,app_password,log_dirs):
  dir_count={}
  dir_status={log_dir:True for log_dir in log_dirs}

  for log_dir in log_dirs:
    dir_count[log_dir]=len(os.listdir(log_dir))
  print(dir_count)

  def send_email(subject,body):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(email_id, app_password) 
    s.sendmail(email_id,email_id,'Subject: {}\n\n{}'.format(subject,body))
    s.quit()

  iteration=0 
  while(any(dir_status.values())):
    iteration+=1
    time.sleep(1800)
    for log_dir,status in dir_status.items():
      if status:
        updated_count=len(os.listdir(log_dir))
        if (updated_count==dir_count[log_dir]):
          print('Test:%s has failed'%(os.path.basename(log_dir)))
          dir_status[log_dir]=False
          send_email('Test failed:%s'%(os.path.basename(log_dir)),'Please check')
        else:
          dir_count[log_dir]=updated_count
          print('Updated test count for %s to %d'%(os.path.basename(log_dir),updated_count))
    if (iteration%2)==0:
      update_msg=''
      for log_dir,status in dir_status.items():
        if True:
          updated_count=len(os.listdir(log_dir))
          update_msg+='test dir:%s count:%d\n'%(os.path.basename(log_dir),updated_count)
      send_email('Test Update',update_msg)
      print('Sending update:\n%s'%(update_msg))

if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to launch test monitoring script')
  parser.add_argument('emailId',help='emailId')
  parser.add_argument('password',help='app password')
  parser.add_argument('log_dirs',nargs='*',help='log dirs to monitor')
  args=parser.parse_args()
  monitor(args.emailId,args.password,args.log_dirs)
