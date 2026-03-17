#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "Installing Build requirements"
pip install -r ../requirements_build.txt
source "$(dirname "$0")/deactivate_vir_env.sh"

