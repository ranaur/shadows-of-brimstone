#!/bin/bash

NAME_1=div1.png
NAME_2=div2.png
NAME_3=div3.png

if [ $# -ne 3 ] ; then
    cat << __HELP__
usage: $(basename "$0") file1 file2 file3
Copies files to $NAME_1 $NAME_2 $NAME_3, respectively

__HELP__
    exit -1
fi

cp "$1" "$NAME_1"
cp "$2" "$NAME_2"
cp "$3" "$NAME_3"
