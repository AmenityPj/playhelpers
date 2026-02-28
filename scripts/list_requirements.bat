call activate_vir_env.bat

set export_path=%output_path%/list_requirements_%vir_env_name%.log
echo Export Path: %export_path%

echo Listing requirements
pip list


echo Exporting requirements to %export_path%
pip freeze > %export_path%

call deactivate_vir_env.bat
