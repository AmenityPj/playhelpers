call activate_vir_env.bat
echo Installing CI CD requirements
pip install -r ..\requirements_cicd.txt
call deactivate_vir_env.bat
