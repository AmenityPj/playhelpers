@echo off

set command=%1
set type=%2

REM Expand command aliases
if "%command%"=="i" set command=install
if "%command%"=="u" set command=uninstall
if "%command%"=="e" set command=env
if "%command%"=="h" set command=help

if "%command%"=="" set command=help

if "%type%"=="" (
    if "%command%"=="install" set type=basic
    if "%command%"=="uninstall" set type=experimental
    if "%command%"=="env" set type=activate
)

REM Expand aliases
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

if "%command%"=="install" or "%command%"=="uninstall" (
    call :activate
    if "%type%"=="basic" (
        if "%command%"=="uninstall" (
            echo Uninstall not supported for basic type
            goto :eof
        )
        set req_file=..\requirements.txt
        set type_desc=basic
        set action=Installing
        set pip_cmd=install
        set flags=
        goto common
    ) else (
        goto %type%
    )
    :experimental
    set type_desc=Experimental
    goto set_req
    :external
    set type_desc=External
    goto set_req
    :internal_lib
    set type_desc=Internal lib
    goto set_req
    :internal_tool
    set type_desc=Internal tools
    goto set_req
    :set_req
    if "%command%"=="install" (
        set req_file=..\requirements_%type%.txt
    ) else (
        set req_file=..\requirements_%type%_name.txt
    )
    goto common
    :common
    if "%command%"=="install" (
        set action=Installing
        set pip_cmd=install
        set flags=
    ) else (
        set action=UnInstalling
        set pip_cmd=uninstall
        set flags=-y
    )
    echo %action% %type_desc% requirements
    pip %pip_cmd% -r %req_file% %flags%
    call :deactivate
) else if "%command%"=="env" (
    if "%type%"=="activate" (
        call :activate
    ) else if "%type%"=="deactivate" (
        call :deactivate
    ) else (
        echo Invalid env command, use activate or deactivate as type
        goto :eof
    )
) else if "%command%"=="help" (
    call :help
) else (
    echo Invalid command. Use install, uninstall, env, or help
    goto :eof
)

goto :eof

:activate
echo Attempting to activate existing Virtual Environment
SET output_path=logs
SET /P vir_env_path=<config_vir_env.ini
for %%A in ("%vir_env_path%") do set "vir_env=%%~nxA"
call %vir_env_path%\Scripts\activate
echo .
echo Python Version
python --version
echo .
echo Python Location
which python
IF NOT EXIST "%output_path%" (
    MD "%output_path%"
    echo "%output_path%" Directory created successfully.
)
echo .
goto :eof

:deactivate
echo Attempting to deactivate existing (and activated) Virtual Environment
SET /P VIR_ENV_PATH=<config_vir_env.ini
call %VIR_ENV_PATH%\Scripts\deactivate
echo .
echo Python Version
python --version
echo .
echo Python Location
which python
goto :eof

:help
echo Usage: manage.bat [command] [type]  (command defaults to help)
echo.
echo Commands:
echo   install (i) [type]    Install requirements. Type optional, defaults to basic. Can be: basic (b), experimental (exp, e), external (ext), internal_lib (il), internal_tool (it).
echo   uninstall (u) [type]  Uninstall requirements. Type optional, defaults to experimental. Can be: experimental (exp, e), external (ext), internal_lib (il), internal_tool (it).
echo   env (e) [type]        Manage virtual environment. Type optional, defaults to activate. Can be: activate (a, act) or deactivate (d, deact).
echo   help (h)              Show this help message.
echo.
echo Examples:
echo   manage.bat        (shows this help)
echo   manage.bat i       (install basic)
echo   manage.bat i e     (install experimental)
echo   manage.bat u       (uninstall experimental)
echo   manage.bat e a     (activate env)
goto :eof
