#!/bin/sh

PATH=/opt/google-appengine:$PATH
ISBNER_HOME=`dirname $0`

trap 'kill %1' 1 2 15

dev_appserver.py -p 8081 $ISBNER_HOME &
dev_appserver.py -p 8080 $ISBNER_HOME
