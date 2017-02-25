#!/bin/sh
arg=$1

if [[ $arg == "" ]]; then
     arg="run"
 fi 

export FLASK_ENV=production
export FLASK_APP=planet.commands

flask $arg