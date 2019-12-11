#!/bin/bash
if [ $# -ne 3 ]; then
  echo 'usage:' $0 'zk_connector zk_dir log_dir' 
  exit 1
fi

zk_connector=$1
zk_dir=$2
log_dir=$3

cd /home/pi/workspace/python/esp

mkdir -p $log_dir/util

python3.6 src/sysstat/sysstat.py $zk_connector $zk_dir $log_dir/util 
