#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "Installing requirements"
pip install -r ../requirements.txt
source "$(dirname "$0")/deactivate_vir_env.sh"

