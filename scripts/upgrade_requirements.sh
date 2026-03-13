#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
python -m pip install --upgrade pip
echo "Upgrading requirements"
pip install -r ../requirements.txt --upgrade
source "$(dirname "$0")/deactivate_vir_env.sh"

