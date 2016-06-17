export FLASK_ENV=dev
export FLASK_APP=planet/commands.py
export FLASK_DEBUG=1

arg=$1

if [[ $arg == "" ]]; then
     arg="run"
 fi 

flask $arg