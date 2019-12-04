import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,opencv

v2=opencv.GrayScale('2',
  vertex.Graph('l5',{
      '0':vertex.ZmqConnector('192.168.88.88',5555),
      '1':vertex.ZmqConnector('192.168.88.88',6666),
      '2':vertex.ZmqConnector('192.168.88.88',7777),
      '3':vertex.ZmqConnector('192.168.88.88',8888),
    }),
  ['1'])
v2.execute()
