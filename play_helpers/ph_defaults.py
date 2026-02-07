from play_helpers.ph_constants import PhConstants
from play_helpers.ph_file_extensions import PhFileExtensions
from play_helpers.ph_modes_error_handling import PhErrorHandlingModes
from play_helpers.ph_modes_execution import PhExecutionModes


class PhDefaults:
    #############
    # Version Objects
    #############
    VERSION = '1.0.1'
    #############
    # Generic Objects
    #############
    CHAR_ENCODING = PhConstants.CHAR_ENCODING_UTF8
    CHAR_ENCODING_ERRORS = PhConstants.CHAR_ENCODING_ERRORS_REPLACE
    EXECUTION_MODE = PhExecutionModes.USER
    ERROR_HANDLING_MODE = PhErrorHandlingModes.CONTINUE_ON_ERROR
    ARCHIVE_FORMAT = PhFileExtensions.ZIP
    #############
    # Data Objects
    #############
    # Common Objects
    # INPUT_DATA
    PRINT_INPUT = True
    PRINT_OUTPUT = True
    PRINT_INFO = True
    QUITE_MODE = False
    # REMARKS
    ENCODING = CHAR_ENCODING
    ENCODING_ERRORS = CHAR_ENCODING_ERRORS
    OUTPUT_PATH = ''
    OUTPUT_FILE_NAME_KEYWORD = ''
    ARCHIVE_OUTPUT = True
    ARCHIVE_OUTPUT_FORMAT = ARCHIVE_FORMAT


class PhDefaultTypesInclude:
    # Common Objects
    # INPUT_DATA
    PRINT_INPUT = bool
    PRINT_OUTPUT = bool
    PRINT_INFO = bool
    QUITE_MODE = bool
    # REMARKS
    ENCODING = str
    ENCODING_ERRORS = str
    OUTPUT_PATH = str
    ARCHIVE_OUTPUT = bool
    ARCHIVE_OUTPUT_FORMAT = str


class PhDefaultTypesExclude:
    # Common Objects
    INPUT_DATA = [int, float, bool]
