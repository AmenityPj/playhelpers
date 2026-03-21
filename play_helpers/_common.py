import re

from play_helpers.ph_constants import PhConstants
from play_helpers.ph_keys import PhKeys


class _PhCommon:
    """
    This Class is mainly creates to avoid 'circular import' scenarios.

    Sample Error:
    ImportError: cannot import name 'PhUtil' from partially initialized module 'play_helpers.ph_util' (most likely due to a circular import) (D:\Other\Github_Self\playHelpers\play_helpers\ph_util.py)
    """

    @classmethod
    def get_key_value_pair(cls, key, value, sep=PhConstants.SEPERATOR_ONE_LINE, dic_format=False, print_also=False,
                           log=None, user_friendly_key=True, pair_is_must=False, length_needed=False):
        """

        :param length_needed:
        :param key:
        :param value:
        :param sep:
        :param dic_format:
        :param print_also:
        :param log:
        :param user_friendly_key:
        :param pair_is_must:
        :return:
        """
        print_or_log = log.info if log else print
        if key is None:
            return None
        if value is None:
            if pair_is_must is True:
                return None
            value = ''
        if length_needed:
            if PhKeys.LENGTH not in key:
                key = f'{key}_{PhKeys.LENGTH}'
            value = len(str(value))
        str_data = f'{cls.get_user_friendly_name(key) if user_friendly_key else key}{sep}{value}'
        if print_also:
            print_or_log(str_data)
        if dic_format:
            return {key: value}
        return str_data

    @classmethod
    def get_user_friendly_name(cls, python_variable_name):
        """

        :param python_variable_name:
        :return:
        """
        temp_data = re.sub(r'[_]', repl=' ', string=python_variable_name)
        return temp_data.title()
