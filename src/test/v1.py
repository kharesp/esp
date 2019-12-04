import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,opencv

v1=opencv.NoOp('1',
  vertex.Graph('g1',{
      '0':vertex.ZmqConnector('192.168.88.88',5555),
      '1':vertex.ZmqConnector('192.168.88.88',6666),
    }),
  ['0'])
v1.execute()
