#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"
python -m pip install --upgrade pip
source "$(dirname "$0")/deactivate_vir_env.sh"

