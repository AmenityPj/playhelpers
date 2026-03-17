#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "Installing CI CD requirements"
pip install -r ../requirements_cicd.txt
source "$(dirname "$0")/deactivate_vir_env.sh"

