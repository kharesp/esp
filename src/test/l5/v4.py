import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,sink

v4=sink.Sink('4',
  vertex.Graph('l4',{
    '0':vertex.ZmqConnector('192.168.88.88',5555),
    '1':vertex.ZmqConnector('192.168.88.88',6666),
    '2':vertex.ZmqConnector('192.168.88.88',7777),
    '3':vertex.ZmqConnector('192.168.88.88',8888),
  }),
  ['3'],
  '/home/pi/workspace/python/esp')
v4.execute()
