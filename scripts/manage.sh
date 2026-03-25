#!/bin/bash
# =============================================================================
# manage.sh — Unified management script for Unix/Linux/macOS (Batch equivalent: manage.bat on Windows)
# version: 1.4
#
# Usage:
#   ./manage.sh <command> [type]
#
# Commands:
#   env [type]           Manage virtual environment (default: activate)
#                            types: activate | deactivate
#   install [type]       Install requirements (default: basic)
#                            types: basic | internal_lib | internal_tool | external | build | cicd | experimental | tests | all
#   uninstall [type]     Uninstall requirements (default: internal_lib)
#                            types: basic | internal_lib | internal_tool | external | build | cicd | experimental | tests | all | name
#   list [type]          List & freeze installed requirements (default: env)
#                            types: env | system
#   upgrade [type]       Upgrade requirements (default: internal_lib)
#                            types: basic | internal_lib | internal_tool | external | build | cicd | experimental | tests | all | pip
#   cicd [type]          Run CI/CD operations (default: build)
#                          types: build | lint_error | lint_warning
#   unit-tests [type]    Run unit tests (default: full)
#                             types: full | unit | package
#   version [type]       Manage project version (default: patch)
#                             types: set | create | dev | patch | default
#   help                 Show this help message
#
#
# Commands Aliases:
#   env           e | en
#   install       i | ins          
#   uninstall     un | rm          
#   upgrade       u | up           
#   list          l | ls           
#   show          s | sh           
#   cicd          ci | cd          
#   unit-tests    t | test | tests | ut
#   version       v | ver          
#   help          h | -h | --help    
#
#
# type Aliases:
#  For env
#   activate         a | act
#   deactivate       d | deact
#  Universal for install/uninstall/upgrade
#   basic            b | ba | basic  
#   internal_lib     i | int | lib   
#   internal_tool    it | tool     
#   external         e | ext       
#   build            bu | build    
#   cicd             c | ci        
#   experimental     x | exp       
#   tests            t | tests     
#   all              a | all       
#  For uninstall
#   name             n | name
#  For upgrade
#   pip              p | pip 
#  For list
#   env              e
#   system           s | sys
#  For cicd
#   build            b | bu 
#   lint_error       e | er | err | error | li_er
#   lint_warning     w | wa | warn | li_wa
#  For unit_tests
#   full             f | all
#   unit             u
#   package          p | pkg
#  For version
#   set              s
#   create           c | init | f | first
#   dev              d
#   patch            p
#   default          def
#
#
# NOTE: On Windows, use manage.bat for equivalent functionality.
#
# =============================================================================

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
LOGS_DIR="${SCRIPT_DIR}/logs"

_lc() {
    # macOS default bash (3.x) does not support ${var,,}
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

_load_venv_vars() {
    # Read the first line of the config file into a variable
    vir_env_path=$(head -n 1 "${SCRIPT_DIR}/config_vir_env.ini")
    # Extract the base directory name
    vir_env_name=$(basename "$vir_env_path")

    # Debugging
    # echo "Virtual Environment Path: $vir_env_path"
    # echo "Virtual Environment Name: $vir_env_name"
}

_fetch_python_version() {
    python_bin="$(command -v python3 || command -v python)"
    python_version="$("$python_bin" -c 'import sys; print(sys.version.split()[0])')"
}

_fetch_os_type() {
    local uname_out
    uname_out="$(uname -s 2>/dev/null || echo unknown)"
    os_type="unknown"

    case "$uname_out" in
      Darwin)
        os_type="macos"
        ;;
      Linux)
        if grep -qiE "(microsoft|wsl)" /proc/version 2>/dev/null; then
          os_type="wsl"
        else
          os_type="linux"
        fi
        ;;
      CYGWIN*|MINGW*|MSYS*)
        os_type="windows"
        ;;
      *)
        os_type="unknown"
        ;;
    esac
}

_activate() {
    echo "Attempting to activate existing Virtual Environment"
    _load_venv_vars

    source "$vir_env_path/bin/activate"
    _fetch_python_version

    echo ""
    echo "Python Version"
    "$python_bin" --version

    echo ""
    echo "Python Location"
    which "$python_bin"

    if [ ! -d "${LOGS_DIR}" ]; then
        mkdir -p "${LOGS_DIR}"
        echo "${LOGS_DIR} Directory created successfully."
    fi

    echo ""
}

_deactivate() {
    echo "Attempting to deactivate existing (and activated) Virtual Environment"
    deactivate
}

_version_specific() {
    # $1 = flag (--dev | --patch | --newversion | --create)
    # $2 = description message
    # $3 = version value (optional, used with --newversion)

    _activate

    local flag="$1"
    local desc="$2"
    local value="$3"
    local package_name

    package_name=$(cat "${ROOT_DIR}/package_name.txt")
    local package_path="${ROOT_DIR}/${package_name}"
    
    # Sample: python -m incremental.update --path=../play_helpers play_helpers --dev
    # Sample: python -m incremental.update --path=../play_helpers play_helpers --patch
    # REM Sample: python -m incremental.update --path=.\..\play_helpers play_helpers --dev
    # REM Sample: python -m incremental.update --path=.\..\play_helpers play_helpers --patch

    local cmd_data=""$python_bin" -m incremental.update --path=$package_path $package_name $flag $value"

    # Debugging
#    echo flag: "$flag"
#    echo desc: "$desc"
#    echo value: "$value"
#    echo package_name: "$package_name"
#    echo package_path: "$package_path"
#    echo cmd_data: "$cmd_data"

    echo "$desc"
    # $cmd_data "$1""$3"
    $cmd_data
    _deactivate
}

_normalize_type() {
    # Normalize type aliases to standard names and validate
    local type="${1:-basic}"
    local cmd="${2:-install}"    
    type="$(_lc "$type")"

    case "$type" in
        # Universal aliases
        b|ba|basic) type="basic" ;;	
        i|int|lib) type="internal_lib" ;;
        it|tool) type="internal_tool" ;;
        e|ext) type="external" ;;
        bu|build) type="build" ;;
        c|ci) type="cicd" ;;
        x|exp) type="experimental" ;;
        t|tests) type="tests" ;;
        a|all) type="all" ;;
        # For uninstall
        n|name) type="name" ;;
        # For upgrade
        p|pip) type="pip" ;;
    esac

    # Validate against supported types for command
    case "$cmd" in
        install)
            [[ "$type" =~ ^(basic|internal_lib|internal_tool|external|build|cicd|experimental|tests|all)$ ]] || { echo "ERROR: Unknown install type '$type'"; return 1; } ;;
        uninstall)
            [[ "$type" =~ ^(basic|internal_lib|internal_tool|external|build|cicd|experimental|tests|all|name)$ ]] || { echo "ERROR: Unknown uninstall type '$type'"; return 1; } ;;
        upgrade)
            [[ "$type" =~ ^(basic|internal_lib|internal_tool|external|build|cicd|experimental|tests|all|pip)$ ]] || { echo "ERROR: Unknown upgrade type '$type'"; return 1; } ;;
    esac
    
    # TODO
    # Need to know the list on known types
    echo "$type"
}

_pip_action() {
    # Generic pip action (install/uninstall/upgrade)

    local action="$1"
    local type="$2"
    local flags="$3"

    local req_file=""
    local desc=""

    # Map type to file and description
    case "$type" in
        basic)           req_file="${ROOT_DIR}/requirements.txt"; desc="all" ;;
        internal_lib)    req_file="${ROOT_DIR}/requirements_internal_lib.txt"; desc="internal lib" ;;
        internal_tool)   req_file="${ROOT_DIR}/requirements_internal_tool.txt"; desc="internal tools" ;;
        external)        req_file="${ROOT_DIR}/requirements_external.txt"; desc="external" ;;
        build)           req_file="${ROOT_DIR}/requirements_build.txt"; desc="build" ;;
        cicd)            req_file="${ROOT_DIR}/requirements_cicd.txt"; desc="CI/CD" ;;
        experimental)    req_file="${ROOT_DIR}/requirements_experimental.txt"; desc="experimental" ;;
        tests)           req_file="${ROOT_DIR}/requirements_tests.txt"; desc="tests" ;;
        name)            req_file="${ROOT_DIR}/requirements_name.txt"; desc="by name" ;;
        pip)             # Special case for pip upgrade
            echo "Upgrading pip"
            "$python_bin" -m pip install --upgrade pip
            return $?
            ;;
        *)
    #    all)             # Special case where basic + couple of more commands are needed
    # TODO:
            echo "ERROR: Unsupported type '$type'"
            return 1
            ;;
    esac

    # Check file exists
    if [ ! -f "$req_file" ]; then
        echo "ERROR: Requirements file not found: $req_file"
        return 1
    fi

    # Determine action text and pip command
    local action_text=""
    local pip_cmd=""
    case "$action" in
        install)
            action_text="Installing"
            pip_cmd="install"
            ;;
        uninstall)
            action_text="UnInstalling"
            pip_cmd="uninstall"
            flags="${flags:--y}"  # Default -y for uninstall
            ;;
        upgrade)
            action_text="Upgrading"
            pip_cmd="install"
            flags="${flags:---upgrade}"  # Default --upgrade for upgrade
            ;;
    esac

    echo "$action_text $desc requirements"
    pip $pip_cmd -r "$req_file" $flags
}

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

cmd_env() {
    local type="${1:-activate}"
    type="$(_lc "$type")"

    case "$type" in
        a|act) type="activate" ;;
        d|deact) type="deactivate" ;;
    esac

    case "$type" in
        activate)   _activate ;;
        deactivate) _deactivate ;;
        *)
            echo "ERROR: Unknown env type '$type'"
            echo "Valid types: activate (a, act) | deactivate (d, deact)"
            return 1
            ;;
    esac
}

cmd_install() {
    local type="${1:-basic}"
    type="$(_normalize_type "$type" "install")" || return 1

    _activate
    _pip_action "install" "$type" "" || { _deactivate; return 1; }
    _deactivate
}

cmd_uninstall() {
    local type="${1:-internal_lib}"
    type="$(_normalize_type "$type" "uninstall")" || return 1

    _activate
    _pip_action "uninstall" "$type" "-y" || { _deactivate; return 1; }
    _deactivate
}

cmd_upgrade() {
    local type="${1:-internal_lib}"
    type="$(_normalize_type "$type" "upgrade")" || return 1

    _activate
    _pip_action "upgrade" "$type" "--upgrade" || { _deactivate; return 1; }
    _deactivate
}

cmd_list() {
    local type="${1:-env}"
    type="$(_lc "$type")"    

    case "$type" in
        e) type="env" ;;
        s|sys) type="system" ;;
    esac

    _load_venv_vars

    if [[ "$type" == "env" ]]; then
        _activate
        local env_name=${vir_env_name}
    else
        local env_name=""
        _fetch_python_version
    fi

    _fetch_os_type

    local export_list_path="${LOGS_DIR}/requirements_list_${type}_${env_name}_${python_version}_${os_type}.log"
    local export_freeze_path="${LOGS_DIR}/requirements_freeze_${type}_${env_name}_${python_version}_${os_type}.log"

    echo "Listing requirements"
    pip list

    echo "Listing requirements to $export_list_path"
    pip list > "$export_list_path"

    echo "Freezing requirements to $export_freeze_path"
    pip freeze > "$export_freeze_path"


    if [[ "$type" == "env" ]]; then
        _deactivate
    fi
}

cmd_show() {
    _activate
    _deactivate
}

cmd_cicd() {
    local type="${1:-build}"
    type="$(_lc "$type")"        

    shift || true

    case "$type" in
        b|bu) type="build" ;;
        e|er|err|error|li_er) type="lint_error" ;;
        w|wa|warn|li_wa) type="lint_warning" ;;
    esac

    _activate
    _fetch_python_version
    _fetch_os_type

    case "$type" in
        build)
            local export_build_path="${LOGS_DIR}/build_${python_version}_${os_type}.log"
            echo "Exporting Build Logs to $export_build_path"
            echo "Building Project"
            cd "${ROOT_DIR}"
            "$python_bin" -m build 2>&1 | tee "$export_build_path"
            echo "Build artifacts:"
            ls -la dist/
            ;;
        lint_error)
            local export_lint_error_path="${LOGS_DIR}/${type}_${python_version}_${os_type}.log"
            echo "Exporting Lint Errors to $export_lint_error_path"
            echo "Error Count is: "
            # Check for Python syntax errors or undefined names
            flake8 "${ROOT_DIR}" --exit-zero --select=E9,F63,F7,F82 | tee "${export_lint_error_path}"
            ;;
        lint_warning)
            local export_lint_warn_path="${LOGS_DIR}/${type}_${python_version}_${os_type}.log"
            echo "Exporting Lint Warnings to $export_lint_warn_path"
            echo "Warning Count is: "
            # Check for other types of warnings.
            flake8 "${ROOT_DIR}" --exit-zero --max-complexity=10 | tee "${export_lint_warn_path}"
            ;;
        *)
            echo "ERROR: Unknown lint type '$type'"
            echo "Valid types: build | lint_error | lint_warning"
            exit 1
            ;;
    esac
    _deactivate
}

cmd_unit_tests() {
    local type="${1:-full}"
    type="$(_lc "$type")"    
        
    shift || true

    case "$type" in
        f|all) type="full" ;;
        u) type="unit" ;;
        p|pkg) type="package" ;;
    esac

    case "$type" in
        full)
            _activate
            local export_path="${LOGS_DIR}/run_tests_${vir_env_name}.log"
            echo "Export Path: $export_path"
            echo "Starting App"
            cd "${SCRIPT_DIR}/.."
            "$python_bin" -u -m play_helpers.test.test > "$export_path" 2>&1
            cd "${SCRIPT_DIR}"
            _deactivate
            ;;
        unit)
            _activate
            echo "Starting App"
            cd "${SCRIPT_DIR}/.."
            # "$python_bin" -m unittest discover -s play_helpers/test
            "$python_bin" -m unittest play_helpers/test/test_util.py
            cd "${SCRIPT_DIR}"
            _deactivate
            ;;
        package)
            local env_list=("../venv_39" "../venv_314")
            local ini_file="${SCRIPT_DIR}/config_vir_env_default.ini"
            echo "Starting the loop..."
            for current_env in "${env_list[@]}"; do
                echo "current_env: $current_env"
                echo "path=$current_env" > "$ini_file"
                bash "${SCRIPT_DIR}/manage.sh" list
                bash "${SCRIPT_DIR}/manage.sh" run-tests full
                echo "-----------------"
            done
            echo "Ending the loop..."
            ;;
        *)
            echo "ERROR: Unknown run-tests type '$type'"
            echo "Valid types: full | unit | package"
            exit 1
            ;;
    esac
}

cmd_version() {
    local type="${1:-patch}"
    type="$(_lc "$type")"        
    shift || true

    local default_version="1.0.0"

    case "$type" in
        s) type="set" ;;
        c|init|f|first) type="create" ;;
        d) type="dev" ;;
        p) type="patch" ;;
        def) type="default" ;;
    esac

    case "$type" in
        set)
            read -p "Please Enter Project Version: " versionValue

            # Add quotes if not present
            # TODO: Quotes are really needed ?
            if [[ "$versionValue" != \"*\" ]]; then
                versionValue="\"$versionValue\""
            fi
            _version_specific --newversion "Setting Specific Version" "$versionValue"
            ;;
        create)
            # if the file was present previously and got deleted now, it will be recreated with same version as before
            # TODO: Need to see the use case when file was not present before, if default version is not set, explicit default version may need to set
            _version_specific --create "Creating Version File"
 #           _version_specific --newversion "Setting Default Version" "$default_version"
            ;;
        dev)
            _version_specific --dev "Setting Dev Version (Should be used for Internal versions only)"
            ;;
        patch)
            _version_specific --patch "Setting Patch Version (Should be used for Public versions only)"
            ;;
        default)
            _version_specific --newversion "Setting Default Version" "$default_version"
            ;;
        *)
            echo "ERROR: Unknown version type '$type'"
            echo "Valid types: set | create | dev | patch | default"
            exit 1
            ;;
    esac
}

cmd_help() {
    tail -n +2 "$0" | while IFS= read -r line; do
        [[ "$line" == \#* ]] || break
        stripped="${line#\#}"
        stripped="${stripped# }"
        printf '%s\n' "$stripped"
    done
    echo ""
    echo "NOTE: On Windows, use manage.bat for equivalent functionality."
}

# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

COMMAND="${1:-help}"
shift || true

case "$(_lc "$COMMAND")" in
    e|en) COMMAND="env" ;;
    i|ins) COMMAND="install" ;;
    un|rm) COMMAND="uninstall" ;;
    u|up) COMMAND="upgrade" ;;
    l|ls) COMMAND="list" ;;
    s|sh) COMMAND="show" ;;
    ci|cd) COMMAND="cicd" ;;
    t|test|tests|ut) COMMAND="unit-tests" ;;
    v|ver) COMMAND="version" ;;
    h|-h|--help) COMMAND="help" ;;
esac

case "$COMMAND" in
    env)            cmd_env "$@" ;;
    install)        cmd_install "$@" ;;
    uninstall)      cmd_uninstall "$@" ;;
    upgrade)        cmd_upgrade "$@" ;;
    list)           cmd_list "$@" ;;
    show)           cmd_show "$@" ;;
    cicd)           cmd_cicd "$@" ;;
# TODO: This needs to be fixed
#    unit-tests)     cmd_unit_tests "$@" ;;
    version)        cmd_version "$@" ;;
    help)           cmd_help ;;
    *)
        echo "ERROR: Unknown command '$COMMAND'"
        echo "Run './manage.sh help' for usage."
        exit 1
        ;;
esac