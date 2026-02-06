#!/bin/bash 

# Given a file of aliases and  a path to a template file, copy the
# template of each alias to the the template in the CURRENT folder. 
#
# The template should probably contain an include to a centralized
# template. (eg use "include-positions.html", not
# "position-template.html")

# Paul "Worthless" Nijjar, 2022-08-16

# (This does not work well for the ward listing. The following may be
# helpful: 
# for i in `/bin/ls *.html | grep -v "Ward"`; do echo $i; rm $i; done
# 
# FIRST run this script using position-tags and the ward template.
# THEN run the loop above to include only "Ward" listings. 
# )

usage() {
  echo $0 [alias-file] [template-file]
  echo ""

  echo Copy template-file for each alias in the alias-file to the
  echo CURRENT folder.

}

die() { 
    usage
    exit 1
}


if [ $# -ne 2 ]
then
    usage
    exit 1
fi

alias_file=$1
template=$2

echo "Aliases: $alias_file, template: $template"

if [[ ! -f $alias_file ]] 
then 
    echo $alias_file does not appear to be a file
    usage
    exit 2
fi

if [[ ! -f $template ]] 
then 
    echo $template does not appear to be a file
    usage
    exit 3
fi

aliases=$(tail +2 $alias_file | cut -f1 -d, )

for a in $aliases 
do
  cp $template ${a}.html
done
