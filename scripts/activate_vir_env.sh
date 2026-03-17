#!/bin/bash

echo "Attempting to activate existing Virtual Environment"

output_path="logs"

# 1. Read the first line of the config file into a variable
vir_env_path=$(head -n 1 config_vir_env.ini)
# 2. Extract the base directory name
vir_env_name=$(basename "$vir_env_path")

# Debugging
# echo "Virtual Environment Path: $vir_env_path"
# echo "Virtual Environment Name: $vir_env_name"

source "$vir_env_path/bin/activate"

echo ""
echo "Python Version"
python --version

echo ""
echo "Python Location"
which python

if [ ! -d "$output_path" ]; then
    mkdir -p "$output_path"
	echo "$output_path%" Directory created successfully.
fi

echo ""