from play_helpers.ph_modules import PhApps
from play_helpers.ph_util import PhUtil


class PhMisc:
    DEFAULT_INCLUDE_ALL_FILES = [
        '*.*',
    ]

    DEFAULT_INCLUDE_PYTHON = [
        '*.py',
    ]
    DEFAULT_INCLUDE_ALL_FOLDERS = [
    ]

    DEFAULT_EXCLUDE_FOLDERS = [
        'data',
        'log*',
        'venv*',
        '.venv*',
        'build*',
        '.idea',
        '.git',
        '.vscode',
        '.eggs',
        '*.egginfo',
        '__pycache__',
        '.eggs',
        'bin',
        'classes',
        'javadoc',
    ]

    DEFAULT_EXCLUDE_FILES = [
        '*.log*',
        '*.gitignore',
        # Archive
        '*.7z',
        '*.rar',
        '*.zip',
        '*.tar',
        '*.gz',
        # Binary
        '*.class',
        '*.pyc',
        '*.obj',
        '*.jar',
        # Binary Windows
        '*.lnk',
        '*.dll',
        '*.exe',
        '*.bin',
        # Binary Unix
        '*.rpm',
        # Docs
        '*.doc',
        '*.docx',
        '*.pdf',
        '*.vsd',
        # Other Programming Language
        '*.html',
        '*.js',
        '*.ini',
        # Misc
        '*.asc',
        '*.bson',
        '*.idx',
        '*.ttf',
    ]

    @classmethod
    def generate_filters(cls, tool_name,
                         include_files=DEFAULT_INCLUDE_ALL_FILES,
                         include_folders=DEFAULT_INCLUDE_ALL_FOLDERS,
                         exclude_files=DEFAULT_EXCLUDE_FILES,
                         exclude_folders=DEFAULT_EXCLUDE_FOLDERS,
                         ):
        """

        :param tool_name:
        :param include_folders:
        :param include_files:
        :param exclude_folders:
        :param exclude_files:
        :return:
        """

        def _decorate_data(data_list, pre, post):
            """

            :param data_list:
            :param pre:
            :param post:
            :return:
            """
            return [(pre + x + post) for x in data_list]

        allowed_tools = [
            PhApps.NOTEPAD_PLUS_PLUS,
            PhApps.BEYOND_COMPARE,
        ]
        tool_name = PhUtil.set_if_unknown(current_value=tool_name, known_values=allowed_tools)
        files_in = []
        folders_in = []
        files_ex = []
        folders_ex = []
        if tool_name == PhApps.NOTEPAD_PLUS_PLUS:
            """
            Exclude Folder:  !+\folder_name
            Exclude File  :  !file_extension  
            """
            sep = ' '
            if exclude_folders:
                decorator_pre = '!+\\'
                decorator_post = ''
                folders_ex = _decorate_data(PhMisc.DEFAULT_EXCLUDE_FOLDERS, decorator_pre, decorator_post)
            if exclude_files:
                decorator_pre = '!'
                decorator_post = ''
                files_ex = _decorate_data(PhMisc.DEFAULT_EXCLUDE_FILES, decorator_pre, decorator_post)
        if tool_name == PhApps.BEYOND_COMPARE:
            """
            Exclude Folder:  '-folder_name\;'
            Exclude File  :  '!file_extension'
            """
            sep = ';'
            if exclude_folders:
                decorator_pre = '-'
                decorator_post = '\\'
                folders_ex = _decorate_data(PhMisc.DEFAULT_EXCLUDE_FOLDERS, decorator_pre, decorator_post)
            if exclude_files:
                decorator_pre = '-'
                decorator_post = ''
                files_ex = _decorate_data(PhMisc.DEFAULT_EXCLUDE_FILES
                                          , decorator_pre, decorator_post)
        return sep.join(filter(None, PhUtil.normalise_list([files_in, folders_in, folders_ex, files_ex])))
