#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "UnInstalling Experimental requirements"
pip uninstall -r ../requirements_experimental_name.txt -y
source "$(dirname "$0")/deactivate_vir_env.sh"

