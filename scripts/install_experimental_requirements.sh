#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "Installing Experimental requirements"
pip install -r ../requirements_experimental.txt
source "$(dirname "$0")/deactivate_vir_env.sh"

