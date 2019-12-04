import opencv,sys
sys.path.append('src/dag')
import vertex

v3=opencv.Add('3',vertex.Graph('g1',\
  {'0':vertex.ZmqConnector('129.59.105.42',5555),
   '1':vertex.ZmqConnector('129.59.105.42',6666),
   '2':vertex.ZmqConnector('129.59.105.42',7777),
   '3':vertex.ZmqConnector('129.59.105.42',8888),
   '4':vertex.ZmqConnector('129.59.105.42',9999)}),
  ['1','2'])
v3.execute()
