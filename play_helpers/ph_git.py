import os
from pathlib import Path

from play_helpers.ph_defaults import PhDefaults
from play_helpers.ph_process import PhProcess


class PhGit:
    """
    Alternatives: https://pypi.org/project/python-git-info/
    """
    KEY_GIT_SUMMARY = 'git_summary'
    KEY_GIT_DESCRIBE_ALWAYS = 'git_describe_always'
    KEY_GIT_LOCAL_FILE_HEAD = 'git_local_file_head'

    _CWD_ABS = os.path.dirname(os.path.abspath(__file__))
    _CWD_PATH_LIB = Path(__file__).resolve().parent

    _cwd_default = _CWD_PATH_LIB
    _char_encoding_default = PhDefaults.CHAR_ENCODING
    _char_encoding_errors_default = PhDefaults.CHAR_ENCODING_ERRORS

    git_cmds_pool = {
        'git_rev_parse_hash': ['git', 'rev-parse', 'HEAD'],
        'git_rev_parse_short_hash': ['git', 'rev-parse', '--short', 'HEAD'],
        'git_rev_parse_branch': ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],

        'git_describe': ['git', 'describe'],
        KEY_GIT_DESCRIBE_ALWAYS: ['git', 'describe', '--always'],

        KEY_GIT_SUMMARY: ['git', 'log', '-n', '1', '--pretty=format:%h; %d; %ci; %cn <%ce>; %s'],
        'git_log_commit_hash': ['git', 'log', '-n', '1', '--pretty=format:%H'],
        'git_log_commit_short_hash': ['git', 'log', '-n', '1', '--pretty=format:%h'],
        'git_log_tree_hash': ['git', 'log', '-n', '1', '--pretty=format:%T'],
        'git_log_tree_short_hash': ['git', 'log', '-n', '1', '--pretty=format:%t'],
        'git_log_parent_hash': ['git', 'log', '-n', '1', '--pretty=format:%P'],
        'git_log_parent_short_hash': ['git', 'log', '-n', '1', '--pretty=format:%p'],
        'git_log_head': ['git', 'log', '-n', '1', '--pretty=format:%d'],
        'git_log_time': ['git', 'log', '-n', '1', '--pretty=format:%ci'],
        'git_log_commiter_name': ['git', 'log', '-n', '1', '--pretty=format:%cn'],
        'git_log_commiter_email': ['git', 'log', '-n', '1', '--pretty=format:%ce'],
        'git_log_message': ['git', 'log', '-n', '1', '--pretty=format:%s'],

        'git_symbolic-ref_head': ['git', 'symbolic-ref', 'HEAD'],
        KEY_GIT_LOCAL_FILE_HEAD: ['cat', os.sep.join([os.pardir, '.git', 'HEAD'])],
    }

    @classmethod
    def get_git_summary(cls):
        return cls.get_git_info_detailed(key=cls.KEY_GIT_SUMMARY, with_path_always=True)

    @classmethod
    def get_git_info_detailed(cls, key=None, cwd=None, encoding=None, encoding_errors=None, with_path_always=False):
        if with_path_always and cwd is None:
            cwd = cls._cwd_default
        if encoding is None:
            encoding = cls._char_encoding_default
        if encoding_errors is None:
            encoding_errors = cls._char_encoding_errors_default
        if key:
            return cls.execute_command_in_shell(cmd=cls.git_cmds_pool.get(key), cwd=cwd, encoding=encoding,
                                                encoding_errors=encoding_errors)
        output = {}
        for key in cls.git_cmds_pool:
            output[key] = cls.execute_command_in_shell(cmd=cls.git_cmds_pool.get(key), cwd=cwd, encoding=encoding,
                                                       encoding_errors=encoding_errors)
        # Additional data
        # TODO: To be removed post analysis
        output[cls.KEY_GIT_DESCRIBE_ALWAYS + '_path'] = cls.get_git_info_detailed(key=cls.KEY_GIT_DESCRIBE_ALWAYS,
                                                                                  cwd=cls._CWD_ABS)
        output[cls.KEY_GIT_DESCRIBE_ALWAYS + '_pathlib'] = cls.get_git_info_detailed(
            key=cls.KEY_GIT_DESCRIBE_ALWAYS, cwd=cls._CWD_PATH_LIB)
        output[cls.KEY_GIT_LOCAL_FILE_HEAD + '_path'] = cls.get_git_info_detailed(key=cls.KEY_GIT_LOCAL_FILE_HEAD,
                                                                                  cwd=cls._CWD_ABS)
        output[cls.KEY_GIT_LOCAL_FILE_HEAD + '_pathlib'] = cls.get_git_info_detailed(
            key=cls.KEY_GIT_LOCAL_FILE_HEAD, cwd=cls._CWD_PATH_LIB)

        return output

    @classmethod
    def execute_command_in_shell(cls, cmd, cwd=None, encoding=PhDefaults.CHAR_ENCODING,
                                 encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS):
        try:
            return PhProcess.execute_command_in_shell(cmd=cmd, cwd=cwd, encoding=encoding,
                                                      encoding_errors=encoding_errors)
        except Exception as e:
            # print(f"Error executing command: {e}")
            # TODO: Future handling; Additional data for '_path & _pathlib can be removed
            # if cwd is None:
            #     return cls._check_output(cmd=cmd, cwd=cls._cwd_default,decode_mode=decode_mode)
            return None
