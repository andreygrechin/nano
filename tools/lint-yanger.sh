#!/bin/bash
set -u # fail if reference a variable that hasn’t been set
set -e # exit if a command fails
set -o pipefail # fail a pipeline if any command of pipeline failed

if [ $# -ne 1 ]
then
  echo Please provide a package folder name, assuming ./ path.
  exit 1
fi
if [ ! -d "$NCS_DIR" ]
then
  echo Didn\'t find NSO main folder "$NCS_DIR"
  exit 1
fi
if [ ! -d "$(pwd)/$1" ]; then
  echo Didn\'find a package folder "./$1"
  exit 1
fi
export YANG_MODPATH=$NCS_DIR/src/ncs/yang
# export YANG_MODPATH=$NCS_DIR/packages/neds/$NED_CISCO_IOS_CLI/src/ncsc-out/modules/yang:$YANG_MODPATH
# export YANG_MODPATH=$NCS_DIR/packages/neds/$NED_CISCO_IOS_CLI_EXAMPLE/src/ncsc-out/modules/yang:$YANG_MODPATH

clear
printf -- "\033[32;1m>>> yanger version \033[0m \n"
yanger --version
printf -- "YANG_MODPATH: $YANG_MODPATH \n"

printf -- "\033[32;1m>>> Tree format \033[0m \n"
yanger --path $YANG_MODPATH --strict --format tree --tree-depth 4 $1/src/yang/*.yang

printf -- "\033[32;1m>>> YANG format \033[0m \n"
yanger --path $YANG_MODPATH --strict --yang-canonical --yang-path-comment --format yang $1/src/yang/*.yang

printf -- "\033[32;1m>>> Lint \033[0m \n"
yanger --path $YANG_MODPATH --strict $1/src/yang/*.yang

printf -- "\033[32;1m>>> Dependencies \033[0m \n"
yanger --path $YANG_MODPATH --strict --format depend $1/src/yang/*.yang

printf -- "\033[32m✅  DONE 🏁\033[0m\n";
