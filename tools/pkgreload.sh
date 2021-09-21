#!/bin/bash
set -u # fail if reference a variable that hasn’t been set
set -e # exit if a command fails
set -o pipefail # fail a pipeline if any command of pipeline failed

ncs_cli -C -u admin << EOF
packages reload force
show packages package oper-status
exit
EOF
