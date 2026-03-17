#!/bin/bash

source "$(dirname "$0")/activate_vir_env.sh"

export_path="$output_path/list_requirements_${vir_env_name}.log"
echo "Export Path: $export_path"

echo "Listing requirements"
pip list

echo "Exporting requirements to $export_path"
pip freeze > "$export_path"

source "$(dirname "$0")/deactivate_vir_env.sh"

