export FLASK_ENV=prod
export FLASK_APP=planet.commands

arg=$1

if [[ $arg == "" ]]; then
     arg="run"
 fi 

flask $arg