#!/bin/bash

ps -ef | grep -v grep | grep -v kill.yml | grep -w execute_vertex.py  | while read -r op; 
do
  pid=`echo $op | awk '{print $2}'`
  kill -9  $pid
done
