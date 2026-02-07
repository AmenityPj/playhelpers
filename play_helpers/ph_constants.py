# import pandas as pd
from enum import Enum


class PhConstants:
    # Mutable Data Type; use copy.copy(x) to create object without reference
    DICT_EMPTY = {}
    # Mutable Data Type; use copy.copy(x) to create object without reference
    LIST_EMPTY = []
    # Mutable Data Type; use copy.copy(x) to create object without reference
    SET_EMPTY = set()
    # Immutable Data Type
    TUPLE_EMPTY = ((),)
    # Immutable Data Type
    STR_EMPTY = ''
    # TODO: Causing issues in setup.py as module is not installed during setup.
    # No Module Names Pandas
    # Value Mutable; but favor immutability
    # DF_EMPTY = pd.DataFrame()

    STR_TAB = '    '
    STR_SPACE = ' '

    STR_CURLY_BRACE_START = '{'
    STR_CURLY_BRACE_END = '}'

    OFFSET_ZERO = 0
    OFFSET_ONE = 1
    OFFSET_NAME_FOR_OUTPUT_FILE = 0
    OFFSET_NAME_FOR_ASN_FILE = 1
    KEYWORD_VARIABLE_DECLARATION_IN = ['var_In', 'var_in_list', 'var_in']
    KEYWORD_VARIABLE_DECLARATION_OUT = ['var_Out', 'varlist', 'var_out', 'VAR_OUT', 'Var_Out']
    KEYWORD_VARIABLE_QUANTITY = ['Quantity', 'Count']
    PLACE_HOLDERS_FOR_VARIABLES = ['${VAR}', '${VAR  }', '${VAR    }']

    # 0th offset contains most preferred name for output file
    # 1st offset contains most preferred name for ASN file (if Applicable)
    VAR_POOL_ICCID_WO_CHECKSUM = ['SER_NB', 'Ser_nb']
    VAR_POOL_ICCID = ['ICCID', 'iccid', 'ICCID_FROM'] + VAR_POOL_ICCID_WO_CHECKSUM
    VAR_POOL_IMSI = ['IMSI', 'imsi', 'IMSI_FROM']
    VAR_POOL_IMSI2 = ['imsi2', 'imsi-9009-2601-rec2']
    VAR_POOL_KI = ['KI', 'key', 'ki', 'KEY']
    VAR_POOL_PIN1 = ['PIN1', 'pinAppl1', 'CHV1', 'PIN', 'CHV']
    VAR_POOL_PIN2 = ['PIN2', 'pinAppl2', 'CHV2', ]
    VAR_POOL_PUK1 = ['PUK1', 'pukAppl1', 'PUK']
    VAR_POOL_PUK2 = ['PUK2', 'pukAppl2']
    VAR_POOL_ADM1 = ['ADM1', 'adm1', 'ISC1', 'ADM1_0A', 'ADM', 'ADMIN']
    VAR_POOL_ADM2 = ['ADM2', 'adm2', 'ISC2', 'ADM1_0B']
    VAR_POOL_ADM3 = ['ADM3', 'adm3', 'ISC3', 'ADM1_0C']
    VAR_POOL_ADM4 = ['ADM4', 'adm4', 'ISC4', 'ADM1_0D']
    VAR_POOL_ADM5 = ['ADM5', 'adm5', 'ISC5', 'ADM1_0E']
    VAR_POOL_KIC1 = ['KIC1', 'kic1IsdR', 'KIC', 'KIC_KID']
    VAR_POOL_KID1 = ['KID1', 'kid1IsdR', 'KID', 'KIC_KID']
    VAR_POOL_KIK1 = ['KIK1', 'kik1IsdR', 'KIK']
    VAR_POOL_KIC2 = ['KIC2', 'kic1IsdP']
    VAR_POOL_KID2 = ['KID2', 'kid1IsdP']
    VAR_POOL_KIK2 = ['KIK2', 'kik1IsdP']
    VAR_POOL_MNO_SD_KIC_01 = ['KIC01', 'mno_sd_kic_01']
    VAR_POOL_MNO_SD_KID_01 = ['KID01', 'mno_sd_kid_01']
    VAR_POOL_MNO_SD_KIK_01 = ['KIK01', 'mno_sd_kik_01']
    VAR_POOL_MNO_SD_KIC_02 = ['KIC02', 'mno_sd_kic_02']
    VAR_POOL_MNO_SD_KID_02 = ['KID02', 'mno_sd_kid_02']
    VAR_POOL_MNO_SD_KIK_02 = ['KIK02', 'mno_sd_kik_02']
    VAR_POOL_MNO_SD_KIC_03 = ['KIC03', 'mno_sd_kic_03']
    VAR_POOL_MNO_SD_KID_03 = ['KID03', 'mno_sd_kid_03']
    VAR_POOL_MNO_SD_KIK_03 = ['KIK03', 'mno_sd_kik_03']
    VAR_POOL_MNO_SD_KIC_04 = ['KIC04', 'mno_sd_kic_04']
    VAR_POOL_MNO_SD_KID_04 = ['KID04', 'mno_sd_kid_04']
    VAR_POOL_MNO_SD_KIK_04 = ['KIK04', 'mno_sd_kik_04']
    VAR_POOL_MNO_SD_KIC_05 = ['KIC05', 'mno_sd_kic_05']
    VAR_POOL_MNO_SD_KID_05 = ['KID05', 'mno_sd_kid_05']
    VAR_POOL_MNO_SD_KIK_05 = ['KIK05', 'mno_sd_kik_05']
    VAR_POOL_MNO_SD_KIC_06 = ['KIC06', 'mno_sd_kic_06']
    VAR_POOL_MNO_SD_KID_06 = ['KID06', 'mno_sd_kid_06']
    VAR_POOL_MNO_SD_KIK_06 = ['KIK06', 'mno_sd_kik_06']
    VAR_POOL_MNO_SD_KIC_07 = ['KIC07', 'mno_sd_kic_07']
    VAR_POOL_MNO_SD_KID_07 = ['KID07', 'mno_sd_kid_07']
    VAR_POOL_MNO_SD_KIK_07 = ['KIK07', 'mno_sd_kik_07']
    VAR_POOL_MNO_SD_KIC_08 = ['KIC08', 'mno_sd_kic_08']
    VAR_POOL_MNO_SD_KID_08 = ['KID08', 'mno_sd_kid_08']
    VAR_POOL_MNO_SD_KIK_08 = ['KIK08', 'mno_sd_kik_08']
    VAR_POOL_MNO_SD_KIC_09 = ['KIC09', 'mno_sd_kic_09']
    VAR_POOL_MNO_SD_KID_09 = ['KID09', 'mno_sd_kid_09']
    VAR_POOL_MNO_SD_KIK_09 = ['KIK09', 'mno_sd_kik_09']
    VAR_POOL_MNO_SD_KIC_0A = ['KIC0A', 'mno_sd_kic_0A']
    VAR_POOL_MNO_SD_KID_0A = ['KID0A', 'mno_sd_kid_0A']
    VAR_POOL_MNO_SD_KIK_0A = ['KIK0A', 'mno_sd_kik_0A']
    VAR_POOL_MNO_SD_KIC_0B = ['KIC0B', 'mno_sd_kic_0B']
    VAR_POOL_MNO_SD_KID_0B = ['KID0B', 'mno_sd_kid_0B']
    VAR_POOL_MNO_SD_KIK_0B = ['KIK0B', 'mno_sd_kik_0B']
    VAR_POOL_MNO_SD_KIC_0C = ['KIC0C', 'mno_sd_kic_0C']
    VAR_POOL_MNO_SD_KID_0C = ['KID0C', 'mno_sd_kid_0C']
    VAR_POOL_MNO_SD_KIK_0C = ['KIK0C', 'mno_sd_kik_0C']
    VAR_POOL_MNO_SD_KIC_0D = ['KIC0D', 'mno_sd_kic_0D']
    VAR_POOL_MNO_SD_KID_0D = ['KID0D', 'mno_sd_kid_0D']
    VAR_POOL_MNO_SD_KIK_0D = ['KIK0D', 'mno_sd_kik_0D']
    VAR_POOL_MNO_SD_KIC_0E = ['KIC0E', 'mno_sd_kic_0E']
    VAR_POOL_MNO_SD_KID_0E = ['KID0E', 'mno_sd_kid_0E']
    VAR_POOL_MNO_SD_KIK_0E = ['KIK0E', 'mno_sd_kik_0E']
    VAR_POOL_MNO_SD_KIC_0F = ['KIC0F', 'mno_sd_kic_0F']
    VAR_POOL_MNO_SD_KID_0F = ['KID0F', 'mno_sd_kid_0F']
    VAR_POOL_MNO_SD_KIK_0F = ['KIK0F', 'mno_sd_kik_0F']
    VAR_POOL_2_PIN1 = ['2PIN1', 'secondPINAppl1']
    VAR_POOL_2_PUK1 = ['2PUK1', 'secondPUKAppl1']
    VAR_POOL_3_PIN1 = ['3PIN1', 'secondPINAppl2']
    VAR_POOL_3_PUK1 = ['3PUK1', 'secondPUKAppl2']
    VAR_POOL_ACC = ['ACC', 'ef-acc', 'Access_Control']

    VAR_TYPE_IN = 1
    VAR_TYPE_OUT = 2
    VAR_TYPE_PROFILE = 3

    POOL_4_DIGITS_LENGTH = [
        'PIN1', 'PIN2', 'secondPINAppl1', 'secondPINAppl2'
    ]
    POOL_8_DIGITS_LENGTH = [
        'PUK1', 'PUK2', 'ADM1', 'ADM2', 'ADM3', 'ADM4', 'ADM5', 'secondPUKAppl1', 'secondPUKAppl2'
    ]
    POOL_16_BYTES_LENGTH = [
        'KI',
        'KIC1', 'KID1', 'KIK1',
        'KIC2', 'KID2', 'KIK2',
        'KIC01', 'KID01', 'KIK01',
        'KIC02', 'KID02', 'KIK02',
        'KIC03', 'KID03', 'KIK03',
        'KIC04', 'KID04', 'KIK04',
        'KIC05', 'KID05', 'KIK05',
        'KIC06', 'KID06', 'KIK06',
        'KIC07', 'KID07', 'KIK07',
        'KIC08', 'KID08', 'KIK08',
        'KIC09', 'KID09', 'KIK09',
        'KIC0A', 'KID0A', 'KIK0A',
        'KIC0B', 'KID0B', 'KIK0B',
        'KIC0C', 'KID0C', 'KIK0C',
        'KIC0D', 'KID0D', 'KIK0D',
        'KIC0E', 'KID0E', 'KIK0E',
        'KIC0F', 'KID0F', 'KIK0F',
    ]

    STR_TYPE_NUMERIC = 1
    STR_TYPE_NUMERIC_OCT = 2
    STR_TYPE_NUMERIC_BIN = 3

    STR_TYPE_HEX_LOWER_CASE = 11
    STR_TYPE_HEX_UPPER_CASE = 12
    STR_TYPE_HEX_RANDOM_CASE = 13

    STR_TYPE_ASCII_LOWER_CASE = 21
    STR_TYPE_ASCII_UPPER_CASE = 22
    STR_TYPE_ASCII_RANDOM_CASE = 32

    STR_TYPE_ALPHA_NUMERIC_LOWER_CASE = 30
    STR_TYPE_ALPHA_NUMERIC_UPPER_CASE = 31
    STR_TYPE_ALPHA_NUMERIC_RANDOM_CASE = 32

    STR_TYPE_PASSWORD_LOWER_CASE = 40
    STR_TYPE_PASSWORD_UPPER_CASE = 41
    STR_TYPE_PASSWORD_RANDOM_CASE = 42

    FILE_TYPE_IN = 1
    FILE_TYPE_OUT = 2

    AID_EUICC_ISDR_OR_UICC_ISD = 'A000000151000000'
    AID_EUICC_ISDP_INITIAL = 'A0000005591010'

    LENGTH_EF_ACC = 0x02
    LENGTH_IMSI = 0x08
    LENGTH_EF_IMSI = LENGTH_IMSI + 0x01
    LENGTH_PINS_PUKS_ADMS = 0x08
    LENGTH_SPN_STRING = 0x10
    LENGTH_EF_SPN = LENGTH_SPN_STRING + 0x01
    LENGTH_DIALING_NUMBER_DEFAULT = 0x0C
    LENGTH_SMSC = LENGTH_DIALING_NUMBER_DEFAULT
    LENGTH_MSISDN = LENGTH_DIALING_NUMBER_DEFAULT

    ONE_STEP_FORWARD = '/'
    MULTIPLE_STEPS_FORWARD = '/**/'
    ONE_STEP_BACKWARD = '/../'

    TRUE_VALUE_POOL = ('yes', 'true', 't', 'y', '1')
    FALSE_VALUE_POOL = ('no', 'false', 'f', 'n', '0')
    EXIT_VALUE_POOL = ('e', 'exit')
    USER_INPUT_OPTIONS = ' [Yes/No/Exit]: '
    MAX_SUPPORTED_DIGIT_IN_INT = 9
    FORMAT_HEX_STRING_AS_PACK = 1
    FORMAT_HEX_STRING_AS_HEX = 2
    FORMAT_HEX_STRING_AS_UPPERCASE = 4
    FORMAT_HEX_STRING_AS_COMMA = 8

    SEARCH_TYPE_PLAIN = 1
    SEARCH_TYPE_REGEX = 2

    FILE_EXTN_TMP = '.tmp'

    SEPERATOR_TWO_WORDS = ' '
    SEPERATOR_TWO_LINES = '\n'
    SEPERATOR_TWO_LINES_MULTI = '\n\n'
    SEPERATOR_FILE_NAME = '_'
    SEPERATOR_ONE_LINE = ': '
    SEPERATOR_KEY_VALUE = ': '
    SEPERATOR_INFO = ' => '
    SEPERATOR_MULTI_LINE = ':\n'
    SEPERATOR_MULTI_LINE_TABBED = ':\n\t'
    SEPERATOR_MULTI_OBJ = '; '
    SEPERATOR_NAME_VERSION = ' '
    SEPERATOR_TITLE = ' | '

    ENCLOSE_HEX = 1
    ENCLOSE_NAME_VALUE = 2
    ENCLOSE_NAME_VALUE_HEX = 3
    ENCLOSE_NAME_VALUE_DICT = 4
    ENCLOSE_NAME_VALUE_HEX_DICT = 5
    ENCLOSE_NAME_VALUE_SEQ_DICT = 6
    ENCLOSE_NAME_VALUE_SEQ = 7
    ENCLOSE_COMMENT = 8

    DEFAULT_TRIM_STRING = '...'
    DEFAULT_TRIM_STRING_LENGTH = len(DEFAULT_TRIM_STRING)

    HEADING_LENGTH_MAX = 120
    HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_SYMBOL = 2
    HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_WHITE_SPACES = 2

    REMARKS_MAX_LENGTH = HEADING_LENGTH_MAX - HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_SYMBOL - HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_WHITE_SPACES

    START_BLOCK = 1
    END_BLOCK = 2
    KNOWN = 'Known'
    UNKNOWN = 'UnKnown'
    PARENT = 21
    CHILD = 22
    DETAILS = 'Details'
    SUMMARY = 'Summary'
    EXCEPTION_OCCURRED = 'Exception Occurred'
    EXCEPTION_OCCURRED_AT_FUNC = 'Exception Occurred at function'
    EXPORT_ERROR = 'export error'
    READ_WRITE_ERROR = 'input/output path reading/writing error'
    WRITE_PATH_ERROR = 'output path writing error'
    TIME_OUT_ERROR = 'time out error'
    NON_ZERO_EXIT_STATUS_ERROR = 'non-zero exit status error'
    INPUTS_ERROR = 'Check all your Inputs'
    INVALID_RAW_DATA = 'Check your Raw Data'
    INVALID_INPUT_DATA = 'Check your Input Data'
    MISSING_INPUT_DATA = 'Missing Input Data'
    MISSING_INPUT_YML = 'Missing "input" in Yml Config'
    INCORRECT_BLOCK_STRUCTURE = 'Incorrect Block Structure; Opening and Closing Sequences are not matching'
    EMPTY_INPUT_FILE = 'Empty Input File'
    UNKNOWN_INPUT_FORMAT = 'Unknown Input Format'
    INVALID_TIME_OUT = 'Invalid Time Out'
    INVALID_URL_TIME_OUT = 'Invalid URL Time Out'
    ITEM = 'item'
    SUB = 'sub '
    KEY_DATE_TIME = 'Date & Time'

    ENV_VARIABLES = {}

    PUBLIC_IP_SERVICES_POOL = [
        'https://ifconfig.co/ip',  # Seems machine based protocol (IPV4/IPV6)
        'https://ipecho.net/plain',  # Seems machine based protocol (IPV4/IPV6)
        'https://checkip.amazonaws.com',  # Seems only IPV4
        'https://ipinfo.io/ip',  # Dedicated IPV4 & IPV6
        'https://api.ipify.org',  # Dedicated IPV4 & IPV6
        'https://icanhazip.com/',  # Dedicated IPV4 & IPV6
        'https://ident.me',  # Dedicated IPV4 & IPV6
    ]

    PUBLIC_IP_SERVICES_IPV4_POOL = [
        'https://ipinfo.io/ip',
        'https://api.ipify.org/',
        'https://ipv4.icanhazip.com/',
        'https://v4.ident.me/',
    ]
    PUBLIC_IP_SERVICES_IPV6_POOL = [
        'https://v6.ipinfo.io/ip',
        'https://api64.ipify.org/',
        'https://ipv6.icanhazip.com/',
        'https://v6.ident.me/',
    ]

    STR_SELECT_OPTION = '-- Select --'
    STR_OTHER_OPTION = '-- Other --'

    CHAR_ENCODING_ASCII = 'ascii'
    CHAR_ENCODING_UTF8 = 'utf-8'
    CHAR_ENCODING_ISO_8859 = 'ISO-8859-1'
    CHAR_ENCODING_CP_1252 = 'cp1252'

    CHAR_ENCODING_POOL = [
        CHAR_ENCODING_ASCII,
        CHAR_ENCODING_UTF8,
        CHAR_ENCODING_ISO_8859,
        CHAR_ENCODING_CP_1252,
    ]

    CHAR_ENCODING_ERRORS_STRICT = 'strict'
    CHAR_ENCODING_ERRORS_IGNORE = 'ignore'
    CHAR_ENCODING_ERRORS_REPLACE = 'replace'

    # Copied from "venv/Lib/site-packages/pandas/_typing.py"
    CHAR_ENCODING_ERRORS_POOL = [
        CHAR_ENCODING_ERRORS_STRICT,
        CHAR_ENCODING_ERRORS_IGNORE,
        CHAR_ENCODING_ERRORS_REPLACE,
        'surrogateescape',
        'xmlcharrefreplace',
        'backslashreplace',
        'namereplace',
    ]

    CRLF = '\r\n'
    LF = '\n'
    WINDOWS_LINE_ENDING = CRLF
    UNIX_LINE_ENDING = LF

    BEGIN_CERTIFICATE = '-----BEGIN CERTIFICATE-----'
    END_CERTIFICATE = '-----END CERTIFICATE-----'
    CERTIFICATE = 'CERTIFICATE'
    OPEN_SSL_CERTIFICATE_COMMENTS = '-'

    YES = True
    NO = False

    DIR_CREATION = 1
    DIR_DELETION = 2

    TEST_DATA_A_Z_LOWER_LEN_26 = 'abcdefghijklmnopqrstuvwxyz'
    TEST_DATA_A_Z_UPPER_LEN_26 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    TEST_DATA_0_9_LEN_10 = '0123456789'
    TEST_DATA_SYMBOL_LEN_13 = '~!@#$%^&*()_+'
    TEST_DATA_MIX_LEN_75 = TEST_DATA_A_Z_LOWER_LEN_26 + TEST_DATA_0_9_LEN_10 + TEST_DATA_A_Z_UPPER_LEN_26 + TEST_DATA_SYMBOL_LEN_13

    # '**DEPRECATED**'
    # DECODE_MODE_ASCII = 'ascii'
    # '**DEPRECATED**'
    # DECODE_MODE_UTF8 = 'utf-8'
    # '**DEPRECATED**'
    # STR_ENCODING_FORMAT_ASCII = 'ascii'
    # '**DEPRECATED**'
    # STR_ENCODING_FORMAT_UTF8 = 'utf-8'
    # '**DEPRECATED**'
    # STR_ENCODING_FORMAT_ISO_8859 = 'ISO-8859-1'
    # '**DEPRECATED**'
    # STR_ENCODING_FORMAT_CP_1252 = 'cp1252'
    # '**DEPRECATED**'
    # STR_ENCODING_ERRORS_IGNORE = 'ignore'
    # '**DEPRECATED**'
    # STR_ENCODING_ERRORS_REPLACE = 'replace'
    # '**DEPRECATED**'
    # STR_TYPE_HEX = STR_TYPE_HEX_UPPER_CASE
    # '**DEPRECATED**'
    # STR_TYPE_PLAIN = STR_TYPE_ALPHA_NUMERIC_RANDOM_CASE

    class Position(Enum):
        TOP = 1
        RIGHT = 2
        BOTTOM = 3
        LEFT = 4
