echo Attempting to activate existing Virtual Environment

SET output_path=logs
SET /P vir_env_path=<config_vir_env.ini
for %%A in ("%vir_env_path%") do set "vir_env_name=%%~nxA"

call %vir_env_path%\Scripts\activate

echo .
echo Python Version
python --version

echo .
echo Python Location
which python

IF NOT EXIST %output_path% MD %output_path%

echo .