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

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

:_load_venv_vars
set "vir_env_path="
set /p vir_env_path=<"%SCRIPT_DIR%config_vir_env.ini"
if not defined vir_env_path (
    echo ERROR: Could not read '%SCRIPT_DIR%config_vir_env.ini'
    exit /b 1
)
if /I "!vir_env_path:~0,5!"=="path=" set "vir_env_path=!vir_env_path:~5!"
for %%I in ("!vir_env_path!") do set "vir_env_name=%%~nxI"
exit /b 0

:_fetch_python_version
set "python_version=unknown"
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if not errorlevel 1 set "python_bin=py -3"
) else (
    set "python_bin=python"
)
for /f "usebackq delims=" %%V in (`%python_bin% -c "import sys; print(sys.version.split()[0])" 2^>nul`) do set "python_version=%%V"
exit /b 0

:_fetch_os_type
set "os_type=windows"
exit /b 0

:_activate
echo Attempting to activate existing Virtual Environment
call :_load_venv_vars || exit /b 1

if not exist "!vir_env_path!\Scripts\activate.bat" (
    echo ERROR: activate.bat not found in '!vir_env_path!\Scripts'
    exit /b 1
)

call "!vir_env_path!\Scripts\activate.bat"
call :_fetch_python_version

echo.
echo Python Version
%python_bin% --version

echo.
echo Python Location
where python

if not exist "%SCRIPT_DIR%%output_path%" (
    mkdir "%SCRIPT_DIR%%output_path%"
    echo %SCRIPT_DIR%%output_path% Directory created successfully.
)

echo.
exit /b 0

:_deactivate
echo Attempting to deactivate existing (and activated) Virtual Environment
deactivate >nul 2>&1
exit /b 0

:_version_specific
set "flag=%~1"
set "desc=%~2"
set "value=%~3"

call :_activate || exit /b 1

set "package_name="
set /p package_name=<"%SCRIPT_DIR%..\package_name.txt"
if not defined package_name (
    echo ERROR: Could not read package name.
    call :_deactivate
    exit /b 1
)
set "package_path=%SCRIPT_DIR%..\%package_name%"

echo %desc%
if defined value (
    %python_bin% -m incremental.update --path="%package_path%" "%package_name%" %flag% %value%
) else (
    %python_bin% -m incremental.update --path="%package_path%" "%package_name%" %flag%
)
set "rc=%errorlevel%"
call :_deactivate
exit /b %rc%

:cmd_env
set "type=%~1"
if "%type%"=="" set "type=activate"
if /I "%type%"=="a" set "type=activate"
if /I "%type%"=="act" set "type=activate"
if /I "%type%"=="d" set "type=deactivate"
if /I "%type%"=="deact" set "type=deactivate"

if /I "%type%"=="activate" (
    call :_activate
    exit /b %errorlevel%
)
if /I "%type%"=="deactivate" (
    call :_deactivate
    exit /b %errorlevel%
)

echo ERROR: Unknown env type '%type%'
echo Valid types: activate ^| deactivate
exit /b 1

:cmd_install
set "type=%~1"
if "%type%"=="" set "type=all"
if /I "%type%"=="a" set "type=all"
if /I "%type%"=="i" set "type=internal_lib"
if /I "%type%"=="int" set "type=internal_lib"
if /I "%type%"=="lib" set "type=internal_lib"
if /I "%type%"=="it" set "type=internal_tool"
if /I "%type%"=="tool" set "type=internal_tool"
if /I "%type%"=="e" set "type=external"
if /I "%type%"=="ext" set "type=external"
if /I "%type%"=="b" set "type=build"
if /I "%type%"=="c" set "type=cicd"
if /I "%type%"=="ci" set "type=cicd"
if /I "%type%"=="x" set "type=experimental"
if /I "%type%"=="exp" set "type=experimental"

call :_activate || exit /b 1
if /I "%type%"=="all" (
    echo Installing all requirements
    pip install -r "%SCRIPT_DIR%..\requirements.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_lib" (
    echo Installing internal lib requirements
    pip install -r "%SCRIPT_DIR%..\requirements_internal_lib.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_tool" (
    echo Installing internal tool requirements
    pip install -r "%SCRIPT_DIR%..\requirements_internal_tool.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="external" (
    echo Installing external requirements
    pip install -r "%SCRIPT_DIR%..\requirements_external.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="build" (
    echo Installing build requirements
    pip install -r "%SCRIPT_DIR%..\requirements_build.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="cicd" (
    echo Installing CI CD requirements
    pip install -r "%SCRIPT_DIR%..\requirements_cicd.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="experimental" (
    echo Installing experimental requirements
    pip install -r "%SCRIPT_DIR%..\requirements_experimental.txt"
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)

echo ERROR: Unknown install type '%type%'
echo Valid types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental
call :_deactivate
exit /b 1

:cmd_uninstall
set "type=%~1"
if "%type%"=="" set "type=internal_lib"
if /I "%type%"=="a" set "type=all"
if /I "%type%"=="i" set "type=internal_lib"
if /I "%type%"=="int" set "type=internal_lib"
if /I "%type%"=="lib" set "type=internal_lib"
if /I "%type%"=="it" set "type=internal_tool"
if /I "%type%"=="tool" set "type=internal_tool"
if /I "%type%"=="e" set "type=external"
if /I "%type%"=="ext" set "type=external"
if /I "%type%"=="b" set "type=build"
if /I "%type%"=="c" set "type=cicd"
if /I "%type%"=="ci" set "type=cicd"
if /I "%type%"=="x" set "type=experimental"
if /I "%type%"=="exp" set "type=experimental"
if /I "%type%"=="n" set "type=name"
if /I "%type%"=="name" set "type=name"

call :_activate || exit /b 1
if /I "%type%"=="all" (
    echo UnInstalling all requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_lib" (
    echo UnInstalling internal lib requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_internal_lib.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_tool" (
    echo UnInstalling internal tool requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_internal_tool.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="external" (
    echo UnInstalling external requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_external.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="build" (
    echo UnInstalling build requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_build.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="cicd" (
    echo UnInstalling CI CD requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_cicd.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="experimental" (
    echo UnInstalling experimental requirements
    pip uninstall -r "%SCRIPT_DIR%..\requirements_experimental.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="name" (
    echo UnInstalling requirements by name
    pip uninstall -r "%SCRIPT_DIR%..\requirements_name.txt" -y
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)

echo ERROR: Unknown uninstall type '%type%'
echo Valid types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental ^| name
call :_deactivate
exit /b 1

:cmd_upgrade
set "type=%~1"
if "%type%"=="" set "type=internal_lib"
if /I "%type%"=="a" set "type=all"
if /I "%type%"=="i" set "type=internal_lib"
if /I "%type%"=="int" set "type=internal_lib"
if /I "%type%"=="lib" set "type=internal_lib"
if /I "%type%"=="it" set "type=internal_tool"
if /I "%type%"=="tool" set "type=internal_tool"
if /I "%type%"=="e" set "type=external"
if /I "%type%"=="ext" set "type=external"
if /I "%type%"=="b" set "type=build"
if /I "%type%"=="c" set "type=cicd"
if /I "%type%"=="ci" set "type=cicd"
if /I "%type%"=="x" set "type=experimental"
if /I "%type%"=="exp" set "type=experimental"
if /I "%type%"=="p" set "type=pip"

call :_activate || exit /b 1
if /I "%type%"=="all" (
    echo Upgrading all requirements
    %python_bin% -m pip install --upgrade pip
    pip install -r "%SCRIPT_DIR%..\requirements.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_lib" (
    echo Upgrading internal lib requirements
    pip install -r "%SCRIPT_DIR%..\requirements_internal_lib.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="internal_tool" (
    echo Upgrading internal tool requirements
    pip install -r "%SCRIPT_DIR%..\requirements_internal_tool.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="external" (
    echo Upgrading external requirements
    pip install -r "%SCRIPT_DIR%..\requirements_external.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="build" (
    echo Upgrading build requirements
    pip install -r "%SCRIPT_DIR%..\requirements_build.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="cicd" (
    echo Upgrading CI CD requirements
    pip install -r "%SCRIPT_DIR%..\requirements_cicd.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="experimental" (
    echo Upgrading experimental requirements
    pip install -r "%SCRIPT_DIR%..\requirements_experimental.txt" --upgrade
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)
if /I "%type%"=="pip" (
    %python_bin% -m pip install --upgrade pip
    set "rc=%errorlevel%"
    call :_deactivate
    exit /b %rc%
)

echo ERROR: Unknown upgrade type '%type%'
echo Valid types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental ^| pip
call :_deactivate
exit /b 1

:cmd_list
set "type=%~1"
if "%type%"=="" set "type=env"
if /I "%type%"=="e" set "type=env"
if /I "%type%"=="s" set "type=system"
if /I "%type%"=="sys" set "type=system"

call :_load_venv_vars || exit /b 1
if /I "%type%"=="env" (
    call :_activate || exit /b 1
    set "env_name=!vir_env_name!"
) else (
    set "env_name="
    call :_fetch_python_version
)

call :_fetch_os_type
set "export_list_path=%SCRIPT_DIR%%output_path%\requirements_list_%type%_%env_name%_%python_version%_%os_type%.log"
set "export_freeze_path=%SCRIPT_DIR%%output_path%\requirements_freeze_%type%_%env_name%_%python_version%_%os_type%.log"

echo Listing requirements
pip list

echo Listing requirements to !export_list_path!
pip list > "!export_list_path!"

echo Freezing requirements to !export_freeze_path!
pip freeze > "!export_freeze_path!"

if /I "%type%"=="env" call :_deactivate
exit /b %errorlevel%

:cmd_unit_tests
set "type=%~1"
if "%type%"=="" set "type=full"
if /I "%type%"=="f" set "type=full"
if /I "%type%"=="all" set "type=full"
if /I "%type%"=="u" set "type=unit"
if /I "%type%"=="p" set "type=package"
if /I "%type%"=="pkg" set "type=package"

if /I "%type%"=="full" (
    call :_activate || exit /b 1
    set "export_path=%SCRIPT_DIR%%output_path%\run_tests_!vir_env_name!.log"
    echo Export Path: !export_path!
    echo Starting App
    pushd "%SCRIPT_DIR%.."
    %python_bin% -u -m play_helpers.test.test > "!export_path!" 2>&1
    set "rc=%errorlevel%"
    popd
    call :_deactivate
    exit /b %rc%
)

if /I "%type%"=="unit" (
    call :_activate || exit /b 1
    echo Starting App
    pushd "%SCRIPT_DIR%.."
    %python_bin% -m unittest play_helpers/test/test_util.py
    set "rc=%errorlevel%"
    popd
    call :_deactivate
    exit /b %rc%
)

if /I "%type%"=="package" (
    set "ini_file=%SCRIPT_DIR%config_vir_env_default.ini"
    echo Starting the loop...
    for %%E in ("..\venv_39" "..\venv_314") do (
        echo current_env: %%~E
        > "!ini_file!" echo path=%%~E
        call "%~f0" list
        call "%~f0" run-tests full
        echo -----------------
    )
    echo Ending the loop...
    exit /b 0
)

echo ERROR: Unknown run-tests type '%type%'
echo Valid types: full ^| unit ^| package
exit /b 1

:cmd_version
set "type=%~1"
if "%type%"=="" set "type=patch"
set "default_version=1.0.0"

if /I "%type%"=="s" set "type=set"
if /I "%type%"=="c" set "type=create"
if /I "%type%"=="init" set "type=create"
if /I "%type%"=="f" set "type=create"
if /I "%type%"=="first" set "type=create"
if /I "%type%"=="d" set "type=dev"
if /I "%type%"=="p" set "type=patch"
if /I "%type%"=="def" set "type=default"

if /I "%type%"=="set" (
    set "versionValue="
    set /p versionValue=Please Enter Project Version:
    if not defined versionValue (
        echo ERROR: Empty version value.
        exit /b 1
    )
    set "firstChar=!versionValue:~0,1!"
    if not "!firstChar!"=="\"" set "versionValue=\"!versionValue!\""
    call :_version_specific --newversion "Setting Specific Version" "!versionValue!"
    exit /b %errorlevel%
)
if /I "%type%"=="create" (
    call :_version_specific --create "Creating Version File"
    exit /b %errorlevel%
)
if /I "%type%"=="dev" (
    call :_version_specific --dev "Setting Dev Version (Should be used for Internal versions only)"
    exit /b %errorlevel%
)
if /I "%type%"=="patch" (
    call :_version_specific --patch "Setting Patch Version (Should be used for Public versions only)"
    exit /b %errorlevel%
)
if /I "%type%"=="default" (
    call :_version_specific --newversion "Setting Default Version" "%default_version%"
    exit /b %errorlevel%
)

echo ERROR: Unknown version type '%type%'
echo Valid types: set ^| create ^| dev ^| patch ^| default
exit /b 1

:cmd_help
echo =============================================================================
echo manage.bat - Unified management script
echo version: 1.0
echo.
echo Usage:
echo   manage.bat ^<command^> [options]
echo.
echo Commands:
echo   e, env [type]                             Manage virtual environment (default: activate)
echo                                                 types: activate ^| deactivate
echo   i, ins, install [type]                    Install required dependencies (default: all)
echo                                                 types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental
echo   un, rm, uninstall [type]                  Uninstall required dependencies (default: internal_lib)
echo                                                 types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental ^| name
echo   u, up, upgrade [type]                     Upgrade required dependencies (default: internal_lib)
echo                                                 types: all ^| internal_lib ^| internal_tool ^| external ^| build ^| cicd ^| experimental ^| pip
echo   l, ls, list [type]                        List ^& freeze installed dependencies  (default: env)
echo                                                 types: env ^| system
echo   t, test, tests, ut, unit-tests [type]     Run unit tests (default: full)
echo                                                 types: full ^| unit ^| package
echo   v, ver, version [type]                    Manage project version (default: patch)
echo                                                 types: set ^| create ^| dev ^| patch ^| default
echo   h, -h, --help, help                       Show this help message
echo.
echo Aliases:
echo   types: act, deact, all, lib, tool, ext, build, cicd, exp, env, sys, full, unit, pkg
echo =============================================================================
exit /b 0

