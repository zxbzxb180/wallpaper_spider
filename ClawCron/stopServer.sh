#!/bin/bash

curdir=`pwd`
scpdir=$(cd `dirname $0`; pwd)

cd $scpdir
#kill -9 `cat CronServer.pid`
#rm CronServer.pid

this_uid=`whoami`
`ps -ef|grep ${this_uid} | grep dispatcher.py |awk '{print $2}' | xargs kill`

pid_count=`ps -ef|grep ${this_uid} | grep -v grep | grep dispatcher.py |awk '{print $2}'| wc -l`
if [ $pid_count -gt 0  ];then
    echo 'stop failed'
elif [ $pid_count -eq 0 ]; then
    echo 'the process had stoped'
else
    echo 'stop success'
fi
cd $curdir
