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

if [ ! -d ".pyang" ]; then
  printf -- "\033[32;1m>>> Setup venv \033[0m \n"
  python3 -m venv .pyang
  ./.pyang/bin/python3 -m pip install --upgrade pip
  ./.pyang/bin/python3 -m pip install pyang
fi

source .pyang/bin/activate
clear
printf -- "\033[32;1m>>> pyang version \033[0m \n"
pyang --version
printf -- "YANG_MODPATH: $YANG_MODPATH \n"
printf -- "\033[32;1m>>> Tree format \033[0m \n"
pyang --format tree $1/src/yang/*.yang --canonical --strict
printf -- "\033[32;1m>>> YANG format \033[0m \n"
pyang --format yang --keep-comments $1/src/yang/*.yang --yang-canonical --strict
printf -- "\033[32;1m>>> Linting results \033[0m \n"
pyang --lint --canonical --strict --max-line-length 160 $1/src/yang/*.yang
printf -- "\033[32m✅  DONE 🏁\033[0m\n";
#
# Create uml diagram (doesn't work)
#
# pyang --format uml $1/src/yang/*.yang -o my.uml
# java -jar plantuml.7997.jar my.uml
# open img/mychmod.png
