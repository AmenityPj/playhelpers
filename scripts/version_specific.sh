#!/bin/bash

# Variable Part
package_name=$(cat ../package_name.txt)

# Constant Part
package_path="../$package_name"

# Sample: python -m incremental.update --path=../play_helpers play_helpers --dev
# Sample: python -m incremental.update --path=../play_helpers play_helpers --patch
cmd_data="python -m incremental.update --path=$package_path $package_name"

# Debugging
# echo cmd_data: "$cmd_data"
# echo package_name: "$package_name"
# echo package_path: "$package_path"
# echo param1: "$1"
# echo param2: "$2"
# echo param3: "$3"
# echo Full Command: "$cmd_data $1 $3"

source "$(dirname "$0")/activate_vir_env.sh"
echo "$2"
$cmd_data "$1""$3"
source "$(dirname "$0")/deactivate_vir_env.sh"