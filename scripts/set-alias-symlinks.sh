#!/bin/bash 

# Given a file of aliases and  a path to a template file, create a
# symlink of each alias to the template in the CURRENT folder.

# Paul "Worthless" Nijjar, 2022-08-16

# (This does not work well for the ward listing. The following may be
# helpful: 
# for i in `/bin/ls *.html | grep -v "Ward"`; do echo $i; rm $i; done
# )

usage() {
  echo $0 [alias-file] [template-file]
  echo ""

  echo Create symlinks for each alias in the alias-file to the
  echo template file in the CURRENT folder.

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
  ln -sf $template ${a}.html
done
