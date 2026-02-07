class PhExecutionModes:
    USER = 1
    DEV = 2
    KNOWN_ISSUES = 22
    UNIT_TESTING = 3
    SAMPLE_SPECIFIC = 4
    SAMPLE_GENERIC = 5
    ALL = 6
    UNIT_TESTING_EXTERNAL = 7
    SAMPLES_LIST = 8
    CLI = 9
    PJ_EXCLUSIVE = 999

    KEYS_NAME = {
        USER: 'user',
        DEV: 'dev',
        KNOWN_ISSUES: 'known_issues',
        UNIT_TESTING: 'unit_testing',
        SAMPLE_SPECIFIC: 'sample_specific',
        SAMPLE_GENERIC: 'sample_generic',
        ALL: 'all',
        UNIT_TESTING_EXTERNAL: 'unit_testing_external',
        SAMPLES_LIST: 'samples_list',
        CLI: 'cli',
        PJ_EXCLUSIVE: 'pj_exclusive',
    }

    @classmethod
    def get_key_name(cls, key):
        return cls.KEYS_NAME.get(key, key)
