@echo off
REM =============================================================================
REM manage.bat — Unified management script for Windows (Bash equivalent: manage.sh)
REM version: 2.0
REM
REM Usage:
REM   manage.bat <command> [type]
REM
REM Commands:
REM   i, install [type]     Install requirements (default: basic)
REM                            types: basic, experimental (exp, e), external (ext), internal_lib (il), internal_tool (it)
REM   u, uninstall [type]   Uninstall requirements (default: experimental)
REM                            types: experimental (exp, e), external (ext), internal_lib (il), internal_tool (it)
REM   up, upgrade [type]    Upgrade requirements (default: internal_lib)
REM                            types: basic, experimental (exp, e), external (ext), internal_lib (il), internal_tool (it), pip
REM   l, list [type]        List & freeze requirements (default: env)
REM                            types: env, system
REM   e, env [type]         Manage virtual environment (default: activate)
REM                            types: activate (a, act), deactivate (d, deact)
REM   ci, cicd [type]       Run CI/CD operations (default: lint_error)
REM                            types: build, lint_error, lint_warning
REM   v, ver, version [type] Manage project version (default: patch)
REM                            types: set, create, dev, patch, default
REM   h, help               Show this help message
REM
REM =============================================================================

set command=%1
set type=%2

REM Expand command aliases
if "%command%"=="i" set command=install
if "%command%"=="u" set command=uninstall
if "%command%"=="up" set command=upgrade
if "%command%"=="l" set command=list
if "%command%"=="e" set command=env
if "%command%"=="ci" set command=cicd
if "%command%"=="v" set command=version
if "%command%"=="ver" set command=version
if "%command%"=="h" set command=help

if "%command%"=="" set command=help

REM Set default types based on command
if "%type%"=="" (
    if "%command%"=="install" set type=basic
    if "%command%"=="uninstall" set type=experimental
    if "%command%"=="upgrade" set type=internal_lib
    if "%command%"=="list" set type=env
    if "%command%"=="env" set type=activate
    if "%command%"=="cicd" set type=lint_error
    if "%command%"=="version" set type=patch
)

REM Expand type aliases
if "%type%"=="a" set type=activate
if "%type%"=="act" set type=activate
if "%type%"=="d" set type=deactivate
if "%type%"=="deact" set type=deactivate
if "%type%"=="b" set type=basic
if "%type%"=="exp" set type=experimental
if "%type%"=="e" set type=experimental
if "%type%"=="ext" set type=external
if "%type%"=="il" set type=internal_lib
if "%type%"=="it" set type=internal_tool

REM Dispatch commands
if "%command%"=="install" (
    goto cmd_install
) else if "%command%"=="uninstall" (
    goto cmd_uninstall
) else if "%command%"=="upgrade" (
    goto cmd_upgrade
) else if "%command%"=="list" (
    goto cmd_list
) else if "%command%"=="env" (
    goto cmd_env
) else if "%command%"=="cicd" (
    goto cmd_cicd
) else if "%command%"=="version" (
    goto cmd_version
) else if "%command%"=="help" (
    call :help
) else (
    echo ERROR: Invalid command '%command%'. Run 'manage.bat help' for usage.
    exit /b 1
)

goto :eof

REM =============================================================================
REM COMMAND HANDLERS
REM =============================================================================

:cmd_install
call :activate
if "%type%"=="basic" (
    set req_file=..\requirements.txt
    set type_desc=basic
    set action=Installing
) else (
    goto install_%type%
)
:install_experimental
set type_desc=Experimental
set req_file=..\requirements_experimental.txt
set action=Installing
goto install_common
:install_external
set type_desc=External
set req_file=..\requirements_external.txt
set action=Installing
goto install_common
:install_internal_lib
set type_desc=Internal lib
set req_file=..\requirements_internal_lib.txt
set action=Installing
goto install_common
:install_internal_tool
set type_desc=Internal tools
set req_file=..\requirements_internal_tool.txt
set action=Installing
goto install_common
:install_common
if not exist "%req_file%" (
    echo ERROR: Requirements file not found: %req_file%
    call :deactivate
    exit /b 1
)
echo %action% %type_desc% requirements
pip install -r %req_file%
if errorlevel 1 (
    echo ERROR: pip install failed with exit code %errorlevel%
    call :deactivate
    exit /b 1
)
call :deactivate
goto :eof

:cmd_uninstall
if "%type%"=="basic" (
    echo ERROR: Uninstall not supported for basic type
    exit /b 1
)
call :activate
goto uninstall_%type%
:uninstall_experimental
set type_desc=Experimental
set req_file=..\requirements_experimental_name.txt
goto uninstall_common
:uninstall_external
set type_desc=External
set req_file=..\requirements_external_name.txt
goto uninstall_common
:uninstall_internal_lib
set type_desc=Internal lib
set req_file=..\requirements_internal_lib_name.txt
goto uninstall_common
:uninstall_internal_tool
set type_desc=Internal tools
set req_file=..\requirements_internal_tool_name.txt
goto uninstall_common
:uninstall_common
if not exist "%req_file%" (
    echo ERROR: Requirements file not found: %req_file%
    call :deactivate
    exit /b 1
)
echo UnInstalling %type_desc% requirements
pip uninstall -r %req_file% -y
if errorlevel 1 (
    echo ERROR: pip uninstall failed with exit code %errorlevel%
    call :deactivate
    exit /b 1
)
call :deactivate
goto :eof

:cmd_upgrade
if "%type%"=="pip" (
    call :activate
    echo Upgrading pip
    python.exe -m pip install --upgrade pip
    if errorlevel 1 (
        echo ERROR: pip upgrade failed with exit code %errorlevel%
        call :deactivate
        exit /b 1
    )
    call :deactivate
    goto :eof
)
call :activate
goto upgrade_%type%
:upgrade_basic
set type_desc=basic
set req_file=..\requirements.txt
goto upgrade_common
:upgrade_experimental
set type_desc=Experimental
set req_file=..\requirements_experimental.txt
goto upgrade_common
:upgrade_external
set type_desc=External
set req_file=..\requirements_external.txt
goto upgrade_common
:upgrade_internal_lib
set type_desc=Internal lib
set req_file=..\requirements_internal_lib.txt
goto upgrade_common
:upgrade_internal_tool
set type_desc=Internal tools
set req_file=..\requirements_internal_tool.txt
goto upgrade_common
:upgrade_common
if not exist "%req_file%" (
    echo ERROR: Requirements file not found: %req_file%
    call :deactivate
    exit /b 1
)
echo Upgrading %type_desc% requirements
pip install -r %req_file% --upgrade
if errorlevel 1 (
    echo ERROR: pip upgrade failed with exit code %errorlevel%
    call :deactivate
    exit /b 1
)
call :deactivate
goto :eof

:cmd_list
call :activate
set output_path=logs
if not exist "%output_path%" (
    mkdir "%output_path%"
    echo %output_path% Directory created.
)

REM Generate timestamp for log files
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    call :deactivate
    exit /b 1
)

if "%type%"=="env" (
    set list_file=%output_path%\requirements_list_env_%mydate%_%mytime%.log
    set freeze_file=%output_path%\requirements_freeze_env_%mydate%_%mytime%.log
) else if "%type%"=="system" (
    set list_file=%output_path%\requirements_list_system_%mydate%_%mytime%.log
    set freeze_file=%output_path%\requirements_freeze_system_%mydate%_%mytime%.log
    call :deactivate
) else (
    echo ERROR: Invalid list type '%type%'. Use 'env' or 'system'.
    call :deactivate
    exit /b 1
)

echo Listing requirements
pip list
echo.
echo Exporting list to %list_file%
pip list > %list_file%
echo.
echo Exporting freeze to %freeze_file%
pip freeze > %freeze_file%

if "%type%"=="env" (
    call :deactivate
)
goto :eof

:cmd_env
if "%type%"=="activate" (
    call :activate
) else if "%type%"=="deactivate" (
    call :deactivate
) else (
    echo ERROR: Invalid env type '%type%'. Use 'activate' or 'deactivate'.
    exit /b 1
)
goto :eof

:cmd_cicd
if "%type%"=="build" (
    call :activate
    set output_path=logs
    if not exist "%output_path%" mkdir "%output_path%"
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set build_log=%output_path%\build_%mydate%_%mytime%.log
    echo Building Project (output: %build_log%)
    cd ..
    python -m build > %build_log% 2>&1
    if errorlevel 1 (
        echo ERROR: Build failed. Check %build_log%
        cd scripts
        call :deactivate
        exit /b 1
    )
    echo Build artifacts:
    dir /b dist\
    cd scripts
    call :deactivate
) else if "%type%"=="lint_error" (
    call :activate
    set output_path=logs
    if not exist "%output_path%" mkdir "%output_path%"
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set lint_log=%output_path%\lint_error_%mydate%_%mytime%.log
    echo Checking lint errors (output: %lint_log%)
    cd ..
    flake8 . --exit-zero --select=E9,F63,F7,F82 > %lint_log% 2>&1
    if errorlevel 1 (
        echo Lint errors found. Check %lint_log%
        cd scripts
        call :deactivate
        exit /b 1
    )
    cd scripts
    call :deactivate
) else if "%type%"=="lint_warning" (
    call :activate
    set output_path=logs
    if not exist "%output_path%" mkdir "%output_path%"
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set lint_log=%output_path%\lint_warning_%mydate%_%mytime%.log
    echo Checking lint warnings (output: %lint_log%)
    cd ..
    flake8 . --exit-zero --max-complexity=10 > %lint_log% 2>&1
    cd scripts
    call :deactivate
) else (
    echo ERROR: Invalid cicd type '%type%'. Use 'build', 'lint_error', or 'lint_warning'.
    exit /b 1
)
goto :eof

:cmd_version
if "%type%"=="set" (
    set /p versionValue=Please Enter Project Version:
    call :activate
    set package_name=
    for /f %%i in (..\package_name.txt) do set package_name=%%i
    set package_path=..\%package_name%
    echo Setting Specific Version: %versionValue%
    python -m incremental.update --path=%package_path% %package_name% --newversion "%versionValue%"
    if errorlevel 1 (
        echo ERROR: Version update failed
        call :deactivate
        exit /b 1
    )
    call :deactivate
) else if "%type%"=="create" (
    call :activate
    set package_name=
    for /f %%i in (..\package_name.txt) do set package_name=%%i
    set package_path=..\%package_name%
    echo Creating Version File
    python -m incremental.update --path=%package_path% %package_name% --create
    if errorlevel 1 (
        echo ERROR: Version file creation failed
        call :deactivate
        exit /b 1
    )
    call :deactivate
) else if "%type%"=="dev" (
    call :activate
    set package_name=
    for /f %%i in (..\package_name.txt) do set package_name=%%i
    set package_path=..\%package_name%
    echo Setting Dev Version
    python -m incremental.update --path=%package_path% %package_name% --dev
    if errorlevel 1 (
        echo ERROR: Dev version update failed
        call :deactivate
        exit /b 1
    )
    call :deactivate
) else if "%type%"=="patch" (
    call :activate
    set package_name=
    for /f %%i in (..\package_name.txt) do set package_name=%%i
    set package_path=..\%package_name%
    echo Setting Patch Version
    python -m incremental.update --path=%package_path% %package_name% --patch
    if errorlevel 1 (
        echo ERROR: Patch version update failed
        call :deactivate
        exit /b 1
    )
    call :deactivate
) else if "%type%"=="default" (
    call :activate
    set package_name=
    for /f %%i in (..\package_name.txt) do set package_name=%%i
    set package_path=..\%package_name%
    echo Setting Default Version
    python -m incremental.update --path=%package_path% %package_name% --newversion "1.0.0"
    if errorlevel 1 (
        echo ERROR: Default version update failed
        call :deactivate
        exit /b 1
    )
    call :deactivate
) else (
    echo ERROR: Invalid version type '%type%'. Use 'set', 'create', 'dev', 'patch', or 'default'.
    exit /b 1
)
goto :eof

REM =============================================================================
REM HELPER SUBROUTINES
REM =============================================================================

:activate
echo Attempting to activate existing Virtual Environment
set output_path=logs
SET /P vir_env_path=<config_vir_env.ini
for %%A in ("%vir_env_path%") do set "vir_env=%%~nxA"
call %vir_env_path%\Scripts\activate
echo.
echo Python Version
python --version
echo.
echo Python Location
where python
if not exist "%output_path%" (
    mkdir "%output_path%"
    echo %output_path% Directory created successfully.
)
echo.
goto :eof

:deactivate
echo Attempting to deactivate existing Virtual Environment
SET /P VIR_ENV_PATH=<config_vir_env.ini
call %VIR_ENV_PATH%\Scripts\deactivate
echo.
echo Python Version
python --version
echo.
echo Python Location
where python
goto :eof

:help
echo Usage: manage.bat [command] [type]  (command defaults to help)
echo.
echo Commands:
echo   env (e) [type]          Manage virtual environment. Default: activate
echo                             Types: activate (a, act), deactivate (d, deact)
echo   install (i) [type]      Install requirements. Default: basic
echo                             Types: basic (b), experimental (exp, e), external (ext), internal_lib (il), internal_tool (it)
echo   uninstall (u) [type]    Uninstall requirements. Default: experimental
echo                             Types: experimental (exp, e), external (ext), internal_lib (il), internal_tool (it)
echo   list (l) [type]         List and freeze requirements. Default: env
echo                             Types: env, system
echo   upgrade (up) [type]     Upgrade requirements. Default: internal_lib
echo                             Types: basic (b), experimental (exp, e), external (ext), internal_lib (il), internal_tool (it), pip (p)
echo   cicd (ci) [type]        Run CI/CD operations. Default: lint_error
echo                             Types: build, lint_error, lint_warning
echo   version (v, ver) [type] Manage project version. Default: patch
echo                             Types: set, create, dev, patch, default
echo   help (h)                Show this help message
echo.
echo Examples:
echo   manage.bat              (shows this help)
echo   manage.bat e a          (activate virtual environment)
echo   manage.bat i            (install basic)
echo   manage.bat i e          (install experimental)
echo   manage.bat u ext        (uninstall external)
echo   manage.bat l env        (list env requirements)
echo   manage.bat up           (upgrade internal_lib)
echo   manage.bat ci build     (build project)
echo   manage.bat v patch      (set patch version)
echo.
echo NOTE: On Unix/macOS/Linux, use manage.sh for equivalent functionality.
goto :eof
