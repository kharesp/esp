import sys
sys.path.append('src/experiment')
import run

for op in ['noop','fib','bf','eqh','clahe','seg','lpr']:
  print('\n\nTesting operator:%s'%(op))
  exp=run.Experiment('log/operator_benchmark/%s'%(op),\
    '192.168.88.87:2181',\
    '/opbench',\
    '/home/pi/workspace/python/esp/log/operator_benchmark/%s'%(op))
  exp.run()
