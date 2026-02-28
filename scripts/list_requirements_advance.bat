@echo OFF
:: --- ARGUMENT CHECK ---
:: Usage: list_requirements.bat [true/false]

SET "run_env_scripts=true"

:: If the user types 'False' (case-insensitive), then disable the env scripts
IF /I "%~1"=="FALSE" (
    SET "run_env_scripts=false"
    echo [STATUS] Env Scripts are DISABLED via parameter
) ELSE (
    echo [STATUS] Env Scripts are ENABLED Default or 'True' passed
)

@echo ON
:: Run Env Stuff only when parameter is set
IF "!run_env_scripts!"=="true" (
    echo Calling acrtivzte
    call activate_vir_env.bat
)

set export_path=%output_path%/requirements_freeze_%vir_env_name%.txt
echo Export Path: %export_path%

echo Listing requirements
pip list

pip freeze > %export_path%

IF "!run_env_scripts!"=="true" (
    call deactivate_vir_env.bat
)
