import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,sink

v2=sink.Sink('2',
  vertex.Graph('l3',{
    '0':vertex.ZmqConnector('192.168.88.88',5555),
    '1':vertex.ZmqConnector('192.168.88.88',6666),
  }),
  ['1'],
  '/home/pi/workspace/python/esp')
v2.execute()
