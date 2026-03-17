#!/bin/bash

read -p "Please Enter Project Version: " versionValue

# Add quotes if not present
if [[ "$versionValue" != \"*\" ]]; then
    versionValue="\"$versionValue\""
fi

bash "$(dirname "$0")/version_specific.sh" --newversion "Setting Specific Version" "$versionValue"

