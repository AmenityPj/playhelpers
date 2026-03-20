@echo off
:: =============================================================================
:: manage.bat — Unified management script for playhelpers
::
:: Usage:
::   manage.bat <command> [options]
::
:: Commands:
::   env [type]              Manage virtual environment (default: activate)
::                             types: activate | deactivate
::   install [type]          Install requirements (default: requirements)
::                             types: requirements | build | cicd | experimental | external
::   uninstall [type]        Uninstall requirements (default: external)
::                             types: experimental | external
::   upgrade [type]          Upgrade packages (default: pip)
::                             types: pip | requirements | internal
::   list [true|false]       List & freeze installed packages (default: true)
::                             true  = activate env, list, freeze, deactivate
::                             false = list & freeze without touching env
::   run-tests [type]        Run tests (default: full)
::                             types: full | unit | package
::   version [type]          Manage project version (default: set)
::                             types: set | create | dev | patch | specific
::                             version specific <flag> <desc> [value]
::   help                    Show this help message
::
:: Aliases:
::   commands: e, i, un, up, ls, test, rt, ver, v, h
::   types: req, exp, ext, int, pkg, spec and yes/no boolean variants
:: =============================================================================

setlocal EnableExtensions EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "output_path=logs"
set "python_bin=python"

set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=help"
shift

REM Command aliases
if /I "%COMMAND%"=="e" set "COMMAND=env"
if /I "%COMMAND%"=="i" set "COMMAND=install"
if /I "%COMMAND%"=="ins" set "COMMAND=install"
if /I "%COMMAND%"=="un" set "COMMAND=uninstall"
if /I "%COMMAND%"=="rm" set "COMMAND=uninstall"
if /I "%COMMAND%"=="u" set "COMMAND=upgrade"
if /I "%COMMAND%"=="up" set "COMMAND=upgrade"
if /I "%COMMAND%"=="l" set "COMMAND=list"
if /I "%COMMAND%"=="ls" set "COMMAND=list"
if /I "%COMMAND%"=="t" set "COMMAND=unit-tests"
if /I "%COMMAND%"=="test" set "COMMAND=unit-tests"
if /I "%COMMAND%"=="tests" set "COMMAND=unit-tests"
if /I "%COMMAND%"=="ut" set "COMMAND=unit-tests"
if /I "%COMMAND%"=="v" set "COMMAND=version"
if /I "%COMMAND%"=="ver" set "COMMAND=version"
if /I "%COMMAND%"=="h" set "COMMAND=help"
if /I "%COMMAND%"=="-h" set "COMMAND=help"
if /I "%COMMAND%"=="--help" set "COMMAND=help"

if /I "%COMMAND%"=="env" goto :cmd_env
if /I "%COMMAND%"=="install" goto :cmd_install
if /I "%COMMAND%"=="uninstall" goto :cmd_uninstall
if /I "%COMMAND%"=="upgrade" goto :cmd_upgrade
if /I "%COMMAND%"=="list" goto :cmd_list
REM TODO: This needs to be fixed
REM if /I "%COMMAND%"=="unit-tests" goto :cmd_unit_tests
if /I "%COMMAND%"=="version" goto :cmd_version
if /I "%COMMAND%"=="help" goto :cmd_help

echo ERROR: Unknown command '%COMMAND%'
echo Run 'manage.bat help' for usage.
exit /b 1

:: ---------------------------------------------------------------------------
:: :_activate  (internal — CALL only)
:: ---------------------------------------------------------------------------
:_activate
    echo Attempting to activate existing Virtual Environment
    SET "output_path=logs"
    SET /P vir_env_path=<"%SCRIPT_DIR%\config_vir_env.ini"
    FOR %%A IN ("%vir_env_path%") DO SET "vir_env_name=%%~nxA"
    CALL "%vir_env_path%\Scripts\activate"
    echo.
    echo Python Version
    python --version
    echo.
    echo Python Location
    where python
    IF NOT EXIST "%SCRIPT_DIR%\%output_path%" (
        MD "%SCRIPT_DIR%\%output_path%"
        echo %SCRIPT_DIR%\%output_path% Directory created successfully.
    )
    echo.
    GOTO :EOF

:: ---------------------------------------------------------------------------
:: :_deactivate  (internal — CALL only)
:: ---------------------------------------------------------------------------
:_deactivate
    echo Attempting to deactivate existing (and activated) Virtual Environment
    CALL "%vir_env_path%\Scripts\deactivate"
    GOTO :EOF

:: ---------------------------------------------------------------------------
:: :_version_specific  (internal — CALL only)
::   %1 = flag  %2 = description  %3 = version value (optional)
:: ---------------------------------------------------------------------------
:_version_specific
    SET /P _pkg_name=<"%SCRIPT_DIR%\..\package_name.txt"
    SET "_pkg_path=%SCRIPT_DIR%\..\%_pkg_name%"
    SET "_cmd=python -m incremental.update --path=%_pkg_path% %_pkg_name%"
    CALL :_activate
    echo %~2
    %_cmd% %~1%~3
    CALL :_deactivate
    GOTO :EOF

:: ---------------------------------------------------------------------------
:cmd_env
    SET "ENV_TYPE=%~1"
    IF "%ENV_TYPE%"=="" SET "ENV_TYPE=activate"
    IF /I "%ENV_TYPE%"=="a" SET "ENV_TYPE=activate"
    IF /I "%ENV_TYPE%"=="act" SET "ENV_TYPE=activate"
    IF /I "%ENV_TYPE%"=="d" SET "ENV_TYPE=deactivate"
    IF /I "%ENV_TYPE%"=="deact" SET "ENV_TYPE=deactivate"
    IF /I "%ENV_TYPE%"=="activate"   ( CALL :_activate   & GOTO end )
    IF /I "%ENV_TYPE%"=="deactivate" ( CALL :_deactivate & GOTO end )
    echo ERROR: Unknown env type '%ENV_TYPE%'
    echo Valid types: activate ^| deactivate
    EXIT /B 1

:: ---------------------------------------------------------------------------
:cmd_install
    SET "INSTALL_TYPE=%~1"
    IF "%INSTALL_TYPE%"=="" SET "INSTALL_TYPE=requirements"
    IF /I "%INSTALL_TYPE%"=="r" SET "INSTALL_TYPE=requirements"
    IF /I "%INSTALL_TYPE%"=="req" SET "INSTALL_TYPE=requirements"
    IF /I "%INSTALL_TYPE%"=="b" SET "INSTALL_TYPE=build"
    IF /I "%INSTALL_TYPE%"=="ci" SET "INSTALL_TYPE=cicd"
    IF /I "%INSTALL_TYPE%"=="x" SET "INSTALL_TYPE=experimental"
    IF /I "%INSTALL_TYPE%"=="exp" SET "INSTALL_TYPE=experimental"
    IF /I "%INSTALL_TYPE%"=="e" SET "INSTALL_TYPE=external"
    IF /I "%INSTALL_TYPE%"=="ext" SET "INSTALL_TYPE=external"
    CALL :_activate
    IF /I "%INSTALL_TYPE%"=="requirements" (
        echo Installing requirements
        pip install -r "%SCRIPT_DIR%\..\requirements.txt"
        GOTO _install_done
    )
    IF /I "%INSTALL_TYPE%"=="build" (
        echo Installing Build requirements
        pip install -r "%SCRIPT_DIR%\..\requirements_build.txt"
        GOTO _install_done
    )
    IF /I "%INSTALL_TYPE%"=="cicd" (
        echo Installing CI CD requirements
        pip install -r "%SCRIPT_DIR%\..\requirements_cicd.txt"
        GOTO _install_done
    )
    IF /I "%INSTALL_TYPE%"=="experimental" (
        echo Installing Experimental requirements
        pip install -r "%SCRIPT_DIR%\..\requirements_experimental.txt"
        GOTO _install_done
    )
    IF /I "%INSTALL_TYPE%"=="external" (
        echo Installing External requirements
        pip install -r "%SCRIPT_DIR%\..\requirements_external.txt"
        GOTO _install_done
    )
    echo ERROR: Unknown install type '%INSTALL_TYPE%'
    echo Valid types: requirements ^| build ^| cicd ^| experimental ^| external
    CALL :_deactivate & EXIT /B 1
:_install_done
    CALL :_deactivate
    GOTO end

:: ---------------------------------------------------------------------------
:cmd_uninstall
    SET "UNINSTALL_TYPE=%~1"
    IF "%UNINSTALL_TYPE%"=="" SET "UNINSTALL_TYPE=external"
    IF /I "%UNINSTALL_TYPE%"=="x" SET "UNINSTALL_TYPE=experimental"
    IF /I "%UNINSTALL_TYPE%"=="exp" SET "UNINSTALL_TYPE=experimental"
    IF /I "%UNINSTALL_TYPE%"=="e" SET "UNINSTALL_TYPE=external"
    IF /I "%UNINSTALL_TYPE%"=="ext" SET "UNINSTALL_TYPE=external"
    CALL :_activate
    IF /I "%UNINSTALL_TYPE%"=="experimental" (
        echo UnInstalling Experimental requirements
        pip uninstall -r "%SCRIPT_DIR%\..\requirements_experimental_name.txt" -y
        GOTO _uninstall_done
    )
    IF /I "%UNINSTALL_TYPE%"=="external" (
        echo UnInstalling External requirements
        pip uninstall -r "%SCRIPT_DIR%\..\requirements_external_name.txt" -y
        GOTO _uninstall_done
    )
    echo ERROR: Unknown uninstall type '%UNINSTALL_TYPE%'
    echo Valid types: experimental ^| external
    CALL :_deactivate & EXIT /B 1
:_uninstall_done
    CALL :_deactivate
    GOTO end

:: ---------------------------------------------------------------------------
:cmd_upgrade
    SET "UPGRADE_TYPE=%~1"
    IF "%UPGRADE_TYPE%"=="" SET "UPGRADE_TYPE=pip"
    IF /I "%UPGRADE_TYPE%"=="p" SET "UPGRADE_TYPE=pip"
    IF /I "%UPGRADE_TYPE%"=="r" SET "UPGRADE_TYPE=requirements"
    IF /I "%UPGRADE_TYPE%"=="req" SET "UPGRADE_TYPE=requirements"
    IF /I "%UPGRADE_TYPE%"=="i" SET "UPGRADE_TYPE=internal"
    IF /I "%UPGRADE_TYPE%"=="int" SET "UPGRADE_TYPE=internal"
    CALL :_activate
    IF /I "%UPGRADE_TYPE%"=="pip" (
        python.exe -m pip install --upgrade pip
        GOTO _upgrade_done
    )
    IF /I "%UPGRADE_TYPE%"=="requirements" (
        python.exe -m pip install --upgrade pip
        echo Upgrading requirements
        pip install -r "%SCRIPT_DIR%\..\requirements.txt" --upgrade
        GOTO _upgrade_done
    )
    IF /I "%UPGRADE_TYPE%"=="internal" (
        echo Upgrading internal requirements
        pip install -r "%SCRIPT_DIR%\..\requirements_internal_lib.txt" --upgrade
        GOTO _upgrade_done
    )
    echo ERROR: Unknown upgrade type '%UPGRADE_TYPE%'
    echo Valid types: pip ^| requirements ^| internal
    CALL :_deactivate & EXIT /B 1
:_upgrade_done
    CALL :_deactivate
    GOTO end

:: ---------------------------------------------------------------------------
:cmd_list
    SET "RUN_ENV=%~1"
    IF "%RUN_ENV%"=="" SET "RUN_ENV=true"
    IF /I "%RUN_ENV%"=="t" SET "RUN_ENV=true"
    IF /I "%RUN_ENV%"=="1" SET "RUN_ENV=true"
    IF /I "%RUN_ENV%"=="y" SET "RUN_ENV=true"
    IF /I "%RUN_ENV%"=="yes" SET "RUN_ENV=true"
    IF /I "%RUN_ENV%"=="f" SET "RUN_ENV=false"
    IF /I "%RUN_ENV%"=="0" SET "RUN_ENV=false"
    IF /I "%RUN_ENV%"=="n" SET "RUN_ENV=false"
    IF /I "%RUN_ENV%"=="no" SET "RUN_ENV=false"

    :: Always load venv vars
    SET "output_path=logs"
    SET /P vir_env_path=<"%SCRIPT_DIR%\config_vir_env.ini"
    FOR %%A IN ("%vir_env_path%") DO SET "vir_env_name=%%~nxA"

    IF /I "%RUN_ENV%"=="false" (
        echo [STATUS] Env activation DISABLED via parameter
    ) ELSE (
        SET "RUN_ENV=true"
        echo [STATUS] Env activation ENABLED (default or 'true' passed^)
        CALL :_activate
    )

    SET "export_path=%SCRIPT_DIR%\%output_path%\requirements_freeze_%vir_env_name%.txt"
    echo Export Path: %export_path%
    echo Listing requirements
    pip list
    echo Freezing requirements to %export_path%
    pip freeze > "%export_path%"

    IF /I "!RUN_ENV!"=="true" CALL :_deactivate
    GOTO end

:: ---------------------------------------------------------------------------
:cmd_run_tests
    SET "RUN_TYPE=%~1"
    IF "%RUN_TYPE%"=="" SET "RUN_TYPE=full"
    IF /I "%RUN_TYPE%"=="f" SET "RUN_TYPE=full"
    IF /I "%RUN_TYPE%"=="all" SET "RUN_TYPE=full"
    IF /I "%RUN_TYPE%"=="u" SET "RUN_TYPE=unit"
    IF /I "%RUN_TYPE%"=="p" SET "RUN_TYPE=package"
    IF /I "%RUN_TYPE%"=="pkg" SET "RUN_TYPE=package"

    IF /I "%RUN_TYPE%"=="full" (
        CALL :_activate
        SET "export_path=%SCRIPT_DIR%\%output_path%\run_tests_%vir_env_name%.log"
        echo Export Path: !export_path!
        echo Starting App
        cd "%SCRIPT_DIR%\.."
        python -u -m play_helpers.test.test > "!export_path!" 2>&1
        cd "%SCRIPT_DIR%"
        CALL :_deactivate
        GOTO end
    )
    IF /I "%RUN_TYPE%"=="unit" (
        CALL :_activate
        echo Starting App
        cd "%SCRIPT_DIR%\.."
        REM python -m unittest discover -s play_helpers/test
        python -m unittest play_helpers/test/test_util.py
        cd "%SCRIPT_DIR%"
        CALL :_deactivate
        GOTO end
    )
    IF /I "%RUN_TYPE%"=="package" (
        SET "env_list=..\venv_39;..\venv_314"
        SET "ini_file=%SCRIPT_DIR%\config_vir_env_default.ini"
        echo Starting the loop...
        FOR %%P IN ("%env_list:;=" "%") DO (
            SET "current_env=%%~P"
            echo current_env: !current_env!
            echo path=!current_env! > "%ini_file%"
            CALL "%SCRIPT_DIR%\manage.bat" list
            CALL "%SCRIPT_DIR%\manage.bat" run-tests full
            echo -----------------
        )
        echo Ending the loop...
        GOTO end
    )
    echo ERROR: Unknown run-tests type '%RUN_TYPE%'
    echo Valid types: full ^| unit ^| package
    EXIT /B 1

:: ---------------------------------------------------------------------------
:cmd_version
    SET "VER_TYPE=%~1"
    IF "%VER_TYPE%"=="" SET "VER_TYPE=set"
    IF /I "%VER_TYPE%"=="s" SET "VER_TYPE=set"
    IF /I "%VER_TYPE%"=="c" SET "VER_TYPE=create"
    IF /I "%VER_TYPE%"=="init" SET "VER_TYPE=create"
    IF /I "%VER_TYPE%"=="d" SET "VER_TYPE=dev"
    IF /I "%VER_TYPE%"=="p" SET "VER_TYPE=patch"
    IF /I "%VER_TYPE%"=="sp" SET "VER_TYPE=specific"
    IF /I "%VER_TYPE%"=="spec" SET "VER_TYPE=specific"

    IF /I "%VER_TYPE%"=="set" (
        SET /P versionValue=Please Enter Project Version:
        SET "versionValue2=!versionValue:~0,1!"
        IF NOT "!versionValue2!"==^"^" SET versionValue="!versionValue!"
        SET "versionValue2=!versionValue:~-1!"
        IF NOT "!versionValue2!"==^"^" SET versionValue=!versionValue!"
        CALL :_version_specific --newversion "Setting Specific Version" !versionValue!
        GOTO end
    )
    IF /I "%VER_TYPE%"=="create" (
        CALL :_version_specific --create "Creating Version File (Should be used for First Time only)"
        CALL :_version_specific --newversion "Setting Default Version" 1.0.0
        GOTO end
    )
    IF /I "%VER_TYPE%"=="dev" (
        CALL :_version_specific --dev "Setting Dev Version (Should be used for Internal versions only)"
        GOTO end
    )
    IF /I "%VER_TYPE%"=="patch" (
        CALL :_version_specific --patch "Setting Patch Version (Should be used for Public versions only)"
        GOTO end
    )
    IF /I "%VER_TYPE%"=="specific" (
        CALL :_version_specific %~2 %~3 %~4
        GOTO end
    )
    echo ERROR: Unknown version type '%VER_TYPE%'
    echo Valid types: set ^| create ^| dev ^| patch ^| specific
    EXIT /B 1

:: ---------------------------------------------------------------------------
:cmd_help
    findstr /B "::" "%~f0" | findstr /V "^::$"
    GOTO end

:: ---------------------------------------------------------------------------
:end
ENDLOCAL

