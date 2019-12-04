import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,opencv

v1=opencv.GrayScale('1',
  vertex.Graph('l4',{
      '0':vertex.ZmqConnector('192.168.88.88',5555),
      '1':vertex.ZmqConnector('192.168.88.88',6666),
      '2':vertex.ZmqConnector('192.168.88.88',7777),
    }),
  ['0'])
v1.execute()
