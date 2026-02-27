call activate_vir_env.bat

echo .
echo Listing requirements
pip list

SET /P VIR_ENV_PATH=<config_vir_env.ini
set export_path=%VIR_ENV_PATH%\requirements_freeze.txt

echo Exporting requirements to %export_path%
pip freeze > %export_path%

call deactivate_vir_env.bat
