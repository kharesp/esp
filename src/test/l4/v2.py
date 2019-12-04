import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,opencv

v2=opencv.NoOp('2',
  vertex.Graph('l4',{
      '0':vertex.ZmqConnector('192.168.88.88',5555),
      '1':vertex.ZmqConnector('192.168.88.88',6666),
      '2':vertex.ZmqConnector('192.168.88.88',7777),
    }),
  ['1'])
v2.execute()
