#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
echo "Installing External requirements"
pip install -r ../requirements_external.txt
source "$(dirname "$0")/deactivate_vir_env.sh"

