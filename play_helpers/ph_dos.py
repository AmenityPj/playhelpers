from play_helpers.ph_util import PhUtil

SEPERATOR = """echo.
echo.
echo.
echo.
echo "XXX"
"""


class PhDos:
    BATCH_RUN_TC = 'run_tc.bat'

    @classmethod
    def delete_file(cls, target_file_path, conditional=True):
        del_cmd = f'DEL /F /S /Q /A "{target_file_path}"'
        return f'if exist "{target_file_path}" {del_cmd}' if conditional else del_cmd

    @classmethod
    def delete_empty_dirs_in_current_folder(cls):
        return 'for /f "delims=" %%d in (\'dir /s /b /ad ^| sort /r\') do rd "%%d"'

    @classmethod
    def create_zip_file(cls, target_zip, source_files):
        return f'7z a -t7z -sdel "{target_zip}" "{source_files}"'

    @classmethod
    def switch_to_current_folder(cls):
        return 'pushd %~dp0'

    @classmethod
    def create_directory(cls, dir_path=None, file_path=None, conditional=True):
        if PhUtil.is_empty(dir_path) and PhUtil.is_not_empty(file_path):
            dir_path = PhUtil.get_file_name_and_extn(file_path=file_path, only_path=True)
        mk_cmd = f'MD "{dir_path}"'
        return f'if not exist "{dir_path}" {mk_cmd}' if conditional else mk_cmd

    @classmethod
    def change_directory_parent(cls):
        return 'cd ..'

    @classmethod
    def change_directory(cls, target_dir_path):
        return f'cd "{target_dir_path}"'

    @classmethod
    def echo_on(cls):
        return '@echo on'

    @classmethod
    def echo_off(cls):
        return '@echo off'

    @classmethod
    def echo(cls, msg, wrap_up=False):
        res = f'echo {msg}'
        if not wrap_up:
            return res
        return [
            cls.echo_off(),
            res,
            cls.echo_on()
        ]

    @classmethod
    def time_stamp(cls):
        return 'echo Time Stamp is: %DATE% %TIME%'

    @classmethod
    def windows_version(cls):
        return 'ver'

    @classmethod
    def user_name(cls):
        return 'echo %USERNAME%'

    @classmethod
    def common_info(cls):
        return [
            cls.echo_off(),
            cls.time_stamp(),
            cls.user_name(),
            'echo %USERDOMAIN%',
            cls.windows_version(),
            cls.echo_on(),
        ]

    @classmethod
    def get_seperator(cls, heading=None):
        heading = PhUtil.set_if_empty(heading, '---------------')
        return SEPERATOR.replace('XXX', heading)

    @classmethod
    def comment_line(cls, line=None):
        return f'REM {line}'

    @classmethod
    def call_script_for_env_handling(cls, activate_venv=True):
        batch_name = 'activate_vir_env.bat' if activate_venv else 'deactivate_vir_env.bat'
        return [
            'cd scripts',
            f'call {batch_name}',
            'cd ..',
        ]

    @classmethod
    def run_python(cls, module_name):
        return f'python -m {module_name}'

    @classmethod
    def redirect_output(cls, file_path):
        return f'> {file_path}'
