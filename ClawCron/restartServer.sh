#!/bin/bash

curdir=`pwd`
scpdir=$(cd `dirname $0`; pwd)

cd $scpdir
#kill -9 `cat CronServer.pid`
#rm CronServer.pid

this_uid=`whoami`
`ps -ef|grep ${this_uid} | grep dispatcher.py |awk '{print $2}' | xargs kill`

nohup python dispatcher.py > ./logs/claw_cron.log 2>&1 &
#echo $! | cat - > CronServer.pid

pid_count=`ps -ef|grep ${this_uid} | grep -v grep | grep dispatcher.py |awk '{print $2}'| wc -l`
#echo $pid_count
if [ $pid_count -gt 0  ] ;
then
    echo -n "starting cron ... "
    sleep 1
    echo -e "\033[32;40;5;1m  [DONE]\033[0m "
else
    echo "restart failed"
fi
cd $curdir
