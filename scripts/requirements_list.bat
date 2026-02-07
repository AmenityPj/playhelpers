call activate_vir_env.bat

echo .
echo Python Version
python --version

echo .
echo Python Location
which python

echo .
echo Listing requirements
pip list

call deactivate_vir_env.bat
