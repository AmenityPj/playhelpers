#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "UnInstalling External requirements"
pip uninstall -r ../requirements_external_name.txt -y
source "$(dirname "$0")/deactivate_vir_env.sh"

