#!/bin/bash  
A=`ps -C nginx -no-header |wc -l`
if [ $A -eq 1 ];then
        pkill keepalived
fi