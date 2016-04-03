export FLASK=dev

PREFIX=$(cd "$(dirname "$0")"; pwd)

arg=$1

if [[ $arg == "" ]]; then
     arg="runserver"
 fi 

python $PREFIX/manage.py $arg