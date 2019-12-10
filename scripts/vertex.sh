#!/bin/bash
if [ $# -ne 5 ]; then
  echo 'usage:' $0 'gid_vid vertex_description zk_connector zk_dir log_dir' 
  exit 1
fi

gid_vid=$1
vertex_description="${2//\\/}"
zk_connector=$3
zk_dir=$4
log_dir=$5

cd /home/pi/workspace/python/esp

gid="$(cut -d'_' -f1 <<<$gid_vid)"
vid="$(cut -d'_' -f2 <<<$gid_vid)"

mkdir -p $log_dir/$gid/err
mkdir -p $log_dir/$gid/dag


python3.6 src/experiment/execute_vertex.py $gid $vertex_description $zk_connector $zk_dir $log_dir/$gid/dag  1>$log_dir/$gid/err/"$vid".log 2>&1
