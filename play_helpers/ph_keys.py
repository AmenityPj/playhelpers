class PhKeys:
    #####################
    # asn1Play
    INPUT_FORMAT = 'input_format'
    OUTPUT_FORMAT = 'output_format'
    ASN1_ELEMENT = 'asn1_element'
    TLV_PARSING_OF_OUTPUT = 'tlv_parsing_of_output'
    RE_PARSE_OUTPUT = 're_parse_output'

    # asn1Play Web
    INPUT_FORMATS = 'input_formats'
    INPUT_FORMAT_SELECTED = 'input_format_selected'
    OUTPUT_FORMATS = 'output_formats'
    OUTPUT_FORMAT_SELECTED = 'output_format_selected'

    # asn1
    ASN1_SCHEMA = 'asn1_schema'
    ASN1_OBJECT = 'asn1_object'
    ASN1_OBJECT_ALTERNATE = 'asn1_object_alternate'
    FETCH_ASN1_OBJECTS_LIST = 'fetch_asn1_objects_list'

    # asn1 source
    ASN1_SOURCE_PATH_ORG = 'original'
    ASN1_SOURCE_PATH_MODIFIED = 'modified'
    ASN1_SOURCE_PATH_FORMATTED = 'formatted'

    # asn1 Web
    ASN1_SCHEMAS = 'asn1_schemas'
    ASN1_SCHEMA_SELECTED = 'asn1_schema_selected'
    ASN1_OBJECTS = 'asn1_objects'
    ASN1_OBJECT_SELECTED = 'asn1_object_selected'

    # tlvPlay
    ONE_LINER = 'one_liner'
    VALUE_IN_ASCII = 'value_in_ascii'
    LENGTH_IN_DECIMAL = 'length_in_decimal'
    NON_TLV_NEIGHBOR = 'non_tlv_neighbor'

    # qrPlay
    # OUTPUT_FORMAT = 'output_format'
    SIZE = 'size'
    QR_CODE_VERSION = 'qr_code_version'
    SPLIT_QRS = 'split_qrs'
    DECORATE_QR = 'decorate_qr'
    LABEL = 'label'
    LABEL_POSITION = 'label_position'

    # qrPlay Web
    SIZES = 'sizes'
    SIZE_SELECTED = 'size_selected'
    QR_CODE_VERSIONS = 'qr_code_versions'
    QR_CODE_VERSION_SELECTED = 'qr_code_version_selected'

    # certPlay
    URL_PRE_ACCESS = 'url_pre_access'
    URL_CERT_FETCH_ONLY = 'url_cert_fetch_only'
    URL_ALL_CERTS = 'url_all_certs'

    # certPlay Web
    URL_TIME_OUT = 'url_time_out'
    URL_TIME_OUTS = 'url_time_outs'
    URL_TIME_OUT_SELECTED = 'url_time_out_selected'

    # dataPlay
    CONTENT_MAPPINGS = 'content_mappings'
    NAME_MAPPINGS = 'name_mappings'
    DELETE_BLOCK = 'delete_block'
    BLOCK_LEVEL = 'block_level'
    INCLUDE_SEARCH_PATTERN = 'include_search_pattern'
    INCLUDE_SEARCH_PATTERN_IS_REGEX = 'include_search_pattern_is_regex'
    EXCLUDE_SEARCH_PATTERN = 'exclude_search_pattern'
    EXCLUDE_SEARCH_PATTERN_IS_REGEX = 'exclude_search_pattern_is_regex'
    REPLACE_WITH = 'replace_with'
    REPLACE_WITH_IS_REGEX = 'replace_with_is_regex'
    INCLUDE_START_BLOCK_PATTERN = 'include_start_block_pattern'
    INCLUDE_START_BLOCK_PATTERN_IS_REGEX = 'include_start_block_pattern_is_regex'
    EXCLUDE_START_BLOCK_PATTERN = 'exclude_start_block_pattern'
    EXCLUDE_START_BLOCK_PATTERN_IS_REGEX = 'exclude_start_block_pattern_is_regex'
    INCLUDE_END_BLOCK_PATTERN = 'include_end_block_pattern'
    INCLUDE_END_BLOCK_PATTERN_IS_REGEX = 'include_end_block_pattern_is_regex'
    EXCLUDE_END_BLOCK_PATTERN = 'exclude_end_block_pattern'
    EXCLUDE_END_BLOCK_PATTERN_IS_REGEX = 'exclude_end_block_pattern_is_regex'

    #####################
    # Others
    PH_KEYS = 'PhKeys'

    #
    TRANSACTION_ID = 'transaction_id'
    INFO_DATA = 'info_data'

    #
    ARCHIVE_OUTPUT_FORMAT = 'archive_output_format'
    ARCHIVE_OUTPUT_FORMATS = 'archive_output_formats'
    ARCHIVE_OUTPUT_FORMAT_SELECTED = 'archive_output_format_selected'

    #
    SAMPLE = 'sample'
    SAMPLES = 'samples'
    SAMPLE_SELECTED = 'sample_selected'

    RE_PARSED_DATA = 're_parsed_data'
    ASN1_MODULE = 'asn1_module'
    ASN1_MODULE_VERSION = 'asn1_module_version'

    #
    ENCODING = 'encoding'
    ENCODING_POOL = 'encoding_pool'
    ENCODING_SELECTED = 'encoding_selected'
    ENCODING_ERRORS = 'encoding_errors'
    ENCODING_ERRORS_POOL = 'encoding_errors_pool'
    ENCODING_ERRORS_SELECTED = 'encoding_errors_selected'

    # Batch
    BATCH_PARAMS = 'batch_params'

    # Process
    PROCESS = 'process'
    PROCESS_INPUT = 'process_input'
    PROCESS_RESET = 'process_reset'
    PROCESS_COPY_CLIPBOARD = 'process_copy_clipboard'
    PROCESS_DOWNLOAD_OUTPUT = 'process_download_output'
    PROCESS_DOWNLOAD_YML = 'process_download_yml'
    PROCESS_SAMPLE = 'process_sample'
    PROCESS_SAMPLE_RANDOM = 'process_sample_random'

    # Sample
    SAMPLE_OPTION = 'sample_option'
    SAMPLE_LOAD_ONLY = 'load_only'
    SAMPLE_LOAD_AND_SUBMIT = 'load_and_submit'

    # Dates
    DATE_FIRST_AVAILABLE = 'date_first_available'
    DATE_LAST_UPDATE = 'date_last_updated'

    # App Parent
    APP_PARENT_TITLE = 'app_parent_title'
    APP_PARENT_VERSION = 'app_parent_version'

    # Result
    RESULT = 'result'
    RESULT_PROCESSED = 'result_processed'
    RESULT_UNPROCESSED = 'result_unprocessed'

    # App
    APP_TITLE = 'app_title'
    APP_HEADER = 'app_header'
    APP_HEADER_PRE = 'app_header_pre'
    APP_HEADER_POST = 'app_header_post'
    APP_DESCRIPTION = 'app_description'
    APP_DESCRIPTION_LEVEL_1 = 'app_description_level_1'
    APP_DESCRIPTION_LEVEL_2 = 'app_description_level_2'
    APP_DESCRIPTION_LEVEL_3 = 'app_description_level_3'
    APP_DESCRIPTION_LEVEL_4 = 'app_description_level_4'
    APP_DESCRIPTION_LEVEL_5 = 'app_description_level_5'
    APP_DESCRIPTION_LEVEL_6 = 'app_description_level_6'
    APP_META_DESCRIPTION = 'app_meta_description'
    APP_META_KEYWORDS = 'app_meta_keywords'
    APP_META_AUTHOR = 'app_meta_author'
    APP_VERSION = 'app_version'
    APP_GITHUB_URL = 'app_github_url'
    APP_GITHUB_PAGES_URL = 'app_github_pages_url'
    APP_GIT_SUMMARY = 'app_git_summary'
    APP_URL = 'app_url'
    APP_URL_ALT = 'app_url_alt'
    APP_URL_API = 'app_url_api'
    APP_TEMPLATE = 'app_template'
    APP_HOST = 'app_host'
    APP_END_POINT = 'app_end_point'
    APP_CODE = 'app_code'
    APP_CANONICAL_URL = 'app_canonical_url'
    APP_STATS_ID = 'app_stats_id'
    NAV_BAR_APP_ITEMS = 'nav_bar_app_items'

    #
    CFG_HIGHLIGHT_SYNTAX = 'cfg_highlight_syntax'
    CFG_HIGHLIGHT_SYNTAX_LANGUAGE = 'cfg_highlight_syntax_language'
    CFG_HIGHLIGHT_SYNTAX_STYLE = 'cfg_highlight_syntax_style'
    CFG_COUNTERS_STATS = 'cfg_counters_stats'
    CFG_COUNTERS_STATS_FORMAT = 'cfg_counters_stats_format'

    #
    ALERT_CSS_CLASS_DANGER = 'danger'
    ALERT_CSS_CLASS_DARK = 'dark'
    ALERT_CSS_CLASS_DISMISSIBLE = 'dismissible'
    ALERT_CSS_CLASS_HEADING = 'heading'
    ALERT_CSS_CLASS_INFO = 'info'
    ALERT_CSS_CLASS_LIGHT = 'light'
    ALERT_CSS_CLASS_LINK = 'link'
    ALERT_CSS_CLASS_PRIMARY = 'primary'
    ALERT_CSS_CLASS_SECONDARY = 'secondary'
    ALERT_CSS_CLASS_SUCCESS = 'success'
    ALERT_CSS_CLASS_WARNING = 'warning'

    #
    TESTIMONIAL_POSTS = 'testimonial_posts'
    TESTIMONIAL_POST = 'testimonial_post'
    TESTIMONIAL_POST_ID = 'testimonial_post_id'
    TESTIMONIAL_POST_TITLE = 'testimonial_post_title'
    TESTIMONIAL_POST_CONTENT = 'testimonial_post_content'
    TESTIMONIAL_POST_PUBLISHER = 'testimonial_post_publisher'
    TESTIMONIAL_POST_CREATED = 'testimonial_post_created'

    #
    TEST_CASE_ID = 'test_case_id'
    TEST_CASE_NAME = 'test_case_name'
    TEST_CASE_FILE_NAME = 'test_case_file_name'

    #
    LOGIN_USER_NAME = 'login_user_name'
    LOGIN_USER_NAME = 'login_pass_word'

    INFO = 'info'
    VERSION = 'version'
    MODE = 'mode'
    PRINT_INPUT = 'print_input'
    PRINT_OUTPUT = 'print_output'
    PRINT_INFO = 'print_info'
    ARCHIVE_OUTPUT = 'archive_output'
    OUTPUT_PATH = 'output_path'
    RE_OUTPUT_PATH = 're_output_path'
    QUITE_MODE = 'quite_mode'
    DATA_GROUP = 'data_group'
    REMARKS = 'remarks'
    REMARKS_GENERATED = 'remarks_generated'
    DEFAULT = 'default'
    UNKNOWN = 'unknown'
    LENGTH = 'length'

    #
    INPUT = 'input'
    INPUT_DATA = 'input_data'
    INPUT_FILE = 'input_file'
    INPUT_LIST = 'input_list'
    INPUT_TUPLE = 'input_tuple'
    INPUT_DICT = 'input_dict'
    INPUT_DIR = 'input_dir'
    INPUT_YML = 'input_yml'
    INPUT_MODES_HIERARCHY = 'input_modes_hierarchy'
    INPUT_ENCODING = 'input_encoding'
    INPUT_ENCODING_ERRORS = 'input_encoding_errors'

    #
    EXPORT_FILE = 'export_file'
    OUTPUT_FILE_NAME_KEYWORD = 'output_file_name_keyword'
    #
    OUTPUT = 'output'
    OUTPUT_DATA = 'output_data'
    OUTPUT_FILE = 'output_file'
    OUTPUT_LIST = 'output_list'
    OUTPUT_TUPLE = 'output_tuple'
    OUTPUT_DIC = 'output_dic'
    OUTPUT_DIR = 'output_dir'
    OUTPUT_YML = 'output_yml'
    OUTPUT_MODES_HIERARCHY = 'output_modes_hierarchy'
    OUTPUT_ENCODING = 'output_encoding'
    OUTPUT_ENCODING_ERRORS = 'output_encoding_errors'

    #
    VAR_EXECUTION_MODE = 'execution_mode'
    VAR_ERROR_HANDLING_MODE = 'error_handling_mode'
    VAR_TOP_FOLDER_PATH = 'top_folder_path'

    #
    GET = 'GET'
    POST = 'POST'

    #
    OUTPUT_VERSION = 'output_version'

    #
    PYTHON = 'Python'
    SGP22 = 'SGP22'
    SGP32 = 'SGP32'
    ASN1PLAY = 'asn1play'
    EUICC_PROFILE_PACKAGE = 'eUICC_Profile_Package'
    PYTHONHELPERS = 'pythonHelpers'
    TIME_STAMP = 'time_stamp'

    #
    COMPILE_TIME = 'compile_time'
    RUN_TIME = 'run_time'

    #
    API = 'api'
    LOG = 'log'
    INTERNAL = 'internal'
    ROOT_PATH = 'root_path'

    # traverse
    TRAVERSE_MODE = 'traverse_mode'
    INCLUDE_FILES = 'include_files'
    INCLUDE_DIRS = 'include_dirs'
    EXCLUDES = 'excludes'

    #
    BEFORE = 'Before: '
    AFTER = 'After : '

    # Deprecated
    # Start
    # SAMPLE_1 = 'sample_1'
    # SAMPLE_2 = 'sample_2'
    # SAMPLE_3 = 'sample_3'
    # SAMPLE_4 = 'sample_4'
    # SAMPLE_5 = 'sample_5'
    # SAMPLE_6 = 'sample_6'
    # SAMPLE_7 = 'sample_7'
    # SAMPLE_8 = 'sample_8'
    # SAMPLE_9 = 'sample_9'
    # SAMPLE_10 = 'sample_10'
    # **DEPRECATED**
    RAW_DATA = 'raw_data'
    # ** DEPRECATED **
    REMARKS_LIST = 'remarks_list'
    # ** DEPRECATED **
    IMAGE_FORMAT = 'image_format'
    # ** DEPRECATED **
    SCALE = 'scale'
    # REMARKS_LIST_GENERATED = 'remarks_list_generated'
    # SAMPLE_PROCESSING = 'sample_processing'
    # End
