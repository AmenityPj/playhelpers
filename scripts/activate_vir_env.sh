#!/bin/bash

echo "Attempting to activate existing Virtual Environment"

output_path="logs"
vir_env_path=$(cat config_vir_env.ini)
vir_env_name=$(basename "$vir_env_path")

source "$vir_env_path/bin/activate"

echo ""
echo "Python Version"
python --version

echo ""
echo "Python Location"
which python

if [ ! -d "$output_path" ]; then
    mkdir -p "$output_path"
fi

echo ""