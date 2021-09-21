#!/bin/bash
set -u # fail if reference a variable that hasn’t been set
set -e # exit if a command fails
set -o pipefail # fail a pipeline if any command of pipeline failed

ncs_load -tF p configs/backups/nso-config-backup-$(date +%Y%m%dT%H%M%S).xml
ls -l configs/backups/
