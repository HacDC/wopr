#!/bin/bash

# selfserve_gateway.sh
# requires:
#   directory: cgi-bin
#   with <cgi script> in cgi-bin
#   and <cgi-script> executable by the user that runs this script
###
usage="$0 [-p <port>] [-d <http root directory>] [-h|--help]"

TEMP=`getopt -o d:p:h --long help -n "$(basename $0)" -- "$@"`

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"

while true ;do
	case "$1" in
		-d)
			SRV_DIR=$2
			shift
			;;
		-p)
			PORT=$2
            shift
            ;;
		-h|--help)
			echo $usage
			exit 1
			;;
		--) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
		esac
done



SRV_DIR=${SRV_DIR:=`pwd`}
PORT=${PORT:=8000}

# selfserve_gateway.sh
# requires:
#   directory: cgi-bin
#   with <cgi script> in cgi-bin
#   and <cgi-script> executable by the user that runs this script
###

python -m CGIHTTPServer ${PORT}
