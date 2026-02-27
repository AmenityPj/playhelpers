call activate_vir_env.bat
echo Starting App
cd ..
python -m play_helpers.test.test
cd scripts
call deactivate_vir_env.bat
