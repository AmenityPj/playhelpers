import base64
import copy
import ctypes
import enum
import fnmatch
import inspect
import math
import os
import random
import re
import secrets
import shutil
import string
import sys
import time
import zipfile
from binascii import unhexlify
from datetime import datetime
from io import TextIOWrapper, StringIO

import pandas as pd
import pkg_resources
import requests
import tzlocal
from packaging import version
from pandas import DataFrame, Series
from ruamel.yaml.scalarstring import PreservedScalarString

from play_helpers.ph_constants import PhConstants
from play_helpers.ph_constants_config import PhConfigConst
from play_helpers.ph_defaults import PhDefaults
from play_helpers.ph_file_extensions import PhFileExtensions
from play_helpers.ph_git import PhGit
from play_helpers.ph_keys import PhKeys
from ._expired_attributes import __expired_attributes__
from .ph_modules import PhModules

"""
Default Flags
"""
_base_profiles_available = False
_psutil_available = True
_debug = False
_ctypes_windll_available = True
_pwd_available = True

"""
Conditional Flags
"""
try:
    import psutil
except ImportError:
    _psutil_available = False
try:
    from ctypes import windll
    # this is available only in Windows
except ImportError:
    _ctypes_windll_available = False
try:
    import pwd
    # this is available only in Unix
except ImportError:
    _pwd_available = False

"""
User Choice
"""


# _debug = True


class PhUtil:

    # init method or constructor
    def __init__(self):
        pass

    def __call__(self):
        pass

    def __getattr__(attr):

        # Warn for expired attributes
        if attr in __expired_attributes__:
            key_name = attr
            details_dic = __expired_attributes__.get(attr)
            since = f" {details_dic.get('since')} release." if 'since' in details_dic else None
            alternate = f", use {details_dic.get('alternate')} instead !!!" if 'alternate' in details_dic else None
            raise AttributeError(''.join(filter(None, [
                f"`{attr}` was removed in the PythonHelpers",
                f'{since}',
                f'{alternate}',
            ])))
            # f"`np.{attr}` was removed in the NumPy 2.0 release. "
            # f"{__expired_attributes__[attr]}"

    # path_current_folder = os.getcwd()
    path_current_folder = os.path.realpath(sys.path[0])
    path_current_script = __file__
    name_current_script = os.path.basename(__file__)
    path_default_res_folder = path_current_folder + os.sep + 'res'
    path_default_log_folder = path_current_folder + os.sep + 'logs'
    path_default_out_folder = path_current_folder + os.sep + 'out'
    path_default_data_folder = path_current_folder + os.sep + 'data'
    path_default_tst_folder = path_current_folder + os.sep + 'tests'
    path_default_bkp_folder = path_current_folder + os.sep + 'backup'
    path_default_data_bkp_folder = os.sep.join([path_current_folder, 'data', 'backup'])
    # Sample Data:
    # in Real Environment: D:\ProgramFiles\Python37
    # in Virtual Environment: D:\Other\Github_Self\asn1Play\venv\Scripts
    path_python_folder = os.path.split(sys.executable)[0]
    path_python_script_folder = os.sep.join([path_python_folder, 'Scripts']) if not path_python_folder.endswith(
        'Scripts') else path_python_folder
    path_python_executable = sys.executable

    @classmethod
    def test(cls, actual, expected):
        """
        Simple provided test() function used in other functions() to print what each function returns vs. what it's
        supposed to return.
        :param actual: any Object (Actual Output)
        :param expected: any Object (Expected Output)
        :return: None
        """
        if actual == expected:
            prefix = ' OK '
        else:
            prefix = '    X '
        print('%s got: %s, expected: %s' % (prefix, repr(actual), repr(expected)))

    @classmethod
    def trim_and_kill_all_white_spaces(cls, str_data):
        return re.sub(r'\s+', '', str_data)
        # return str_data.translate({ord(c): None for c in string.whitespace})

    @classmethod
    def trim_and_kill_extra_white_spaces(cls, str_data):
        return re.sub(r'\s+', ' ', str_data).strip()

    @classmethod
    def trim_white_spaces_in_str(cls, data):
        return data.strip() if isinstance(data, str) else data

    @classmethod
    def is_hex(cls, s):
        # Don't verify length here; this is just to verify String Type
        return all(c in string.hexdigits for c in s)

    @classmethod
    def is_numeric(cls, s):
        return all(c in string.digits for c in s)

    @classmethod
    def is_ascii(cls, s):
        return all(c in (string.ascii_letters + string.digits) for c in s)

    @classmethod
    def is_base64(cls, s):
        """
        Data Set is: [A-Za-z0-9+/]
        :param s: 
        :return: 
        """
        return True if re.search(re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'),
                                 s) else False

    @classmethod
    def decode_to_base64_if_hex(cls, raw_data):
        """

        :param raw_data:
        :return:
        """
        if cls.is_hex(raw_data):
            return base64.b64encode(unhexlify(raw_data)).decode()
        return raw_data

    @classmethod
    def decode_to_hex_if_base64(cls, raw_data):
        """

        :param raw_data:
        :return:
        """
        if not cls.is_hex(raw_data) and cls.is_base64(raw_data):
            return base64.b64decode(raw_data).hex()
        return raw_data

    @classmethod
    def len_hex(cls, str_hex_data, output_in_str_format=False):
        data_len = int(len(str_hex_data) / 2)
        return '%02X' % data_len if output_in_str_format else data_len

    @classmethod
    def len_odd(cls, str_data):
        return True if len(str_data) % 2 else False

    @classmethod
    def len_even(cls, str_data):
        return not cls.len_odd(str_data)

    @classmethod
    def swap_nibbles_str(cls, hex_str_data, pad_if_required=True):
        """
        Swap nibbles in a hex string.
        len(s) must be even otherwise ValueError will be raised.
        """
        if cls.len_odd(hex_str_data):
            if pad_if_required:
                hex_str_data = hex_str_data + 'F'
            else:
                raise ValueError('Odd Length of data; Padding is recommended.')
        return ''.join([y + x for x, y in zip(*[iter(hex_str_data)] * 2)])

    @classmethod
    def check_if_iter(cls, the_iter, list_as_str, check_for_dict_attibute):
        is_iter = False
        if the_iter is None:
            return is_iter, the_iter
        # Duck Typing
        try:
            """
            Scenarios where obj is iterable by default. e.g.: dict, EnumMeta (Enum Class), str
            """
            if isinstance(the_iter, str):
                # String should not be treated as iterable
                return is_iter, the_iter
            if isinstance(the_iter, list) and list_as_str:
                # Here List should not be treated as iterable
                return is_iter, the_iter
            iter(the_iter)
            is_iter = True
            return is_iter, the_iter
        except TypeError:
            try:
                if not check_for_dict_attibute:
                    return is_iter, the_iter
                """
                Scenarios where obj is not iterable by default, however dict attribute is present. e.g.: Namespace
                """
                if isinstance(the_iter, enum.Enum):
                    # Child of Enum Class should not be treated as iterable
                    return is_iter, the_iter
                the_iter = the_iter.__dict__
                is_iter = True
                return is_iter, the_iter
            except AttributeError:
                return is_iter, the_iter
        return is_iter, the_iter

    @classmethod
    def print(cls, data='', log=None):
        print_or_log = log.info if log else print
        print_or_log(data)

    @classmethod
    def print_input_output(cls, input_data, output_data, log=None, verbose=False, output_remarks=None,
                           input_remark=None):
        if not input_data and not output_data:
            return
        if not isinstance(output_data, list):
            # Cast To List
            output_data = [output_data]
        output_count = len(output_data)
        output_remarks = PhUtil.extend_list(cls.set_if_none(output_remarks, []), expected_length=output_count)
        print_or_log = log.info if log else print
        EXTRA_NEW_LINE = ''
        if verbose:
            input_str = f'Remarks: {input_remark}; input: {input_data}; type: {type(input_data)}, length: {len(str(input_data))}'
            output_str = [f'Remarks: {y}; output: {x}; type: {type(x)}, length: {len(str(x))}' for x, y in
                          zip(output_data, output_remarks)]
        else:
            input_str = f'Remarks: {input_remark}; input: {input_data}';
            output_str = [f'Remarks: {y}; output: {x}' for x, y in zip(output_data, output_remarks)]
            # msg = f'input: {input_data}; output: {output_data}'
        # with Additional new line
        # TODO: Additional new line, can be omitted for scenario where single output if getting listed in normal mode
        msg = '\n'.join(cls.normalise_list([input_str, output_str, '']))
        print_or_log(msg)

    @classmethod
    def print_iter(cls, the_iter, header=None, log=None, list_as_str=None, depth_level=-1, verbose=False,
                   formatting_level=0, sep=None, sep_child=None, check_for_dict_attribute=None):
        """
        This function takes a positional argument called 'the_iter', which is any Python list (of, possibly,
        nested lists). Each data item in the provided list is (recursively) printed to the screen on its own line.

        :param sep:
        :param sep_child:
        :param verbose:
        :param formatting_level:
        :param depth_level:
        :param the_iter:
        :param header:
        :param log:
        :param list_as_str:
        :param check_for_dict_attribute: Force checking of Dict Attribute while checking for iter object. However it may caused "RecursionError" for unhandled types

        For "RecursionError", set this flag as false
        :return:
        """

        def _print_item(_dict_format=False):
            """

            :param _value:
            :return:
            """
            if data_pool:
                print_or_log(sep.join(data_pool))
            if PhConstants.SEPERATOR_TWO_LINES in sep and (
                    not nested and (the_iter_length > 1 or header)) and not list_as_str:
                print_or_log(PhConstants.STR_EMPTY)

        def _collect_item(_value=None, _key=None, _dict_format=False, _empty_data=False):
            """

            :param _value:
            :param _key:
            :param _dict_format:
            :return:
            """
            if _empty_data is True:
                data_pool.append('')
                return
            _data = f'{str(key)}: {value}' if _dict_format else _value
            if verbose:
                data_pool.append(f'{spaces}{_data}; type: {type(_value)}, length: {len(str(_value))}')
            else:
                data_pool.append(f'{spaces}{_data}')
            return

        # TODO: Need to fix support of formatting_level

        print_or_log = log.info if log else print
        data_pool = []
        formatting_level = cls.set_if_none(formatting_level, 0)
        # spaces = PhConstants.STR_TAB * formatting_level
        spaces = PhConstants.STR_TAB * 0
        list_as_str = cls.set_if_none(list_as_str, False)
        check_for_dict_attribute = cls.set_if_none(check_for_dict_attribute, True)
        sep = cls.set_if_none(sep, PhConstants.SEPERATOR_TWO_LINES)
        sep_child = cls.set_if_none(sep_child, PhConstants.SEPERATOR_MULTI_OBJ)
        nested = PhConstants.NO
        is_iter, the_iter = cls.check_if_iter(
            the_iter=the_iter,
            list_as_str=list_as_str,
            check_for_dict_attibute=check_for_dict_attribute
        )
        the_iter_length = len(the_iter) if is_iter else 0
        if header:
            header = f'{header}:'
        # NonIterable is an Enum Object
        if isinstance(the_iter, enum.Enum):
            # enum_class_name = type(the_iter).__name__
            enum_class_name = the_iter.__class__.__name__
            pair_data = cls.get_key_value_pair(the_iter.name, the_iter.value, user_friendly_key=False)
            _collect_item(_value=' '.join(filter(None, [header, enum_class_name, pair_data])))
            _print_item()
            return
        if not is_iter:
            _collect_item(_value=' '.join(filter(None, [header, str(the_iter)])))
            _print_item()
            return
        if header:
            print_or_log(header)
        # Iterable is a Dictionary, OrderedDictionary etc.
        if isinstance(the_iter, dict):
            for key in the_iter.keys():
                value = the_iter[key]
                if depth_level == -1 and cls.check_if_iter(
                        the_iter=value,
                        list_as_str=list_as_str,
                        check_for_dict_attibute=check_for_dict_attribute
                )[0]:
                    nested = PhConstants.YES
                    cls.print_iter(the_iter=value, header=str(key), log=log, list_as_str=list_as_str,
                                   formatting_level=formatting_level + 1, sep=sep,
                                   check_for_dict_attribute=check_for_dict_attribute)
                else:
                    _collect_item(_key=key, _value=value, _dict_format=True)
            _print_item(_dict_format=True)
            return
        # Other iterable Items
        for each_item in the_iter:
            # Check if sub-objects are Iterable
            if depth_level == -1 and cls.check_if_iter(
                    the_iter=each_item,
                    list_as_str=list_as_str,
                    check_for_dict_attibute=check_for_dict_attribute
            )[0]:
                nested = PhConstants.YES
                cls.print_iter(the_iter=each_item, log=log, formatting_level=formatting_level + 1, sep=sep_child,
                               check_for_dict_attribute=check_for_dict_attribute)
                continue
            _collect_item(_value=each_item)
        _print_item()

    @classmethod
    def print_separator(cls, character='-', count=80, main_text='', log=None, get_only=False, multi_line=False):
        """

        :param multi_line:
        :param character:
        :param count:
        :param main_text:
        :param log:
        :param get_only:
        :return:
        """
        print_or_log = log.info if log else print
        if main_text is None:
            main_text = ''
        text_len = len(main_text)
        if count - 4 <= text_len:
            count = 2  # Minimum Needed
        else:
            count = count - text_len
        count = int(count / 2)
        sep_initial = count * character
        sep_end = count * character
        sep_mid = ' ' if main_text else ''
        msg = f'{sep_initial}{sep_mid}{main_text}{sep_mid}{sep_end}'
        if multi_line:
            msg = f'\n\n\n\n{msg}'
        if get_only:
            return msg
        print_or_log(msg)

    @classmethod
    def print_cmt(cls, main_text='', character='-', count=40, log=None, quite_mode=False):
        if not quite_mode:
            cls.print_separator(character=character, count=count, main_text=main_text, log=log)

    @classmethod
    def print_done(cls, main_text='All Done.', log=None):
        cls.print_separator(log=log)
        cls.print_separator(character=' ', count=35, main_text=main_text, log=log)
        cls.print_separator(log=log)

    @classmethod
    def print_work_in_progress(cls, main_text='Work In Progress', append_function_name=True, log=None):
        cls.print_separator(log=log)
        if append_function_name:
            main_text = f'{cls.get_current_func_name(parent_level=2)}(): {main_text}'
        cls.print_separator(character='+', count=50, main_text=main_text, log=log)
        cls.print_separator(log=log)

    @classmethod
    def print_error(cls, str_heading, log=None):
        cls.print_separator(log=log)
        cls.print_separator(character='+', main_text=f'Error Occurred: {str_heading}', log=log)
        cls.print_separator(log=log)

    @classmethod
    def print_modules(cls, filter_string=None, depth_level=0):
        data = sys.modules
        print(f'Total Modules Count: {len(data)}')
        if filter_string:
            filtered_data = {k: v for k, v in data.items() if filter_string in k}
            print(f'Filtered Modules Count: {len(filtered_data)}')
            cls.print_iter(filtered_data, depth_level=depth_level)
        else:
            cls.print_iter(data, depth_level=depth_level)

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
    def get_tool_name_w_version(cls, tool_name=None, tool_version=None, dic_format=False, fetch_tool_version=None):
        if fetch_tool_version:
            tool_version = cls.get_module_version(tool_name)
        str_format_keyword = ' version is '
        version_keyword = 'v'
        tool_name = 'Python' if tool_name is None else tool_name
        tool_version = sys.version if tool_name == 'Python' else (
            str(tool_version) if tool_version is not None else None)
        if tool_version:
            version_keyword_needed = False if tool_version.strip().lower().startswith(version_keyword) else True
            tool_version = f'{version_keyword}{tool_version}' if version_keyword_needed else tool_version
        if dic_format:
            return {tool_name: tool_version}
        return str_format_keyword.join([tool_name, cls.set_if_none(tool_version)])

    @classmethod
    def print_version(cls, tool_name=None, tool_version=None, fetch_tool_version=False, log=None, parameters_pool=None,
                      no_additional_info=False, with_python=True, with_ph_lib=True,
                      with_user_info=True, with_time_stamp=True, with_git_summary=True,
                      with_ip=False, with_git_detailed_info=False, get_only=False, dic_format=False):
        """

        :param tool_name:
        :param tool_version:
        :param fetch_tool_version:
        :param log:
        :param parameters_pool: List of Dicts containing parameters
        :param no_additional_info:
        :param with_python:
        :param with_ph_lib:
        :param with_user_info:
        :param with_time_stamp:
        :param with_git_summary:
        :param with_ip:
        :param with_git_detailed_info:
        :param get_only:
        :param dic_format:
        :return:
        """

        def __print_version():
            nonlocal with_ph_lib, no_additional_info
            print_or_log = log.info if log else print
            sep_needed = False if tool_name in [None, PhConfigConst.TOOL_NAME] else True
            if dic_format:
                no_additional_info = True
                sep_needed = False
            if tool_name == PhConfigConst.TOOL_NAME:
                # Avoid Redundant Info (when explicitly asked)
                with_ph_lib = False
            if sep_needed:
                cls.print_separator(log=log)
            if not no_additional_info:
                if with_python:
                    cls.print_version(log=log, no_additional_info=True)
                    print(f'Python executable Path is {cls.path_python_folder}')
                    cls.print_separator(log=log)
                if with_user_info:
                    print(f'User Name is {cls.get_user_details_display_name()}')
                    print(f'User Account is {cls.get_user_details_account_name()}')
                    cls.print_separator(log=log)
                if with_time_stamp:
                    print(f'Time Stamp is {cls.get_time_stamp(files_format=False)}')
                    cls.print_separator(log=log)
                if with_ip:
                    print(f'IPV4 is {cls.get_ip(ipv4=True)}')
                    print(f'IPV6 is {cls.get_ip(ipv4=False)}')
                    cls.print_separator(log=log)
                if with_git_summary:
                    print(f'Git Summary is {PhConfigConst.TOOL_GIT_SUMMARY}')
                    cls.print_separator(log=log)
                if with_git_detailed_info:
                    cls.print_iter(PhGit.get_git_info_detailed(), header='Git Details are')
                    cls.print_separator(log=log)
                if with_ph_lib:
                    cls.print_version(tool_name=PhConfigConst.TOOL_NAME, tool_version=PhConfigConst.TOOL_VERSION,
                                      log=log, no_additional_info=True)
                    cls.print_separator(log=log)
            name_w_version = cls.get_tool_name_w_version(tool_name=tool_name, tool_version=tool_version,
                                                         fetch_tool_version=fetch_tool_version, dic_format=dic_format)
            if get_only:
                return name_w_version
            print_or_log(name_w_version)
            if sep_needed:
                cls.print_separator(log=log)
            return name_w_version

        if parameters_pool is None:
            # Single Mode
            return __print_version()
        # Bulk Mode
        output = []
        for index, parameters_dict in enumerate(parameters_pool):
            # Avoid Redundent info
            parameters_dict.update({'no_additional_info': no_additional_info if index == 0 else True})
            if get_only:
                parameters_dict.update({'get_only': get_only})
            if dic_format:
                parameters_dict.update({'dic_format': dic_format})
            output.append(cls.print_version(**parameters_dict))
        return output

    @classmethod
    def print_heading(cls, str_heading=None, heading_level=1, char=None, max_length=None, log=None, parent_level=None):
        """

        :param str_heading:
        :param heading_level:
        :param char:
        :param max_length:
        :param log:
        :return:
        """
        print_or_log = log.info if log else print
        char_selector = {
            1: '-',
            2: '*',
            3: '+',
        }
        if char is None:
            char = char_selector.get(heading_level, '-')
        if parent_level is None:
            parent_level = 2
        if str_heading is None:
            str_heading = cls.get_current_func_name(parent_level=parent_level)
        if isinstance(str_heading, list):
            str_heading = PhConstants.SEPERATOR_MULTI_OBJ.join(filter(None, str_heading))
        if max_length is None:
            max_length = PhConstants.HEADING_LENGTH_MAX
        data_max_length = max_length - PhConstants.HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_SYMBOL - PhConstants.HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_WHITE_SPACES
        str_heading = str_heading[:data_max_length].replace('\n', ' ')
        current_len = len(str_heading)
        remaining_count = max_length - current_len - PhConstants.HEADING_LENGTH_RESERVE_STARTING_AND_ENDING_WHITE_SPACES
        print_or_log(
            ''.join([char * math.ceil(remaining_count / 2), ' ', str_heading, ' ', char * int(remaining_count / 2)]))

    @classmethod
    def print_data(cls, cmt_to_print, str_hex_data='', log=None):
        return cls.analyse_data(str_hex_data=str_hex_data, cmt_to_print=cmt_to_print, print_also=True, log=log)

    @classmethod
    def analyse_data(cls, str_hex_data, cmt_to_print='', print_also=False, log=None):
        """

        :param str_hex_data:
        :param cmt_to_print:
        :param print_also:
        :param log:
        :return:
        """
        print_or_log = log.info if log else print
        analysed_str = ''
        if str_hex_data:
            str_hex_data = str(str_hex_data)  # Needed to convert any type
            if cls.len_odd(str_hex_data):
                analysed_str = 'Odd Length'
            analysed_str = ', '.join(filter(None, [analysed_str,
                                                   'Length: ' + str(len(str_hex_data)) + ' digits(s) / ' + cls.len_hex(
                                                       str_hex_data, output_in_str_format=True) + ' byte(s)',
                                                   'Data: ' + str_hex_data]))
        if cmt_to_print:
            if str_hex_data:
                cmt_to_print = '\n' + cmt_to_print + '\t'
            analysed_str = ':'.join(filter(None, [cmt_to_print, analysed_str]))
        if print_also:
            print_or_log(analysed_str)
        return analysed_str

    @classmethod
    def is_empty(cls, value):
        if value is None:
            return True
        if isinstance(value, bool):
            return False
        # TODO: Need to find a proper way to handle all int like scenarios (float etc)
        if isinstance(value, int):
            return False
        if len(value) == 0:
            return True
        return False

    @classmethod
    def is_not_empty(cls, value):
        return not cls.is_empty(value)

    @classmethod
    def is_none(cls, value):
        return True if value is None else False

    @classmethod
    def is_not_none(cls, value):
        return not cls.is_none(value)

    @classmethod
    def is_empty_or_comment_string(cls, str_data, comments_pool=None):
        """
        Check if line is a comment
        :param str_data:
        :param comments_pool:
        :return:
        """
        comments_pool = cls.set_if_empty(comments_pool, new_value=['#', '*', ';', '-', '/*'])
        if cls.is_empty_string(str_data):
            return True
        str_data = str_data.strip()
        for comment_char in comments_pool:
            if str_data.startswith(comment_char):
                return True
        return False

    @classmethod
    def is_empty_string(cls, str_data):
        """

        :param str_data:
        :return:
        """
        return True if str_data is None or str_data.strip() == '' else False

    @classmethod
    def is_not_empty_string(cls, str_data):
        """

        :param str_data:
        :return:
        """
        return not cls.is_empty_string(str_data)

    @classmethod
    def set_type_if_different(cls, value=None, new_type=None):
        return new_type(value) if new_type and not isinstance(value, new_type) else value

    @classmethod
    def set_if_none(cls, current_value, new_value='', new_type=None):
        value = new_value if cls.is_none(current_value) else current_value
        return cls.set_type_if_different(value, new_type=new_type)

    @classmethod
    def set_if_empty(cls, current_value, new_value='', new_type=None):
        value = new_value if cls.is_empty(current_value) else current_value
        return cls.set_type_if_different(value, new_type=new_type)

    @classmethod
    def get_file_name_and_extn(cls, file_path, name_with_out_extn=None, only_extn=None, extn_with_out_dot=None,
                               only_path=None, ext_available=None, path_with_out_extn=None, only_folder_name=None):
        """

        :param file_path:
        :param name_with_out_extn:
        :param only_extn:
        :param extn_with_out_dot:
        :param only_path:
        :param ext_available:
        :param path_with_out_extn:
        :param only_folder_name:
        :return:
        """
        name_with_out_extn = cls.set_if_none(name_with_out_extn, False)
        only_extn = cls.set_if_none(only_extn, False)
        extn_with_out_dot = cls.set_if_none(extn_with_out_dot, False)
        only_path = cls.set_if_none(only_path, False)
        ext_available = cls.set_if_none(ext_available, True)
        path_with_out_extn = cls.set_if_none(path_with_out_extn, False)
        only_folder_name = cls.set_if_none(only_folder_name, False)

        if not file_path:
            return ''
        sep_char = os.sep
        if sep_char == '\\':
            # needed to avoid escape sequence chars in file path
            file_path = re.sub(r'\\{1,}', '/', file_path)
            sep_char = '/'
        split_data = list(filter(None, file_path.split(sep_char)))
        file_name = split_data[-1]
        folder_name = split_data[-2] if len(split_data) > 1 else ''
        path = file_path.replace(file_name, '')
        if only_path:
            path = re.sub(r'/{1,}$', '/', path)
            return path
        if only_folder_name:
            return folder_name
        if ext_available:
            extn = os.path.splitext(file_path)[1]
            if not extn:
                temp = file_path.split(sep_char)[-1]
                if len(temp) >= 1 and temp[0] == '.':
                    extn = temp
        else:
            extn = ''
        if only_extn:
            if extn_with_out_dot:
                return extn.replace('.', '')
            return extn
        file_name_wo_extn = file_name.replace(extn, '')
        # Name is needed
        if name_with_out_extn:
            return file_name_wo_extn
        # Full Name is needed
        if path_with_out_extn:
            return sep_char.join([path, file_name_wo_extn])
        return file_name

    @classmethod
    def backup_file_name(cls, str_file_path, default_file_ext=PhFileExtensions.BKP, default_key_word='backup',
                         file_path_is_dir=None):
        return cls.append_in_file_name(str_file_path,
                                       str_append=[default_key_word, cls.get_time_stamp(files_format=True)],
                                       file_path_is_dir=file_path_is_dir, treat_folder_as_file=False,
                                       default_ext=default_file_ext)

    @classmethod
    def rreplace(cls, main_str, old, new, max_split=1):
        return new.join(main_str.rsplit(old, max_split))

    @classmethod
    def count(cls, main_str, sub_string, start=None, end=None):
        if cls.is_empty_string(main_str) or cls.is_empty_string(sub_string):
            return 0
        main_str = main_str.lower()
        sub_string = sub_string.lower()
        return main_str.count(sub_string, start, end)

    @classmethod
    def append_in_file_name(cls, str_file_path, str_append=None, sep=None, new_name=None, new_ext=None,
                            file_path_is_dir=None, ext_available_in_file_name=None, append_post=None,
                            treat_folder_as_file=False, default_ext=None):
        """

        :param default_ext:
        :param treat_folder_as_file:
        :param str_file_path:
        :param str_append:
        :param sep:
        :param new_name:
        :param new_ext:
        :param file_path_is_dir:
        :param ext_available_in_file_name:
        :param append_post:
        :return:
        """
        # Set Default Values, if not available
        str_file_path = cls.set_if_none(str_file_path)
        str_append = cls.set_if_none(str_append)
        sep = cls.set_if_none(sep, new_value='_')
        new_ext = cls.set_if_none(new_ext)
        default_ext = cls.set_if_none(default_ext)
        file_path_is_dir = cls.set_if_none(file_path_is_dir, False)
        ext_available_in_file_name = cls.set_if_none(ext_available_in_file_name, True)
        append_post = cls.set_if_none(append_post, True)

        if isinstance(str_file_path, TextIOWrapper):
            str_file_path = str_file_path.name
        if file_path_is_dir or str_file_path.endswith(os.sep):
            str_ext = ''
            ext_available_in_file_name = False
            if treat_folder_as_file:
                # consider folder name as file name
                str_file_name = cls.get_file_name_and_extn(str_file_path)
                str_path = cls.get_file_name_and_extn(str_file_path, only_path=True)
            else:
                # consider folder name as folder name
                str_file_name = ''
                str_path = str_file_path
                if not str_file_path.endswith(os.sep):
                    str_path += os.sep
        else:
            str_path = cls.get_file_name_and_extn(str_file_path, only_path=True)
            str_ext = cls.get_file_name_and_extn(str_file_path, only_extn=True,
                                                 ext_available=ext_available_in_file_name)
            str_file_name = cls.get_file_name_and_extn(str_file_path, name_with_out_extn=True,
                                                       ext_available=ext_available_in_file_name)
        if isinstance(str_append, list):
            str_append = sep.join(filter(None, str_append))
        if isinstance(new_name, list):
            new_name = sep.join(filter(None, new_name))
        if not str_file_name:
            sep = ''
        if str_append:
            str_append = (sep + str_append) if append_post else (str_append + sep)
        else:
            str_append = ''
        #
        if not str_ext and not new_ext and default_ext:
            new_ext = default_ext
        str_new_ext = (str_ext if not new_ext else new_ext)
        str_temp_name = new_name if new_name is not None else str_file_name
        str_new_file_name = (str_temp_name + str_append) if append_post else (str_append + str_temp_name)
        # file name is present
        str_file_path = cls.rreplace(str_file_path, str_file_name, str_new_file_name, 1) if str_file_name else (
                str_path + str_new_file_name + str_ext)
        # extension is present
        str_file_path = cls.rreplace(str_file_path, str_ext, str_new_ext, 1) if str_ext else (
                str_file_path + str_new_ext)
        return str_file_path

    @classmethod
    def get_ip(cls, ipv4=True):
        def __get_ip_from_service(ip_service):
            ext_ip = ''
            try:
                ext_ip = requests.get(url=ip_service, timeout=1).text.strip()
                # ext_ip = urllib.request.urlopen(ip_service, timeout=1).read().decode('utf8').strip()
                # print(f'{ext_ip} as per {ip_service}')
            except Exception as e:
                # print(f'Error Fetching IP from {ip_service}')
                pass
            return ext_ip

        def __get_ip_from_pool(ip_services_pool):
            for ip_service in ip_services_pool:
                ext_ip = __get_ip_from_service(ip_service)
                if ext_ip:
                    return ext_ip

        if ipv4 is True:
            return __get_ip_from_pool(PhConstants.PUBLIC_IP_SERVICES_IPV4_POOL)
        if ipv4 is False:
            return __get_ip_from_pool(PhConstants.PUBLIC_IP_SERVICES_IPV6_POOL)
        return __get_ip_from_pool(PhConstants.PUBLIC_IP_SERVICES_POOL)

    @classmethod
    def get_time_stamp(cls, files_format=True, date_only=False, default_format=False):
        if files_format:
            date_format = '%Y%m%d'
            time_format = date_format if date_only else f'{date_format}_%H%M%S%f'
            # Unique time must be generated
            time.sleep(0.001)
        else:
            # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            # Date & Time: Thursday, Apr 04 2023, 18:44:44:356307, IST (GMT+0530)
            date_format = '%A, %b %d %Y'
            time_format = date_format if date_only else f'{date_format}, %H:%M:%S:%f, %Z (GMT%z)'
        # current date and time
        # now = datetime.now()  # current date and time
        # now = datetime.now().astimezone() # needed for %z & %Z
        now = datetime.now(tzlocal.get_localzone())
        if default_format:
            return now
        date_time = now.strftime(time_format)
        if files_format:
            return str(date_time)
        return date_time

    @classmethod
    def format_time(cls, time_value, time_interval=False):
        time_format = '%H:%M:%S'
        if time_interval:
            time_value = time.gmtime(time_value)
        return time.strftime(time_format, time_value)

    @classmethod
    def get_user_friendly_name(cls, python_variable_name):
        temp_data = re.sub(r'[_]', repl=' ', string=python_variable_name)
        return temp_data.title()

    @classmethod
    def get_python_friendly_name(cls, user_variable_name, all_lower=True, case_sensitive=True):
        if isinstance(user_variable_name, str):
            temp_data = user_variable_name
            temp_data = temp_data.replace(PhConstants.DEFAULT_TRIM_STRING, '_')
            temp_data = re.sub(r'[^a-zA-Z0-9_.]', repl='_', string=temp_data)
            temp_data = re.sub(r'(_)\1+', repl=r'\1', string=temp_data)
            temp_data = temp_data.strip('_')
            if case_sensitive:
                return temp_data.lower() if all_lower else temp_data.title()
            else:
                return temp_data
        return user_variable_name

    traverse_modes = ['ImmediateFilesOnly', 'ImmediateFoldersOnly', 'ImmediateFolderAndFiles',
                      'RecursiveFilesOnly', 'RecursiveFoldersOnly', 'RecursiveAll', 'Regex']

    @classmethod
    def traverse_it(cls, top=path_current_folder, traverse_mode='Regex', include_files=None, include_dirs=None,
                    excludes=None, detail_info=False, print_also=False):
        """
        Usage: python <programName.py> <folderName>

        glob: https://en.wikipedia.org/wiki/Glob_(programming)
        :param top:
        :param traverse_mode:
        :param include_files: applicable only when traverseMode is 'Regex'
            Sample: ['*.mp3', '*.mp4']
        :param include_dirs:
        :param excludes: for dirs and files, applicable only when traverseMode is 'Regex'
            Sample1: ['/home/paulo-freitas/Documents']
            Sample2: ['E:\\Entertainment\\Songs_Mp3\\19's', 'E:\\Entertainment\\Songs_Mp3\\2000-2009']
        :param detail_info:
        :param print_also:
        :return:
        """
        if not include_files:
            include_files = []
        if isinstance(include_files, str):
            include_files = [include_files]
        if not include_dirs:
            include_dirs = []
        if isinstance(include_dirs, str):
            include_dirs = [include_dirs]
        if not excludes:
            excludes = []
        if isinstance(excludes, str):
            excludes = [excludes]
        output_list = []
        output_list_temp = []

        print(f'traverse_mode: {traverse_mode}')
        print(f'top: {top}')
        print(f'include_files: {include_files}')
        print(f'include_dirs: {include_dirs}')
        print(f'excludes: {excludes}')

        if traverse_mode == 'Regex':
            # transform glob patterns to regular expressions
            include_files = r'|'.join([fnmatch.translate(x) for x in include_files])
            include_dirs = r'|'.join([fnmatch.translate(x) for x in include_dirs])
            excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'
            # print('include_files: ', include_files)
            # print('include_dirs: ', include_dirs)
            # print('excludes: ', excludes)

        for dirpath, dirnames, filenames in os.walk(top):
            if traverse_mode == 'ImmediateFilesOnly':
                for filename in filenames:
                    if dirpath == top:
                        filepath = os.path.join(dirpath, filename)
                        output_list.append(filepath)

            if traverse_mode == 'ImmediateFoldersOnly':
                for dirname in dirnames:
                    if dirpath == top:
                        filepath = os.path.join(dirpath, dirname)
                        output_list.append(filepath)

            if traverse_mode == 'ImmediateFolderAndFiles':
                output_list_temp = cls.traverse_it(top, traverse_mode='ImmediateFoldersOnly')
                output_list = output_list_temp
                output_list_temp = cls.traverse_it(top, traverse_mode='ImmediateFilesOnly')
                output_list = output_list + output_list_temp

            if traverse_mode == 'RecursiveFilesOnly':
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        if detail_info:
                            filesize = cls.str_insert_char_repeatedly(os.stat(filepath).st_size, reverse=True)
                            fileext = cls.get_file_name_and_extn(filename, only_extn=True, extn_with_out_dot=True)
                            pattern = [filename, filepath, filesize, fileext]
                            output_list.append('\t'.join(pattern))
                        else:
                            output_list.append(filepath)
                    except:
                        pass

            if traverse_mode == 'RecursiveFoldersOnly':
                for dirname in dirnames:
                    filepath = os.path.join(dirpath, dirname)
                    output_list.append(filepath)

            if traverse_mode == 'RecursiveAll':
                output_list_temp = cls.traverse_it(top, traverse_mode='RecursiveFoldersOnly')
                output_list = output_list_temp
                output_list_temp = cls.traverse_it(top, traverse_mode='RecursiveFilesOnly')
                output_list = output_list + output_list_temp

            if traverse_mode == 'Regex':
                # Ref: https://stackoverflow.com/a/5141829

                # exclude dirs
                dirnames[:] = [os.path.join(dirpath, d) for d in dirnames]
                dirnames[:] = [d for d in dirnames if not re.match(excludes, d)]
                # include dirs
                dirnames[:] = [d for d in dirnames if re.match(include_dirs, d)]
                # exclude/include filenames
                filenames = [os.path.join(dirpath, f) for f in filenames]
                filenames = [f for f in filenames if not re.match(excludes, f, re.IGNORECASE)]
                filenames = [f for f in filenames if re.match(include_files, f, re.IGNORECASE)]
                output_list = output_list + filenames
        if print_also:
            cls.print(f'Count is: {len(output_list)}')
            cls.print_iter(output_list)
        return output_list

    @classmethod
    def get_random_string_for_variable(cls, var_name):
        """

        :param var_name:
        :return:
        """
        var_name = cls.get_synonym_of_variable_name(var_name)
        if var_name in PhConstants.POOL_4_DIGITS_LENGTH:
            size = 4
            str_type = PhConstants.STR_TYPE_NUMERIC
        elif var_name in PhConstants.POOL_8_DIGITS_LENGTH:
            size = 8
            str_type = PhConstants.STR_TYPE_NUMERIC
        elif var_name in PhConstants.POOL_16_BYTES_LENGTH:
            size = 16
            str_type = PhConstants.STR_TYPE_HEX_UPPER_CASE
        else:
            return ''
        return cls.get_random_string(size, str_type)

    @classmethod
    def get_random_string(cls, target_str_length=8, str_type=PhConstants.STR_TYPE_HEX_UPPER_CASE):
        """

        :param target_str_length:
        :param str_type:
        :return:
        """
        if str_type == PhConstants.STR_TYPE_HEX_LOWER_CASE:
            return secrets.token_hex(target_str_length)
        letters_mapping = {
            PhConstants.STR_TYPE_NUMERIC_BIN: '01',
            PhConstants.STR_TYPE_NUMERIC_OCT: string.octdigits,
            PhConstants.STR_TYPE_NUMERIC: string.digits,
            #
            PhConstants.STR_TYPE_HEX_LOWER_CASE: string.digits + 'abcdef',
            PhConstants.STR_TYPE_HEX_UPPER_CASE: string.digits + 'ABCDEF',
            PhConstants.STR_TYPE_HEX_RANDOM_CASE: string.hexdigits,
            #
            PhConstants.STR_TYPE_ASCII_LOWER_CASE: string.ascii_lowercase,
            PhConstants.STR_TYPE_ASCII_UPPER_CASE: string.ascii_uppercase,
            PhConstants.STR_TYPE_ASCII_RANDOM_CASE: string.ascii_letters,
            #
            PhConstants.STR_TYPE_ALPHA_NUMERIC_LOWER_CASE: string.ascii_lowercase + string.digits,
            PhConstants.STR_TYPE_ALPHA_NUMERIC_UPPER_CASE: string.ascii_uppercase + string.digits,
            PhConstants.STR_TYPE_ALPHA_NUMERIC_RANDOM_CASE: string.ascii_letters + string.digits,
            #
            PhConstants.STR_TYPE_PASSWORD_LOWER_CASE: string.ascii_lowercase + string.digits + string.punctuation,
            PhConstants.STR_TYPE_PASSWORD_UPPER_CASE: string.ascii_uppercase + string.digits + string.punctuation,
            PhConstants.STR_TYPE_PASSWORD_RANDOM_CASE: string.ascii_letters + string.digits + string.punctuation,
            #
        }
        return ''.join(
            random.choice(letters_mapping.get(str_type, letters_mapping.get(PhConstants.STR_TYPE_HEX_UPPER_CASE))) for _
            in range(target_str_length))

    @classmethod
    def get_random_item_from_iter(cls, the_iter, skip_generalise_item=True):
        def __get_random_from_iter(the_iter):
            if isinstance(the_iter, dict):
                if not the_iter:  # Empty Dict
                    return None
                return random.choice(list(the_iter.keys()))
            if isinstance(the_iter, list):
                if len(the_iter) == 0:  # Empty List
                    return None
                return random.choice(the_iter)
            return random.choice(list(the_iter))

        def __is_generalise_item(item):
            return item in [PhConstants.STR_SELECT_OPTION, PhConstants.STR_OTHER_OPTION]

        res = __get_random_from_iter(the_iter)
        if not (skip_generalise_item and __is_generalise_item(res)):
            return res
        # need to skip a couple of items
        max_attempt = 3
        while max_attempt > 0:
            res = __get_random_from_iter(the_iter)
            if not __is_generalise_item(res):
                break
        return res

    @classmethod
    def generate_transaction_id(cls):
        return cls.get_random_string(target_str_length=12, str_type=PhConstants.STR_TYPE_ALPHA_NUMERIC_LOWER_CASE)

    @classmethod
    def get_synonym_of_variable_name(cls, var_name, var_type=PhConstants.VAR_TYPE_OUT):
        """

        :param var_name:
        :param var_type:
        :return:
        """
        default_offset = (1 if var_type == PhConstants.VAR_TYPE_PROFILE else 0)
        pools = [
            PhConstants.VAR_POOL_ICCID, PhConstants.VAR_POOL_IMSI, PhConstants.VAR_POOL_IMSI2, PhConstants.VAR_POOL_KI,
            #
            PhConstants.VAR_POOL_PIN1, PhConstants.VAR_POOL_PIN2, PhConstants.VAR_POOL_2_PIN1,
            PhConstants.VAR_POOL_3_PIN1,
            #
            PhConstants.VAR_POOL_PUK1, PhConstants.VAR_POOL_PUK2, PhConstants.VAR_POOL_2_PUK1,
            PhConstants.VAR_POOL_3_PUK1,
            #
            PhConstants.VAR_POOL_ADM1, PhConstants.VAR_POOL_ADM2, PhConstants.VAR_POOL_ADM3,
            #
            PhConstants.VAR_POOL_ACC,
            #
            PhConstants.VAR_POOL_KIC1, PhConstants.VAR_POOL_KID1, PhConstants.VAR_POOL_KIK1,
            #
            PhConstants.VAR_POOL_KIC2, PhConstants.VAR_POOL_KID2, PhConstants.VAR_POOL_KIK2,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_01, PhConstants.VAR_POOL_MNO_SD_KID_01, PhConstants.VAR_POOL_MNO_SD_KIK_01,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_02, PhConstants.VAR_POOL_MNO_SD_KID_02, PhConstants.VAR_POOL_MNO_SD_KIK_02,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_03, PhConstants.VAR_POOL_MNO_SD_KID_03, PhConstants.VAR_POOL_MNO_SD_KIK_03,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_04, PhConstants.VAR_POOL_MNO_SD_KID_04, PhConstants.VAR_POOL_MNO_SD_KIK_04,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_05, PhConstants.VAR_POOL_MNO_SD_KID_05, PhConstants.VAR_POOL_MNO_SD_KIK_05,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_06, PhConstants.VAR_POOL_MNO_SD_KID_06, PhConstants.VAR_POOL_MNO_SD_KIK_06,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_07, PhConstants.VAR_POOL_MNO_SD_KID_07, PhConstants.VAR_POOL_MNO_SD_KIK_07,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_08, PhConstants.VAR_POOL_MNO_SD_KID_08, PhConstants.VAR_POOL_MNO_SD_KIK_08,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_09, PhConstants.VAR_POOL_MNO_SD_KID_09, PhConstants.VAR_POOL_MNO_SD_KIK_09,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0A, PhConstants.VAR_POOL_MNO_SD_KID_0A, PhConstants.VAR_POOL_MNO_SD_KIK_0A,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0B, PhConstants.VAR_POOL_MNO_SD_KID_0B, PhConstants.VAR_POOL_MNO_SD_KIK_0B,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0C, PhConstants.VAR_POOL_MNO_SD_KID_0C, PhConstants.VAR_POOL_MNO_SD_KIK_0C,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0D, PhConstants.VAR_POOL_MNO_SD_KID_0D, PhConstants.VAR_POOL_MNO_SD_KIK_0D,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0E, PhConstants.VAR_POOL_MNO_SD_KID_0E, PhConstants.VAR_POOL_MNO_SD_KIK_0E,
            #
            PhConstants.VAR_POOL_MNO_SD_KIC_0F, PhConstants.VAR_POOL_MNO_SD_KID_0F, PhConstants.VAR_POOL_MNO_SD_KIK_0F,
            #
        ]
        for pool in pools:
            if var_name in pool:
                return pool[default_offset]
        return var_name

    @classmethod
    def generate_range_str(cls, start_point, end_point, func=None):
        range_data = []
        start_counter = int(start_point[len(start_point) - PhConstants.MAX_SUPPORTED_DIGIT_IN_INT:])
        end_counter = int(end_point[len(end_point) - PhConstants.MAX_SUPPORTED_DIGIT_IN_INT:])
        start_point = start_point[:-PhConstants.MAX_SUPPORTED_DIGIT_IN_INT]
        for count in range(start_counter, end_counter + 1):
            data = start_point + str(count).zfill(PhConstants.MAX_SUPPORTED_DIGIT_IN_INT)
            if func:
                data = func(data)
            range_data.append(data)
        return range_data

    @classmethod
    def make_dirs(cls, dir_path=None, file_path=None, absolute_path_needed=False, quite_mode=True):
        return cls.__handle_dirs(dir_path=dir_path, file_path=file_path, absolute_path_needed=absolute_path_needed,
                                 operation_type=PhConstants.DIR_CREATION, quite_mode=quite_mode)

    @classmethod
    def remove_dirs(cls, dir_path=None, file_path=None, absolute_path_needed=False, quite_mode=True):
        return cls.__handle_dirs(dir_path=dir_path, file_path=file_path, absolute_path_needed=absolute_path_needed,
                                 operation_type=PhConstants.DIR_DELETION, quite_mode=quite_mode)

    @classmethod
    def find_offset_of_section(cls, data, char_to_find, corresponding_char_to_find):
        """
        Considering Ideal Scenario: Any target char is not present as a comment
        Data Pattern is correct,target characters are available in pairs

        :param data:
        :param char_to_find:
        :param corresponding_char_to_find:
        :return:
        """
        slack = []
        start_char_list = [m.start() for m in re.finditer(char_to_find, data)]
        end_char_list = [m.start() for m in re.finditer(corresponding_char_to_find, data)]
        start_char_list_len = len(start_char_list)
        end_char_list_len = len(end_char_list)
        # print('start_char_list', start_char_list)
        # print('end_char_list', end_char_list)
        # print('start_char_list_len', start_char_list_len)
        # print('end_char_list_len', end_char_list_len)
        index_start_char = 0
        index_end_char = 0
        count = 0
        end_char = len(data)  # assignment is needed for the wrong case when target chars are not present
        while count < start_char_list_len + end_char_list_len:
            count += 1
            start_char = int(start_char_list[index_start_char]) if index_start_char < start_char_list_len else -1
            end_char = int(end_char_list[index_end_char]) if index_end_char < end_char_list_len else -1
            if start_char < end_char and start_char != -1:
                # print('pushed', start_char)
                index_start_char += 1
                slack.append(start_char)
            else:
                # print('poped', end_char)
                index_end_char += 1
                slack.pop()
            if len(slack) == 0:
                # print(corresponding_char_to_find, end_char)
                break
        return end_char

    @classmethod
    def dec_to_hex(cls, dec_num, digit_required=None, even_digits=True, signed_byte_handling=True):
        """

        :param dec_num:
        :param digit_required:
        :param even_digits:
        :param signed_byte_handling: Byte in Java is represented by signed int in range (-128, 127), Byte Python is represented by unsigned int in range(0, 255).
        :return:
        """
        # return hex(dec_num).split('x')[-1].upper()
        # return '0x{:02x}'.format(dec_num)
        # return binascii.hexlify(str(dec_num))
        if isinstance(dec_num, list):
            res = [cls.dec_to_hex(dec_num=x, digit_required=digit_required, even_digits=even_digits,
                                  signed_byte_handling=signed_byte_handling) for x in dec_num]
            return ''.join(res)
        if dec_num < 0 and signed_byte_handling:
            dec_num = dec_num + 256
        if digit_required is None:
            digit_required = 0
        temp = format(dec_num, 'X')
        if even_digits:
            temp = temp.rjust(len(temp) + (1 if cls.len_odd(temp) else 0), '0')
        return temp.rjust(digit_required, '0')

    @classmethod
    def hex_str_to_dec(cls, hex_str, signed_byte_handling=False):
        """

        :param hex_str:
        :param signed_byte_handling: Byte in Java is represented by signed int in range (-128, 127), Byte Python is represented by unsigned int in range(0, 255).
        :return:
        """
        dec_num = int(hex_str, 16) if isinstance(hex_str, str) else hex_str
        if 127 < dec_num < 256 and signed_byte_handling:
            dec_num = dec_num - 256
        return dec_num

    @classmethod
    def hex_str_to_dec_list(cls, hex_str, signed_byte_handling=False):
        """

        :param hex_str:
        :param signed_byte_handling: Byte in Java is represented by signed int in range (-128, 127), Byte Python is represented by unsigned int in range(0, 255).
        :return:
        """
        hex_str = cls.trim_and_kill_all_white_spaces(hex_str)
        if len(hex_str) > 2:
            chunk_size = 2
            return [cls.hex_str_to_dec(hex_str[i:i + chunk_size], signed_byte_handling=signed_byte_handling) for i in
                    range(0, len(hex_str), chunk_size)]

    @classmethod
    def rstrip_hex_str(cls, hex_str):
        return cls.rstrip_str(hex_str, 'FF')

    @classmethod
    def rstrip_str(cls, plain_str, data_to_strip):
        # data = data.rstrip('FF')
        # data = data[:data.rfind('FF$')]
        # Must be removed in pair
        # pattern = '(FF)*$'
        pattern = '(' + data_to_strip + ')*$'
        return re.sub(pattern, '', plain_str)

    @classmethod
    def lstrip_hex_str(cls, hex_str):
        return cls.lstrip_str(hex_str, 'FF')

    @classmethod
    def lstrip_str(cls, plain_str, data_to_strip):
        pattern = '^(' + data_to_strip + ')*'
        return re.sub(pattern, '', plain_str)

    @classmethod
    def analyse_profile(cls, base_profile, imp_info=False):
        if isinstance(base_profile, bytes):
            base_profile = base_profile.hex()
        bp_name = ''
        bp_status = False
        if _base_profiles_available:
            for key in base_profiles.profile_pool_hex:
                if base_profiles.profile_pool_hex.get(key).lower() in base_profile.lower():
                    bp_name = key
                    bp_status = True
                    break
        # Logic is needed to analyse Custom Profiles
        msg = [f'Profile Name is: {bp_name}{" (Base Profile)" if bp_status else ""}']
        if imp_info:
            module_name = PhModules.PYCRATE
            module_version = cls.get_module_version(module_name)
            msg.append(f'\nImportant Info: {module_name} version is: {module_version}')
        return '\n'.join(msg), bp_status

    @classmethod
    def get_key_from_dict_based_on_val(cls, my_dict, value_to_check, operation=None):
        for key, value in my_dict.items():
            if operation == 'startswith':
                if value_to_check.startswith(value):
                    return key
            elif value == value_to_check:
                return key
        return None

    @classmethod
    def remove_file(cls, file_path):
        if cls.file_dir_exists(file_path):
            os.remove(file_path)
            print('File {0} deleted successfully.'.format(file_path))
        else:
            print(f'File {file_path} does not exist.')

    @classmethod
    def get_file_size(cls, file_path, unit_level=None, print_also=False):
        default_unit_level = 1
        size_unit = 1024
        level_mapping = {
            0: ('Bits', -1),
            1: ('Bytes', 0),
            2: ('KB (Kilobytes)', 1),
            3: ('MB (Megabytes)', 2),
            4: ('GB (Gigabytes)', 3),
            5: ('TB (Terabytes)', 4),
            6: ('PB (Petabytes)', 5),
            7: ('EB (Exabytes)', 6),
        }
        if cls.file_dir_exists(file_path):
            file_size_bytes = os.path.getsize(file_path)
            if unit_level not in level_mapping.keys():
                unit_level = default_unit_level
            level_data = level_mapping.get(unit_level)
            _unit_level_opration = level_data[1]
            if _unit_level_opration == -1:  # Bits
                file_size_bytes = file_size_bytes * 8
            elif _unit_level_opration == 0:  # Bytes
                file_size_bytes = file_size_bytes
            else:
                file_size_bytes = {file_size_bytes / (size_unit * _unit_level_opration)}
            msg = f'{file_size_bytes} {level_data[0]}'
            if print_also:
                print(f'File Size: {msg}')
        else:
            print(f'File {file_path} does not exist.')
        return msg

    @classmethod
    def file_dir_exists(cls, file_path):
        return True if os.path.exists(file_path) else False

    @classmethod
    def get_current_func_name(cls, parent_level=1):
        # print(inspect.stack()[0][3])  # will give current
        # print(inspect.stack()[1][3])  # will give the caller (Parent)
        # print(inspect.stack()[2][3])  # will give the caller of caller (Grand Parent)
        # cls.print_iter(inspect.stack())
        return inspect.stack()[parent_level][3]

    @classmethod
    def enclose(cls, format, data1, data2='', indent_level=0):
        space = '  ' * indent_level
        if format == PhConstants.ENCLOSE_COMMENT:
            return space + '-- ' + str(data1)
        if format == PhConstants.ENCLOSE_HEX:
            return space + "'" + str(data1) + "'H"
        if format == PhConstants.ENCLOSE_NAME_VALUE:  # identification 0
            return space + data1 + ' ' + data2
        if format == PhConstants.ENCLOSE_NAME_VALUE_HEX:  # efFileSize '68'H
            return space + data1 + ' ' + cls.enclose(PhConstants.ENCLOSE_HEX, data2)
        if format == PhConstants.ENCLOSE_NAME_VALUE_DICT:  # doNotCreate : NULL
            return space + data1 + ' : ' + data2
        if format == PhConstants.ENCLOSE_NAME_VALUE_HEX_DICT:  # filePath : '7FF1'H
            return space + data1 + ' : ' + cls.enclose(PhConstants.ENCLOSE_HEX, data2)
        if format in [PhConstants.ENCLOSE_NAME_VALUE_SEQ,
                      PhConstants.ENCLOSE_NAME_VALUE_SEQ_DICT]:  # templateID {0 0} # fileDescriptor : {...}
            separator = ' ' if format == PhConstants.ENCLOSE_NAME_VALUE_SEQ else ' : '
            if data1 == '':
                separator = ''
            if isinstance(data2, str):
                return space + data1 + separator + '{' + data2 + '}'
            if isinstance(data2, list):
                if len(data2) == 0:  # Empty List
                    return space + data1 + separator + '{ }'
                return space + data1 + separator + '{\n' + ',\n'.join(data2) + '\n' + space + '}'
        return data1

    @classmethod
    def normalise_name_user_to_pandas(cls, col_name, upper_case=True, fix_names=[]):
        # Remove unwanted var_out
        res_items = [ele for ele in PhConstants.KEYWORD_VARIABLE_DECLARATION_OUT if (ele in col_name)]
        for item in res_items:
            col_name = col_name.replace(item, '')
        # Remove these Chars
        temp_data = re.sub(r'[(]|[)]|[.]|[:]', repl='', string=col_name)
        # Strip Unnecessary White Spaces
        temp_data = temp_data.strip()
        # Replace these Chars
        temp_data = re.sub(r'[ ]|[/]', repl='_', string=temp_data)
        # Remove Multiple Occurrences Of '_'
        temp_data = re.sub(r'[_]+', repl='_', string=temp_data)
        # Convert the case
        if fix_names:
            temp_fix_names = [each_string.lower() for each_string in fix_names]
            if temp_data.lower() in temp_fix_names:
                return fix_names[temp_fix_names.index(temp_data.lower())]
        temp_data = temp_data.upper() if upper_case else temp_data.lower()
        return temp_data

    @classmethod
    def normalise_name_pandas_to_user(cls, col_name, all_caps_keywords=None):
        """

        :param col_name:
        :param all_caps_keywords:
        :return:
        """
        if all_caps_keywords is None:
            all_caps_keywords = ['ICCID', 'IMSI', 'ID', 'MSISDN']
        return ' '.join(
            x.title() if x not in all_caps_keywords else x for x in [x for x in re.split('_', string=str(col_name))])

    @classmethod
    def normalise_user_input(cls, user_input):
        """

        :param user_input:
        :return:
        """
        temp_user_input = cls.str_to_bool(user_input)
        if temp_user_input is not None:
            return temp_user_input
        if user_input in PhConstants.EXIT_VALUE_POOL:
            # return 'e'
            sys.exit()
        print(f'Oops! "{user_input}" was not a valid input. Try again...')
        return None

    @classmethod
    def normalise_list(cls, user_list):
        new_list = copy.copy(PhConstants.LIST_EMPTY)
        for item in user_list:
            if cls.is_none(item):
                continue
            if isinstance(item, list):
                new_list.extend(item)
            else:
                new_list.append(item)
        return new_list

    @classmethod
    def read_csv(cls,
                 file_name,
                 sep='\s+',
                 rename_col=False,
                 comment='*',
                 print_shape=True,
                 print_frame=False,
                 # encoding='unicode_escape',
                 names=None,
                 encoding=None,
                 log=None,
                 ):
        if names:
            obj = pd.read_csv(file_name, sep=sep, dtype='str', na_filter=False, skip_blank_lines=True, comment=comment,
                              encoding=encoding, names=names)
        else:
            obj = pd.read_csv(file_name, sep=sep, dtype='str', na_filter=False, skip_blank_lines=True, comment=comment,
                              encoding=encoding)
        #
        rename_col_dict = {}
        if rename_col:
            # Fixing Messy Column Names
            for col_name in list(obj):
                rename_col_dict[col_name] = cls.normalise_name_user_to_pandas(col_name)
            obj.rename(columns=rename_col_dict, inplace='True')
        if print_shape:
            cls.print_data_frame_shape(obj, '' if isinstance(file_name, StringIO) else file_name, log=log)
        if print_frame:
            cls.print_data_frame(obj, log=log)
        return obj

    @classmethod
    def to_csv(cls, output, file_name, str_append='', new_ext='', sep=' ', index=False, print_shape=True,
               print_frame=False, log=None,
               encoding=PhDefaults.CHAR_ENCODING, encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS):
        """

        :param output: DataFrame
        :param file_name:
        :param str_append:
        :param new_ext:
        :param sep:
        :param index:
        :param print_shape:
        :param print_frame:
        :param encoding:
        :param log:
        :return:
        """
        if output is None:
            return None
        if isinstance(output, DataFrame) or isinstance(output, Series):
            if print_shape:
                cls.print_data_frame_shape(output, file_name, log=log)
            if print_frame:
                cls.print_data_frame(output)
            if str_append or new_ext:
                file_name = cls.append_in_file_name(str_file_path=file_name, str_append=str_append, new_ext=new_ext)
            cls.make_dirs(cls.get_file_name_and_extn(file_name, only_path=True))
            output.to_csv(path_or_buf=file_name, index=index, sep=sep, encoding=encoding, errors=encoding_errors)
            return file_name
        return cls.to_file(output_lines=output, file_name=file_name, str_append=str_append, new_ext=new_ext,
                           encoding=encoding, encoding_errors=encoding_errors)

    @classmethod
    def to_file(cls, output_lines, file_name='', str_append='', new_ext='', lines_sep='\n',
                encoding=PhDefaults.CHAR_ENCODING, encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS,
                back_up_file=False, file_path_is_dir=None):
        """

        :param file_path_is_dir:
        :param output_lines:
        :param file_name:
        :param str_append:
        :param new_ext:
        :param lines_sep:
        :param encoding:
        :param encoding_errors:
        :param back_up_file:
        :return:
        """
        if output_lines is None:
            return None
        if back_up_file:
            file_name = cls.backup_file_name(str_file_path=file_name, file_path_is_dir=file_path_is_dir)
        if str_append or new_ext:
            file_name = cls.append_in_file_name(str_file_path=file_name, str_append=str_append, new_ext=new_ext)
        folder_path = cls.get_file_name_and_extn(file_name, only_path=True)
        if folder_path:
            cls.make_dirs(folder_path)
        with open(file_name, 'w', encoding=encoding, errors=encoding_errors) as file_write:
            if isinstance(output_lines, list):
                file_write.writelines(lines_sep.join(output_lines))
            else:
                file_write.write(output_lines)
        return file_name

    @classmethod
    def compare_two_data_frame(cls, file_input_left, file_input_right, col_name, file_result='', sort=False,
                               print_shape=True,
                               print_frame=False, encoding=None, log=None):
        local_data_left = file_input_left if isinstance(file_input_left, DataFrame) else \
            cls.read_csv(file_input_left, sep=',', encoding=encoding, log=log)
        local_data_right = file_input_right if isinstance(file_input_right, DataFrame) else \
            cls.read_csv(file_input_right, sep=',', encoding=encoding, log=log)
        file_output_left = ''
        file_output_common = ''
        file_output_right = ''
        if not file_result:
            file_result = cls.append_in_file_name(
                str_file_path=cls.append_in_file_name(
                    str_file_path=os.sep.join([cls.path_default_out_folder, '']),
                    str_append=[col_name, '1st'], new_ext='.txt')
                if isinstance(file_input_left, DataFrame) else file_input_left,
                str_append=['vs', ('2nd' if isinstance(file_input_right, DataFrame) else
                                   cls.get_file_name_and_extn(file_input_right, name_with_out_extn=True))])
        """
        Left
        """
        file_output_left = cls.append_in_file_name(str_file_path=file_result, str_append='left')
        # outData = local_data_left[~local_data_left.col_name.isin(local_data_right.col_name)] # Getting error for this
        out_data = local_data_left[~local_data_left[col_name].isin(local_data_right[col_name])]
        out_data.to_csv(path_or_buf=file_output_left, index=False)
        if sort:
            file_output_left = cls.append_in_file_name(str_file_path=file_output_left, str_append='sorted')
        out_data = out_data.sort_values(by=col_name)
        out_data.to_csv(path_or_buf=file_output_left, index=False)
        if print_shape:
            cls.print_data_frame_shape(out_data, file_output_left, log=log)
        if print_frame:
            cls.print_data_frame(out_data, log=log)
        """
        Right
        """
        file_output_right = cls.append_in_file_name(str_file_path=file_result, str_append='right')
        out_data = local_data_right[~local_data_right[col_name].isin(local_data_left[col_name])]
        out_data.to_csv(path_or_buf=file_output_right, index=False)
        if sort:
            file_output_right = cls.append_in_file_name(str_file_path=file_output_right, str_append='sorted')
        out_data = out_data.sort_values(by=col_name)
        out_data.to_csv(path_or_buf=file_output_right, index=False)
        if print_shape:
            cls.print_data_frame_shape(out_data, file_output_right, log=log)
        if print_frame:
            cls.print_data_frame(out_data, log=log)
        """
        Common
        """
        file_output_common = cls.append_in_file_name(str_file_path=file_result, str_append='common')
        out_data = local_data_left[local_data_left[col_name].isin(local_data_right[col_name])]
        out_data.to_csv(path_or_buf=file_output_common, index=False)
        if sort:
            file_output_common = cls.append_in_file_name(str_file_path=file_output_common, str_append='sorted')
            out_data = out_data.sort_values(by=col_name)
            out_data.to_csv(path_or_buf=file_output_common, index=False)
        if print_shape:
            cls.print_data_frame_shape(out_data, file_output_common, log=log)
        if print_frame:
            cls.print_data_frame(out_data, log=log)
        return file_output_left, file_output_common, file_output_right

    @classmethod
    def strip_all_columns(cls, df_input):
        df_obj = df_input.select_dtypes(['object'])
        df_input[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        return df_input

    """
        Help: Print
        options:
        print(list(output))
        output.info()
        print(output)
        print(output.head())
        print(output[['ICCID']])
        print(output['ICCID'].head())
    """

    @classmethod
    def print_data_frame(cls, output, cmt='', level=0, log=None):
        """

        :param output:
        :param cmt:
        :param level:
        :param log:
        :return:
        """
        print_or_log = log.info if log else print
        if not isinstance(output, DataFrame):
            return
        pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        print_or_log(cmt)
        if level == 0:
            print_or_log(output.head())
        if level == 1:
            print_or_log(output.tail())
        if level == 2:
            print_or_log(output.to_string(index=False))
        if level == 3:
            pd.set_option('display.max_rows', None, 'display.max_columns', None)
            print_or_log(output)

    @classmethod
    def print_data_frame_shape(cls, output, cmt='', level=1, log=None):
        if not isinstance(output, DataFrame):
            return
        print_or_log = log.info if log else print
        print_or_log(','.join(filter(None, ['Shape: {} x {}'.format(output.shape[0], output.shape[1]), cmt])))
        # Faster alternate
        # count_row = len(output.index)
        if level < 1:
            return
        print_or_log(f'Cols Headers: {list(output)}')
        if level < 2:
            return
        print_or_log(output.info())

    @classmethod
    def find_offset_of_next_non_white_space_char(cls, temp, current_offset):
        new_offset = current_offset
        for a in temp[current_offset:]:
            if not a.isspace():
                break
            new_offset += 1
        return new_offset

    @classmethod
    def str_insert_char_repeatedly(cls, my_str, group=3, char=',', reverse=False):
        my_str = str(my_str)
        start = 0
        end = len(my_str)
        pre_str = ''
        post_str = ''
        if reverse:
            start = end % group
            pre_str = my_str[0:start]
        post_str = char.join(my_str[i:i + group] for i in range(start, end, group))
        return char.join(filter(None, [pre_str, post_str]))

    @classmethod
    def prepare_file_name(cls, keywords_list, file_ext='.txt', time_stamp=True):
        sep = '_'
        file_name = keywords_list
        time_str = cls.get_time_stamp(files_format=True) if time_stamp else ''
        if isinstance(keywords_list, list):
            keywords_list.append(time_str)
            file_name = sep.join(filter(None, keywords_list))
        sep = ''
        return sep.join([file_name, file_ext])

    @classmethod
    def format_profile_parsing_log(cls, profile_hex_data, profiles_asn_data, profile_name=None):
        """

        :param profile_hex_data:
        :param profiles_asn_data:
        :param profile_name:
        :return: dict with log_folder, log_name, log_data
        """
        if not profile_name:
            profile_name = 'Profile'
        full_logging = True if (profile_hex_data and profiles_asn_data) else False
        logging_data_list = []
        file_ext = '.txt'
        log_folder = None
        file_name_keywords = []
        if full_logging:
            res_profile_name, res_bp_status = cls.analyse_profile(profile_hex_data)
            logging_data_list.append(res_profile_name)
            logging_data_list.append('\n\n' + 'Hex Profile is: \n')
        else:  # Any one is definitely True
            if not profile_hex_data:
                log_folder = 'asn1'
                file_ext = '.asn1'
            if not profiles_asn_data:
                log_folder = 'hex'
                file_ext = '.hex'
        log_name = cls.append_in_file_name(str_file_path=profile_name, str_append=file_name_keywords, new_ext=file_ext,
                                           # Profile name could have a '.'
                                           ext_available_in_file_name=False)
        if profile_hex_data:
            logging_data_list.append(profile_hex_data)
        if full_logging:
            logging_data_list.append('\n\n' + 'ASN Profile is: \n')
        if profiles_asn_data:
            logging_data_list.append(profiles_asn_data)
        return {
            'log_folder': log_folder,
            'log_name': log_name,
            'log_content': ''.join(logging_data_list),
        }

    @classmethod
    def ascii_to_hex_str(cls, ascii_str):
        return ascii_str.encode(PhConstants.CHAR_ENCODING_UTF8).hex()

    @classmethod
    def hex_str_to_ascii(cls, str_data, only_if_printable=True, encoding=PhConstants.CHAR_ENCODING_UTF8,
                         encoding_errors=PhConstants.CHAR_ENCODING_ERRORS_STRICT):
        printable = True
        res = ''
        if only_if_printable:
            # Check if printable
            hex_bytes = [cls.hex_str_to_dec(str_data[i:i + 2]) for i in range(0, len(str_data), 2)]
            printable = all((0x20 <= hex_byte <= 0x7E) for hex_byte in hex_bytes)
        if printable:
            try:
                res = bytearray.fromhex(str_data).decode(encoding=encoding, errors=encoding_errors)
            except UnicodeDecodeError:
                pass
        return res

    @classmethod
    def gen_acc(cls, str_imsi):
        """

        :param str_imsi:
        :return:
        """
        # formula: 2 ^ imsi_last_digit
        return cls.dec_to_hex(pow(2, int(str_imsi[-1])), 4)

    @classmethod
    def gen_isim_data(cls, imsi, mcc_mnc, pattern_or_data):
        """

        :param imsi:
        :param mcc_mnc:
        :param pattern_or_data: Could be pattern as well as real data
        :return:
        """
        if pattern_or_data is not None:
            mcc = ''
            mnc = ''
            if mcc_mnc is not None:
                mcc = mcc_mnc[0:3]
                # MNC must be padded with 0 if needed
                mnc = mcc_mnc[3:].zfill(3)
            pattern_or_data = pattern_or_data.replace('${IMSI}', imsi)
            pattern_or_data = pattern_or_data.replace('${MCC}', mcc)
            pattern_or_data = pattern_or_data.replace('${MNC}', mnc)
        return pattern_or_data

    @classmethod
    def to_hex_string(cls, bytes_data=[], required_format=0):
        """
        Returns a hex string representing bytes

        :param bytes_data: a list of bytes to stringify; e.g. [59, 22, 148, 32, 2, 1, 0, 0, 13]
        :param required_format: a logical OR of
            - COMMA: add a comma between bytes
            - HEX: add the 0x chars before bytes
            - UPPERCASE: use 0X before bytes (need HEX)
            - PACK: remove blanks
        :return:
        """
        if type(bytes_data) is not list:
            raise TypeError('not a list of bytes')

        if bytes_data is None or bytes_data == []:
            return ''
        else:
            pformat = '%-0.2X'
            if PhConstants.FORMAT_HEX_STRING_AS_COMMA & required_format:
                separator = ','
            else:
                separator = ''
            if not PhConstants.FORMAT_HEX_STRING_AS_PACK & required_format:
                separator = separator + ' '
            if PhConstants.FORMAT_HEX_STRING_AS_HEX & required_format:
                if PhConstants.FORMAT_HEX_STRING_AS_UPPERCASE & required_format:
                    pformat = '0X' + pformat
                else:
                    pformat = '0x' + pformat
            return (separator.join(map(lambda a: pformat % ((a + 256) % 256), bytes_data))).rstrip()

    @classmethod
    def check_and_assign(cls, primary_value, secondary_value):
        """

        :param primary_value:
        :param secondary_value:
        :return:
        """
        if primary_value is not None:
            return primary_value
        if secondary_value is not None:
            return secondary_value
        return None

    @classmethod
    def get_version_from_name(cls, name, max_depth=None, trim_v=False):
        """

        :param name:
        :param max_depth:
        :param trim_v:
        :return:
        """
        if max_depth is None:
            match = re.search(r'(v|V)([\d._-])*(\d)', name)
        else:
            match = re.search(r'(v|V)([\d._-]){0,' + str(max_depth + 1) + r'}(\d)', name)
        if match:
            result = re.sub('[._-]', '_', match.group(0))
            return result[1:] if trim_v else result
        return ''

    @classmethod
    def print_all_environment_variables(cls, custom_only=False):
        """

        :param custom_only:
        :return:
        """
        if custom_only:
            for var in PhConstants.ENV_VARIABLES:
                print(cls.get_environment_variables(var))
        else:
            cls.print_iter(os.environ)

    @classmethod
    def str_to_bool(cls, value):
        """

        :param value:
        :return:
        """
        if isinstance(value, bool):
            return value
        value = value.lower().strip()
        if value in PhConstants.TRUE_VALUE_POOL:
            return True
        elif value in PhConstants.FALSE_VALUE_POOL:
            return False
        return None

    @classmethod
    def is_clean_name(cls, name):
        """

        :param name:
        :return:
        """
        return not name.startswith('_') and not name.endswith('_')

    @classmethod
    def clean_names(cls, lst):
        return [n for n in lst if cls.is_clean_name(n)]

    @classmethod
    def get_obj_list(cls, cls_to_explore, obj_name_filter='', obj_name_needed=True,
                     obj_value_to_find=None, clean_name=False, sort=True, print_also=False):
        """

        :param print_also:
        :param cls_to_explore:
        :param obj_name_filter:
        :param obj_name_needed:
        :param obj_value_to_find:
        :param clean_name:
        :param sort:
        :return:
        """

        def __get_obj_list(cls_to_explore, obj_name_filter, obj_name_needed, obj_value_to_find, clean_name, sort):
            if cls_to_explore is None:
                return ''
            obj_dict = cls_to_explore.__dict__
            obj_list = [obj for obj in obj_dict]
            if obj_name_filter:
                obj_list = [obj for obj in obj_list if str(obj).startswith(obj_name_filter)]
            if obj_name_needed is not True:
                obj_list = [getattr(cls_to_explore, obj) for obj in obj_list]
            if obj_name_needed:
                if clean_name:
                    obj_list = cls.clean_names(obj_list)
                if sort:
                    obj_list.sort()
            if len(obj_list) > 0 and isinstance(obj_list[0], list):
                obj_list = obj_list[0]
            if isinstance(cls_to_explore, enum.EnumMeta):
                obj_list = [cls_to_explore(obj).name for obj in obj_list]
            if obj_value_to_find is None:
                return obj_list
            for obj in obj_list:
                if isinstance(obj, cls_to_explore):
                    if obj.value == obj_value_to_find:
                        return obj.name
            return ''

        data = __get_obj_list(cls_to_explore, obj_name_filter, obj_name_needed, obj_value_to_find, clean_name, sort)
        if print_also:
            cls.print_iter(data)
        return data

    @classmethod
    def get_classes_list(cls, module_to_explore, parent_class=None, obj_name_needed=True, sort=True, print_also=False):
        def __get_classes_list(module_to_explore, parent_class, obj_name_needed, sort):
            INDEX_CLASS_NAME = 0
            INDEX_CLASS_OBJECT = 1
            if module_to_explore is None:
                return ''
            if parent_class is None:
                classes_list = [cls for cls in inspect.getmembers(module_to_explore, inspect.isclass) if
                                cls[INDEX_CLASS_OBJECT].__module__ == module_to_explore.__name__]
            else:
                classes_list = [cls for cls in inspect.getmembers(module_to_explore, inspect.isclass) if
                                issubclass(cls[INDEX_CLASS_OBJECT], parent_class)]
            if obj_name_needed is True:
                classes_list = [cls_name for cls_name, cls in classes_list]
            else:
                classes_list = [cls for cls_name, cls in classes_list]
            if sort:
                classes_list.sort()
            return classes_list

        data = __get_classes_list(module_to_explore, parent_class=parent_class, obj_name_needed=obj_name_needed,
                                  sort=sort)
        if print_also:
            cls.print_iter(data, depth_level=0)
        return data

    @classmethod
    def get_environment_variables(cls, var_name, var_default_value=None, check_presence_only=False):
        """

        :param var_name:
        :param var_value:
        :param check_presence_only:
        :return:
        """
        # Check for Custom Variables
        env_variable_name, env_variable_default_value = PhConstants.ENV_VARIABLES.get(var_name, (None, None))
        env_variable_name = cls.set_if_none(env_variable_name, var_name)
        env_variable_default_value = cls.set_if_none(env_variable_default_value, var_default_value)
        try:
            env_variable_value = os.environ[env_variable_name]
            if check_presence_only:
                return True
            print(f'Environment Variable {env_variable_name} Found, value is {env_variable_value}')
        except:
            if check_presence_only:
                return False
            print(
                f'Environment Variable {env_variable_name} Not Found, using default Value {env_variable_default_value}')
            env_variable_value = env_variable_default_value
        return env_variable_value

    @classmethod
    def format_data_as_hex(cls, str_data):
        """

        :param str_data:
        :return:
        """
        return ' '.join(re.findall('([0-9a-zA-Z]{2}|[0-9a-zA-Z])', str_data))

    @classmethod
    def append_path(cls, dir_file_list):
        """

        :param dir_file_list:
        :return:
        """
        return os.sep.join(filter(None, dir_file_list))

    @classmethod
    def cpu_usage(cls):
        """

        :return:
        """
        if _psutil_available:
            res = psutil.cpu_times()
            print(f'cpu_times is {res}')

            res = psutil.cpu_percent(0.1)
            print(f'cpu_percent is {res}')

            res = psutil.cpu_times_percent(0.1)
            print(f'cpu_times_percent is {res}')

            res = psutil.cpu_stats()
            print(f'cpu_stats is {res}')

            res = psutil.cpu_freq()
            print(f'cpu_freq is {res}')

            res = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
            print(f'getloadavg is {res}')

    @classmethod
    def get_module_version(cls, module_name=PhModules.PYCRATE, minimum_version_required=None):
        """

        :param module_name:
        :param minimum_version_required:
        :return:
        """
        module_version = pkg_resources.get_distribution(module_name).version
        module_version = version.parse(module_version)
        if minimum_version_required:
            minimum_version_required = version.parse(minimum_version_required)
            version_available = True if module_version >= minimum_version_required else False
            return module_version, version_available
        else:
            return module_version

    @classmethod
    def get_user_details_display_name(cls):
        """

        :return:
        """
        if _ctypes_windll_available:
            get_user_name_ex = windll.secur32.GetUserNameExW
            name_display = 3

            size = ctypes.pointer(ctypes.c_ulong(0))
            get_user_name_ex(name_display, None, size)

            name_buffer = ctypes.create_unicode_buffer(size.contents.value)
            get_user_name_ex(name_display, name_buffer, size)
            return name_buffer.value
        if _pwd_available:
            # print(f'User ID (getuid; 0) is {os.getuid()}')
            # print(f'User ID (geteuid; 0) is {os.geteuid()}')
            # cls.print_iter(pwd.getpwall(), header='pwd.getpwall(); List All Users')
            # print(f'User Account (pwd.getpwuid(os.getuid())[4]) is {next(entry[4] for entry in pwd.getpwall() if entry[2] == os.geteuid())}')
            # print(f'User Account (pwd.getpwuid(os.getuid()).pw_gecos) is {pwd.getpwuid(os.getuid()).pw_gecos}')
            # print(f'User Account (pwd.getpwuid(os.getuid())[4]) is {pwd.getpwuid(os.getuid())[4]}')
            # print(f'User Account (pwd.getpwuid(os.geteuid())[4]) is {pwd.getpwuid(os.geteuid())[4]}')
            return pwd.getpwuid(os.getuid()).pw_gecos

    @classmethod
    def get_user_details_account_name(cls):
        """

        :return:
        """
        user_name = os.getlogin()
        # print(f'User Account (getpass) is {getpass.getuser()}')
        # print(f'User Account (getlogin) is {os.getlogin()}')
        # if _ctypes_windll_available:
        #     print(f'User Account (os.environ) is {os.environ.get("USERNAME")}')
        # if _pwd_available:
        #     print(f'User Account (getpwuid; pw_name) is {pwd.getpwuid(os.getuid()).pw_name}')
        #     print(f'User Account (getpwuid; 0) is {pwd.getpwuid(os.getuid())[0]}')
        return user_name

    @classmethod
    def append_remarks(cls, main_remarks, additional_remarks=None, max_length=PhConstants.REMARKS_MAX_LENGTH,
                       append_mode_post=True):
        main_remarks = cls.set_if_none(main_remarks, new_type=str)
        additional_remarks = cls.set_if_none(additional_remarks, new_type=str)
        len_sep = len(PhConstants.SEPERATOR_MULTI_OBJ) if len(main_remarks) > 0 and len(additional_remarks) > 0 else 0
        len_main_remarks = len(main_remarks)
        diff_length = len_main_remarks - max_length + len_sep + PhConstants.DEFAULT_TRIM_STRING_LENGTH
        if diff_length > 0:
            return cls.trim_remarks(main_remarks, max_length)
        diff_length = max_length - len_main_remarks - len_sep
        additional_remarks = cls.trim_remarks(additional_remarks, diff_length)
        if append_mode_post:
            return cls.combine_list_items([main_remarks, additional_remarks])
        else:
            return cls.combine_list_items([additional_remarks, main_remarks])

    @classmethod
    def trim_remarks(cls, user_remarks, max_length=PhConstants.REMARKS_MAX_LENGTH):
        if len(user_remarks) > max_length > 0:
            # Trimming is needed
            user_remarks = user_remarks[
                           :max_length - PhConstants.DEFAULT_TRIM_STRING_LENGTH] + PhConstants.DEFAULT_TRIM_STRING
        return user_remarks

    @classmethod
    def to_list(cls, obj, all_str=False, trim_data=True):
        data_list = [] if obj is None else (obj if isinstance(obj, list) else [obj])
        if all_str:
            data_list = [str(x) for x in data_list]
        if trim_data:
            data_list = [cls.trim_white_spaces_in_str(x) for x in data_list]
        return data_list

    @classmethod
    def extend_list(cls, obj, expected_length=0, filler='', unique_entries=False, trim_data=False):
        obj = cls.to_list(obj, trim_data=trim_data)
        current_length = len(obj)
        if expected_length <= current_length:
            return obj
        target_filler = filler if filler or current_length < 1 else obj[-1]
        if trim_data:
            target_filler = cls.trim_white_spaces_in_str(target_filler)
        extended_list = ([target_filler] * (expected_length - current_length))
        if unique_entries:
            extended_list = [PhConstants.SEPERATOR_FILE_NAME.join(filter(None, [str(x), str(y + 1)])) for x, y in
                             zip(extended_list, range(len(extended_list)))]
        return obj + extended_list

    @classmethod
    def combine_list_items(cls, list_data, trim_data=True, clean_data=True):
        if not isinstance(list_data, list):
            temp = list_data
            list_data = list()
            list_data.append(temp)
        list_data = list(filter(None, list_data))
        if trim_data:
            list_data = [x.strip() if x is not None and isinstance(x, str) else x for x in list_data]
        if clean_data:
            list_data = [re.sub(r'^(;+ *)*|(;+ *)*$', '', x) if x is not None and isinstance(x, str) else x for x in
                         list_data]
        if 0 < len(list_data) < 2:
            return list_data[0]
        list_data = [str(x) for x in list_data]
        res = PhConstants.SEPERATOR_MULTI_OBJ.join(list_data)
        return res

    @classmethod
    def get_absolute_path(cls, rel_path):
        return os.path.abspath(rel_path)

    @classmethod
    def get_relative_path(cls, abs_path):
        return os.path.relpath(abs_path)

    @classmethod
    def get_current_dir_path(cls):
        return cls.path_current_folder

    @classmethod
    def get_current_script_path(cls):
        path_current_file = os.path.realpath(__file__)
        # path_current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
        return path_current_file

    @classmethod
    def get_current_script_folder(cls):
        return cls.get_directory_path(cls.get_current_script_path())

    @classmethod
    def get_directory_path(cls, path):
        return os.path.dirname(path)

    @classmethod
    def generalise_list(cls, data_list, append_na=True, sort=True, append_others=False):
        new_data_list = data_list.copy() if data_list is not None else []
        if sort:
            new_data_list.sort()
        if append_na:
            new_data_list.insert(PhConstants.OFFSET_ZERO, PhConstants.STR_SELECT_OPTION)
        if append_others:
            new_data_list.append(PhConstants.STR_OTHER_OPTION)
        return new_data_list

    @classmethod
    def generalise_list_reverse(cls, data_list):
        new_data_list = data_list.copy() if data_list is not None else []
        if cls.is_generalised_item(new_data_list[PhConstants.OFFSET_ZERO], PhConstants.STR_SELECT_OPTION):
            new_data_list = new_data_list[1:]
        if cls.is_generalised_item(new_data_list[-1], PhConstants.STR_OTHER_OPTION):
            new_data_list = new_data_list[:-1]
        return new_data_list

    @classmethod
    def is_generalised_item(cls, item, target_item=PhConstants.STR_SELECT_OPTION):
        return True if str(item) in target_item else False

    @classmethod
    def filter_processing_related_keys(cls, data_dic):
        return {k: v for k, v in data_dic.items() if not (k.startswith(PhKeys.SAMPLE) or k.startswith(PhKeys.PROCESS))}

    @classmethod
    def generate_key_and_data_group(cls, remarks):
        remarks = cls.to_list(remarks, all_str=True, trim_data=True)[0]
        data_group_list = remarks.split(PhConstants.SEPERATOR_MULTI_OBJ)
        data_group = data_group_list[0] if len(data_group_list) > 0 else data_group_list
        return remarks, data_group

    @classmethod
    def dict_merge(cls, dict1, dict2):
        if not dict2:
            return dict1
        if not dict1:
            return dict2
        return {**dict1, **dict2}

    @classmethod
    def dict_clean(cls, dict1):
        return {k: v for k, v in dict1.items() if v is not None}

    @classmethod
    def dict_update(cls, dict1, key_pair_list):
        key_pair_list = cls.to_list(key_pair_list, trim_data=False)
        for key_pair in key_pair_list:
            dict1.update(key_pair)
        return dict1

    @classmethod
    def list_clean(cls, list1):
        return [x for x in list1 if x is not None]

    @classmethod
    def archive_files(cls, source_files_dir, archive_format=PhDefaults.ARCHIVE_FORMAT, delete_dir_after_archive=False,
                      export_hash=False):
        if archive_format == PhFileExtensions.ZIP:
            return cls.zip_and_clean_dir(source_files_dir=source_files_dir,
                                         delete_dir_after_zip=delete_dir_after_archive,
                                         export_hash=export_hash)
        return None

    @classmethod
    def create_zip(cls, zip_file_name, source_dir, keep_source_dir_in_zip=False, include_files=None, include_dirs=None,
                   excludes=None):
        files_list = []
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            files_list = cls.traverse_it(top=source_dir, include_files=include_files, include_dirs=include_dirs,
                                         excludes=excludes)
            for file_path in files_list:
                rel_path = os.path.join(source_dir, '..') if keep_source_dir_in_zip else source_dir
                zip_file.write(file_path, os.path.relpath(file_path, rel_path))
            return files_list

    @classmethod
    def zip_and_clean_dir(cls, source_files_dir, target_dir=None, target_file_name_wo_extn=None,
                          delete_dir_after_zip=False, keep_source_dir_in_zip=False, export_hash=True,
                          include_files=None, include_dirs=None, excludes=None):
        if not source_files_dir:
            return None
        if not target_file_name_wo_extn:
            target_file_name_wo_extn = cls.get_file_name_and_extn(file_path=source_files_dir)
        if not target_dir or target_dir == source_files_dir:
            # source & target_dir should not be the same
            target_dir = os.sep.join([source_files_dir, os.pardir])
        cls.make_dirs(target_dir)
        zip_file_path = os.sep.join(filter(None, [target_dir, f'{target_file_name_wo_extn}.zip']))
        cls.print_cmt(main_text=f'Exporting Zip File: {zip_file_path}')
        # shutil.make_archive(base_name=zip_file_name, format='zip', root_dir=folder_path)
        files_list = cls.create_zip(zip_file_path, source_files_dir, keep_source_dir_in_zip=keep_source_dir_in_zip,
                                    include_files=include_files, include_dirs=include_dirs, excludes=excludes)
        if export_hash:
            hash_file_path = os.sep.join(filter(None, [target_dir, f'{target_file_name_wo_extn}.hash']))
            cls.print_cmt(main_text=f'Exporting Hash of Files inside Zip File: {hash_file_path}')
            # Zip file contains Time stamp of archived files, hence its hash is changing always
            # so Grab the hash of individual files
            cls.generate_hash(files_list, hash_file_path)
        if delete_dir_after_zip:
            cls.clean_dirs(source_files_dir)
        return zip_file_path

    @classmethod
    def generate_hash(cls, files_list, hash_file_path):
        cls.print_work_in_progress()

    @classmethod
    def all_chars_to_utf8(cls, input_text, current_encoding=None, target_encoding=PhConstants.CHAR_ENCODING_UTF8,
                          encoding_errors=PhDefaults.CHAR_ENCODING_ERRORS, via_regex=True):
        if not input_text:
            return input_text
        if current_encoding is not None and target_encoding is not None:
            input_text = input_text.encode(current_encoding).decode(target_encoding, errors=encoding_errors)
        # List of annoying characters
        replacement_characters_dict = {
            '\x82': ',',  # High code comma
            '\x84': ',,',  # High code double comma
            '\x85': '...',  # Tripple dot
            '\x88': '^',  # High carat
            '\x91': '\x27',  # Forward single quote
            '\x92': '\x27',  # Reverse single quote
            '\x93': '\x22',  # Forward double quote
            '\x94': '\x22',  # Reverse double quote
            '\x95': ' ',
            '\x96': '-',  # High hyphen
            '\x97': '--',  # Double hyphen
            '\x99': ' ',
            '\xa0': ' ',
            '\xa6': '|',  # Split vertical bar
            '\xab': '<<',  # Double less than
            '\xbb': '>>',  # Double greater than
            '\xbc': '1/4',  # one quarter
            '\xbd': '1/2',  # one half
            '\xbe': '3/4',  # three quarters
            '\xbf': '\x27',  # c-single quote
            '\xa8': '',  # modifier - under curve
            '\xb1': '',  # modifier - under line
            ##################################### ISO 78
            '\xe2\x80\x99': '\x27',  # Forward single quote
            '\xe2\x80\x98': '\x27',  # Forward single quote
            '\xe2\x80\x93': '-',  # High hyphen
            '\xe2\x80¦': '...',  # Tripple dot
            #####################################
            "‘": "'",
            "’": "'",
            "…": '...',
            "â€˜": "'",
            "â€™": "'",
            "–": '-',
            "â€“": '-',
        }

        def _replace_chars(match):
            char = match.group(0)
            return replacement_characters_dict[char]

        result_regex = re.sub('(' + '|'.join(replacement_characters_dict.keys()) + ')', _replace_chars, input_text)
        if via_regex:
            return result_regex
        return cls.replace_multiple(input_text=input_text, replacement_characters_dict=replacement_characters_dict)

    @classmethod
    def replace_multiple(cls, input_text, replacement_characters_dict):
        if not input_text:
            return input_text
        if not replacement_characters_dict:
            return input_text
        output_text = input_text
        for key, value in replacement_characters_dict.items():
            to_find = key
            if to_find not in input_text:
                continue
            if isinstance(value, tuple) and len(value) >= 2:
                to_replace = value[0]
                regex_pattern = value[1]
            else:
                to_replace = value
                regex_pattern = None
            search_type = PhConstants.SEARCH_TYPE_PLAIN if (
                    not regex_pattern or regex_pattern is None) else PhConstants.SEARCH_TYPE_REGEX
            if search_type == PhConstants.SEARCH_TYPE_PLAIN:
                output_text = input_text.replace(to_find, to_replace)
            elif search_type == PhConstants.SEARCH_TYPE_REGEX:
                output_text = re.sub(regex_pattern, to_replace, input_text)
        return output_text

    @classmethod
    def popup_msg(cls, msg, caption=None, no_user_interation=False):
        if cls.is_empty(msg):
            return
        print(f'Popup Msg: {msg}')
        if no_user_interation:
            return
        if _ctypes_windll_available:
            message_box_ = windll.user32.MessageBoxW
            caption = cls.set_if_none(caption, os.path.basename(__file__))
            message_box_(0, msg, caption, 1)

    @classmethod
    def clear_quotation_marks(cls, v):
        if cls.is_empty(v) or not isinstance(v, str):
            return v
        if v.startswith('"""') and v.endswith('"""'):
            return v[3:-3]
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            return v[1:-1]
        return v

    @classmethod
    def replace_line_endings(cls, v):
        if cls.is_empty(v) or not isinstance(v, str):
            return v
        if PhConstants.WINDOWS_LINE_ENDING in v:
            return v.replace(PhConstants.WINDOWS_LINE_ENDING, PhConstants.UNIX_LINE_ENDING)
        return v

    @classmethod
    def dict_to_data(cls, user_dict, data_types_include=copy.copy(PhConstants.DICT_EMPTY),
                     data_types_exclude=copy.copy(PhConstants.DICT_EMPTY), trim_quotation_marks=True, trim_data=True,
                     replace_line_endings=True):
        if _debug:
            cls.print_iter(user_dict, 'user_dict initial', verbose=True, depth_level=1)
        cleaning_needed = trim_quotation_marks or trim_data or replace_line_endings
        for k, v in user_dict.items():
            v_org = v
            if cls.is_none(v):
                continue
            if isinstance(v, str):
                v_eval = None
                if cleaning_needed:
                    if trim_data:
                        # Trim Garbage data
                        v = cls.trim_white_spaces_in_str(v)
                    if trim_quotation_marks:
                        v = cls.clear_quotation_marks(v)
                        if trim_data:
                            # Trim spaces again may be uncovered after quotation mark
                            v = cls.trim_white_spaces_in_str(v)
                    if replace_line_endings:
                        # Web Request (Chrome on windows) is sending CRLF, which is causing increment in input data size
                        v = cls.replace_line_endings(v)
                    if _debug:
                        print(
                            f'dict_to_data; {k}'
                            f'; length_before_clean: {len(v_org)}'
                            f'; length_after_clean: {len(v)}'
                        )
                v_lower_case = v.lower()
                try:
                    v_eval = eval(v)
                    if isinstance(v_eval, str):
                        # Everything was already str
                        v_eval = None
                    else:
                        v = v_eval
                        user_dict[k] = v
                    if _debug:
                        print(
                            f'dict_to_data; {k}'
                            f'; type_before_eval: {type(v_org)}'
                            f'; type_after_eval: {type(v)}'
                        )
                except:
                    pass
                # Handel cases which are not supported with eval()
                if v_lower_case in ['none']:
                    # none, None, NONE
                    v = None
                    user_dict[k] = v
                if v_lower_case in ['true']:
                    # true, TruE
                    v = True
                    user_dict[k] = v
                if v_lower_case in ['false']:
                    # false, FaLse
                    v = False
                    user_dict[k] = v
                if v_org != v:
                    user_dict[k] = v
                # Handle Custom Objects (like int, float)
                data_type = type(v)
                data_type_org = type(v_org)
                if k in data_types_exclude:
                    block_data_types = cls.to_list(data_types_exclude.get(k))
                    if data_type in block_data_types and data_type_org not in block_data_types:
                        # new data_type is excluded, set the org data
                        user_dict[k] = v_org
                        continue
                if k in data_types_include:
                    allow_data_types = cls.to_list(data_types_include.get(k))
                    if data_type_org in allow_data_types and data_type not in allow_data_types:
                        # old data_type is included, set the org data
                        user_dict[k] = v_org
                        continue
            if v in [PhConstants.STR_SELECT_OPTION]:
                user_dict[k] = None
                continue
        if _debug:
            cls.print_iter(user_dict, 'user_dict processed', verbose=True, depth_level=1)
        return user_dict

    @classmethod
    def get_dic_data_and_print(cls, key, sep, value, dic_format=True, print_also=True, length_needed=False):
        if value is not None and isinstance(value, str) and '\n' in value:
            value = PreservedScalarString(value)
        return cls.get_key_value_pair(key=key, value=value, sep=sep, dic_format=dic_format, print_also=print_also,
                                      length_needed=length_needed)

    @classmethod
    def get_help_for_param(cls, help_msg=None, default_value=None, include_none=False):
        default_value_msg = None if cls.is_none(
            default_value) and include_none is False else f'{default_value} is Default'
        return PhConstants.SEPERATOR_MULTI_OBJ.join(filter(None, [help_msg, default_value_msg]))

    @classmethod
    def generate_test_data(cls, require_length, sample_data=None, sep=None):
        sample_data = cls.set_if_none(sample_data, PhConstants.TEST_DATA_MIX_LEN_75)
        sep = cls.set_if_none(sep, '\n')
        sample_data_with_sep = sample_data + sep
        #
        len_sample_data_with_sep = len(sample_data_with_sep)
        multiplier = require_length // len_sample_data_with_sep
        # if multiplier < 0:
        #     multiplier = 1
        test_data = sample_data_with_sep * multiplier
        len_diff = require_length - len(test_data)
        if len_diff > 0:
            test_data = test_data + sample_data_with_sep[0:len_diff]
        return test_data

    @classmethod
    def decorate_output_data(cls, output_data):
        if isinstance(output_data, list):
            temp_data = '\n,\n'.join(output_data)
            temp_data = temp_data.replace('\n', '\n  ')
            output_data = f'[\n  {temp_data}\n]'
        return output_data

    @classmethod
    def decorate_info_data(cls, info_data_pool):
        info_objs = [(cls.get_dic_data_and_print(key, PhConstants.SEPERATOR_ONE_LINE, value, dic_format=False,
                                                 print_also=False) if value else None) for key, value in
                     info_data_pool.items()]
        return PhConstants.SEPERATOR_MULTI_OBJ.join(filter(None, info_objs))

    @classmethod
    def adjust_paths(cls, execution_from_inside=False, folder_path=None):
        """

        :param execution_from_inside:
        :param folder_path:
        :return:
        """
        return os.sep.join(
            filter(None, cls.normalise_list([os.pardir if execution_from_inside is True else None, folder_path])))

    @classmethod
    def last_modification_time(cls, file_or_folder_path):
        return datetime.fromtimestamp(os.path.getmtime(file_or_folder_path))

    ####################################################################################################################
    ### INTERNAL ###
    ####################################################################################################################

    @classmethod
    def __handle_dirs(cls, dir_path, file_path, absolute_path_needed, operation_type, quite_mode):
        if cls.is_empty(dir_path) and cls.is_not_empty(file_path):
            dir_path = cls.get_file_name_and_extn(file_path=file_path, only_path=True)
        if absolute_path_needed:
            dir_path = cls.get_absolute_path(dir_path)
        if cls.file_dir_exists(dir_path):
            if operation_type == PhConstants.DIR_CREATION:
                cls.print_cmt(main_text=f'Target Folder: {dir_path}; Already Existed', quite_mode=quite_mode)
            if operation_type == PhConstants.DIR_DELETION:
                if os.path.isdir(dir_path):
                    cls.print_cmt(main_text=f'Target Folder: {dir_path}; Deletion Initiated', quite_mode=quite_mode)
                    shutil.rmtree(dir_path)
                else:
                    cls.print_cmt(main_text=f'Target path {dir_path} does not belongs to a Folder',
                                  quite_mode=quite_mode)
        else:
            if operation_type == PhConstants.DIR_CREATION:
                cls.print_cmt(main_text=f'Target Folder: {dir_path}; Creation Initiated', quite_mode=quite_mode)
                os.makedirs(dir_path)
            if operation_type == PhConstants.DIR_DELETION:
                cls.print_cmt(main_text=f'Target Folder: {dir_path}; Already Deleted', quite_mode=quite_mode)
        return dir_path
