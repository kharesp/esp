import sys
sys.path.append('src/experiment')
import run

for op in ['noop','fib','bf','eqh','clahe','seg','lpr','bf_lpr','eqh_lpr','clahe_lpr']:
  print('\n\nTesting operator(distributed):%s'%(op))
  exp=run.Experiment('log/operator_benchmark/distributed/%s'%(op),\
    '192.168.88.87:2181',\
    '/opbench',\
    '/home/pi/workspace/python/esp/log/operator_benchmark/distributed/%s'%(op))
  exp.run()

  print('\n\nTesting operator(single_host):%s'%(op))
  exp=run.Experiment('log/operator_benchmark/single_host/%s'%(op),\
    '192.168.88.87:2181',\
    '/opbench',\
    '/home/pi/workspace/python/esp/log/operator_benchmark/single_host/%s'%(op))
  exp.run()
