import rx,zmq

MSG_TYPE_ERR=-1
MSG_TYPE_END=0
MSG_TYPE_DATA=1

def from_topic(topics,ip_addrs,ports):
  def _receive(observer,scheduler=None):
    try: 
      context=zmq.Context()
      sockets=[]
      for i in range(len(ip_addrs)):
        socket=context.socket(zmq.SUB)
        socket.connect('tcp://%s:%d'%(ip_addrs[i],ports[i]))
        socket.setsockopt_string(zmq.SUBSCRIBE,topics[i])
        sockets.append(socket)

      poller=zmq.Poller() 
      for socket in sockets:
        poller.register(socket,zmq.POLLIN)

      completed_count=0
      continue_polling=True
      while continue_polling:
        data_in=dict(poller.poll())
        for idx,socket in enumerate(sockets):
          if socket in data_in and data_in[socket]==zmq.POLLIN:
            topic_name,msg=socket.recv_string().split()
            code=int(msg.partition(',')[0])
            if code==MSG_TYPE_END:
              completed_count+=1
              if completed_count==len(sockets):
                continue_polling=False
                observer.on_completed()
            elif code==MSG_TYPE_ERR:
              observer.on_error(Exception(msg.partition(',')[1]))
              continue_polling=False
            else:
              observer.on_next(msg)
    except Exception as err:
        continue_polling=False
        observer.on_error(err)
    finally:
      for socket in sockets:
        poller.unregister(socket)
        socket.close()
      if context:
        context.destroy()
  return rx.Observable(_receive)

def to_topic(topic,ip_addr,port):
  def _publish(source):
    context=zmq.Context()
    pub_socket=context.socket(zmq.PUB)
    pub_socket.bind('tcp://*:%d'%(port))
    def subscribe(observer,scheduler=None):
      def on_next(msg):
        pub_socket.send_string('%s %s'%(topic,msg))
      def on_error(err):
        pub_socket.send_string('%s %d,%s'%(topic,MSG_TYPE_ERR,err))
        pub_socket.close()
        context.destroy()
        observer.on_error(err)
      def on_completed():
        pub_socket.send_string('%s %d'%(topic,MSG_TYPE_END))
        pub_socket.close()
        context.destroy()
        observer.on_completed()
      return source.subscribe(on_next,on_error,on_completed,scheduler)
    return rx.create(subscribe)
  return _publish
