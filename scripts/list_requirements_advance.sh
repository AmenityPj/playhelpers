#!/bin/bash

# --- ARGUMENT CHECK ---
# Usage: list_requirements_advance.sh [true/false]

run_env_scripts="true"

# If the user types 'false' (case-insensitive), then disable the env scripts
if [[ "${1,,}" == "false" ]]; then
    run_env_scripts="false"
    echo "[STATUS] Env Scripts are DISABLED via parameter"
else
    echo "[STATUS] Env Scripts are ENABLED Default or 'true' passed"
fi

# Run Env Stuff only when parameter is set
if [[ "$run_env_scripts" == "true" ]]; then
    echo "Calling activate"
    source "$(dirname "$0")/activate_vir_env.sh"
fi

# Read vir_env_name from the config file
output_path="logs"
vir_env_path=$(cat config_vir_env.ini)
vir_env_name=$(basename "$vir_env_path")

export_path="$output_path/requirements_freeze_${vir_env_name}.txt"
echo "Export Path: $export_path"

echo "Listing requirements"
pip list

pip freeze > "$export_path"

if [[ "$run_env_scripts" == "true" ]]; then
    source "$(dirname "$0")/deactivate_vir_env.sh"
fi

