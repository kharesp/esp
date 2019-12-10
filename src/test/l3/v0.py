import sys
sys.path.append('src/dag')
sys.path.append('src/vertices')
import vertex,source

v0=source.Source('0',
  vertex.Graph('l3',{
    '0':vertex.ZmqConnector('129.59.105.42',5555),
    '1':vertex.ZmqConnector('129.59.105.42',6666),
  }),
  None,
  '/home/kharesp/workspace/python/esp/log',
  '/home/kharesp/workspace/python/esp/ocr_plates/selected_plates',
  1,
  180)
v0.execute()
