#!/bin/bash

export DOCKER_HOST=`/sbin/ifconfig|grep 'inet addr'|grep -v '127.0.0.1'|awk '{print $2}'|awk -F '.' '{print $3"_"$4}'`
needchange_via=`ip r|grep default|grep "10.200.0.1"`
if [ "x$needchange_via" == "x" ]
then
        echo "not need change via"
else
        echo "need change via"
        /sbin/ip r del default via 10.200.0.1 dev eth0
        /sbin/ip r add default via 10.200.0.243 dev eth0
fi

sed -i -e '/pam_loginuid.so/s/^/#/' /etc/pam.d/cron
/usr/bin/crontab /root/rootcron
/etc/init.d/cron start

cd /home/scrapyer/seedgenerator/newsrc/ClawCron
ln -sf /home/scrapyer/settings.py /home/scrapyer/seedgenerator/newsrc/settings.py
python dispatcher.py 

