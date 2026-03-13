#!/bin/bash

versionValue="1.0.0"
bash "$(dirname "$0")/version_specific.sh" --create "Creating Version File (Should be used for First Time only)"
bash "$(dirname "$0")/version_specific.sh" --newversion "Setting Default Version" "$versionValue"

