echo Attempting to activate existing Virtual Environment

SET /P VIR_ENV_PATH=<config_vir_env.ini
call %VIR_ENV_PATH%\Scripts\activate

echo .
echo Python Version
python --version

echo .
echo Python Location
which python