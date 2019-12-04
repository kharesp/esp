import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,source

v0=source.Source('0',
  vertex.Graph('l5',{
    '0':vertex.ZmqConnector('192.168.88.88',5555),
    '1':vertex.ZmqConnector('192.168.88.88',6666),
    '2':vertex.ZmqConnector('192.168.88.88',7777),
    '3':vertex.ZmqConnector('192.168.88.88',8888),
  }),
  None,
  '/home/pi/workspace/python/data/cars',
  '.bmp',
  1)
v0.execute()
