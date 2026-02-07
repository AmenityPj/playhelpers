from ._git_info import GIT_SUMMARY
from ._tool_name import TOOL_NAME, TOOL_TITLE, TOOL_PACKAGE_NAME
from .ph_defaults import PhDefaults

_run_time = False
try:
    from ._version import __version__

    # this is available post installation, run time only,
    _run_time = True
except ImportError:
    pass


class PhConfigConst:
    TOOL_VERSION = __version__.public() if _run_time else PhDefaults.VERSION
    TOOL_VERSION_DETAILED = f'v{TOOL_VERSION}'
    TOOL_NAME = TOOL_NAME
    TOOL_TITLE = TOOL_TITLE
    TOOL_PACKAGE_NAME = TOOL_PACKAGE_NAME
    TOOL_GIT_SUMMARY = GIT_SUMMARY
    TOOL_DESCRIPTION = f'A Python software package suite to provide various utility functions.'
    TOOL_META_DESCRIPTION = f'{TOOL_DESCRIPTION}'
    TOOL_META_KEYWORDS = f'{TOOL_TITLE}, Common Functions, Funcs, Util, Utility'
    TOOL_URL = 'https://github.com/AmenityPj/playhelpers'
    TOOL_URL_BUG_TRACKER = 'https://github.com/AmenityPj/playhelpers/issues'
