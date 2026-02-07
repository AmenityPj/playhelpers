import copy
import os
import sys
import time
import unittest
from collections import OrderedDict

import play_helpers
from play_helpers.ph_constants import PhConstants
from play_helpers.ph_constants_config import PhConfigConst
from play_helpers.ph_crypto import PhCrypto
from play_helpers.ph_defaults import PhDefaults
from play_helpers.ph_git import PhGit
from play_helpers.ph_keys import PhKeys
from play_helpers.ph_modules import PhModules
from play_helpers.ph_time import PhTime
from play_helpers.ph_util import PhUtil
from play_helpers.test import test_util
from play_helpers.test.ph_constants_test import PhTestConst


def test_version():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading=f'tool_version={PhDefaults.VERSION}')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION)
    PhUtil.print_heading(str_heading='')
    PhUtil.print_version()
    PhUtil.print_heading(str_heading='tool_version=None')
    PhUtil.print_version('Test Tool', None)
    PhUtil.print_heading(str_heading='fetch_tool_version=True')
    PhUtil.print_version(PhModules.PYTHON_HELPERS, PhDefaults.VERSION, fetch_tool_version=True)
    PhUtil.print_heading(str_heading='fetch_tool_version=False')
    PhUtil.print_version(PhModules.PYTHON_HELPERS, PhDefaults.VERSION, fetch_tool_version=False)
    PhUtil.print_heading(str_heading='no_additional_info=True')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, no_additional_info=True)
    PhUtil.print_heading(str_heading='no_additional_info=False')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, no_additional_info=False)
    PhUtil.print_heading(str_heading='with_ip=True')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_ip=True)
    PhUtil.print_heading(str_heading='with_ip=False')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_ip=False)
    PhUtil.print_heading(str_heading='with_git_summary=True')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_git_summary=True)
    PhUtil.print_heading(str_heading='with_git_summary=False')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_git_summary=False)
    PhUtil.print_heading(str_heading='with_git_detailed_info=True')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_git_detailed_info=True)
    PhUtil.print_heading(str_heading='with_git_detailed_info=False')
    PhUtil.print_version('Test Tool', PhDefaults.VERSION, with_git_detailed_info=False)
    PhUtil.print_heading(str_heading='version_parameters_dicts')
    version_parameters_pool = [
        {'tool_name': PhConfigConst.TOOL_NAME, 'tool_version': PhConfigConst.TOOL_VERSION},
        {'tool_name': 'packaging', 'tool_version': None, 'fetch_tool_version': True},
        {'tool_name': 'pandas', 'fetch_tool_version': True},
        {'tool_name': 'psutil', 'fetch_tool_version': True},
        {'tool_name': 'tzlocal', 'fetch_tool_version': True},
        {'tool_name': 'requests', 'fetch_tool_version': True},
        {'tool_name': 'pycryptodome', 'fetch_tool_version': True},
        {'tool_name': 'ruamel.yaml', 'fetch_tool_version': True},
    ]
    PhUtil.print_version(parameters_pool=version_parameters_pool)
    PhUtil.print_heading(str_heading='parameters_pool=version_parameters_pool, get_only=True, dic_format=True')
    PhUtil.print_iter(
        the_iter=PhUtil.print_version(parameters_pool=version_parameters_pool, get_only=True, dic_format=True),
        header='Pool')


def test_misc():
    PhUtil.print_heading()
    print(PhUtil.len_even('123456'))
    print(PhUtil.len_odd('123456'))


def test_list():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='cast_to_list')
    print(PhUtil.to_list(5))
    print(PhUtil.to_list('5'))
    print(PhUtil.to_list('6   ', trim_data=False))
    print(PhUtil.to_list('6   ', trim_data=True))
    print(PhUtil.to_list(['5']))
    print(PhUtil.to_list(None))
    print(PhUtil.to_list([]))
    PhUtil.print_heading(str_heading='extend_list')
    print(PhUtil.extend_list([6], 5))
    print(PhUtil.extend_list(['Pj'], 9))
    print(PhUtil.extend_list(['Pj'], 1))
    print(PhUtil.extend_list(['Pj'], 0))
    print(PhUtil.extend_list([], 5))
    print(PhUtil.extend_list(None, 5))
    print(PhUtil.extend_list(None, 5, filler='Pj'))
    print(PhUtil.extend_list(['Pj', 'Jp'], 5, filler='P'))
    PhUtil.print_heading(str_heading='extend_list, unique')
    print(PhUtil.extend_list([6], 5, unique_entries=True))
    print(PhUtil.extend_list(['Pj'], 9, unique_entries=True))
    print(PhUtil.extend_list(['Pj'], 1, unique_entries=True))
    print(PhUtil.extend_list(['Pj'], 0, unique_entries=True))
    print(PhUtil.extend_list([], 5, unique_entries=True))
    print(PhUtil.extend_list(None, 5, unique_entries=True))
    print(PhUtil.extend_list(None, 5, filler='Pj', unique_entries=True))
    print(PhUtil.extend_list(['Pj', 'Jp'], 5, filler='P', unique_entries=True))
    PhUtil.print_heading(str_heading='extend_list, unique, trim data')
    print(PhUtil.extend_list([' Pj', 'Jp '], 5, filler='P', unique_entries=True, trim_data=True))
    print(PhUtil.extend_list([' Pj', 'Jp '], 5, filler='P', unique_entries=True, trim_data=False))
    print(PhUtil.extend_list([' Pj', 'Jp '], 5, filler=' P', unique_entries=True, trim_data=True))
    print(PhUtil.extend_list([' Pj', 'Jp '], 5, filler=' P', unique_entries=True, trim_data=False))
    PhUtil.print_heading(str_heading='combine_list_items')
    print(PhUtil.combine_list_items(['Pj', 'Lp', ' nn'], trim_data=True))
    print(PhUtil.combine_list_items(['Pj', 'Lp', ' nn'], trim_data=False))
    print(PhUtil.combine_list_items('Pj'))
    PhUtil.print_heading(str_heading='combine_list_items ; clean_data=False')
    print(PhUtil.combine_list_items([';Pj ', 'Lp', 'nn'], clean_data=False))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp', 'nn'], clean_data=False))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp;', 'nn'], clean_data=False))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp;', 'nn;'], clean_data=False))
    print(PhUtil.combine_list_items(['Pj; ', '   ; Lp;', 'nn'], clean_data=False))
    print(PhUtil.combine_list_items(['P;j; ', 'Lp;', 'nn'], clean_data=False))
    print(PhUtil.combine_list_items(['# BulkMode; DirectoryInput; YmlInput; .YmlFiles;', '(3 Elements)'],
                                    clean_data=False))
    print(PhUtil.combine_list_items(['Pj;'], clean_data=False))
    print(PhUtil.combine_list_items(['Remarks semi colon 1;', 'Remarks semi colon 2; '], clean_data=False))
    print(PhUtil.combine_list_items(['Remarks semi colon 1;', 'Remarks semi colon 2; ; '], clean_data=False))
    PhUtil.print_heading(str_heading='combine_list_items ; clean_data=True')
    print(PhUtil.combine_list_items([';Pj ', 'Lp', 'nn'], clean_data=True))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp', 'nn'], clean_data=True))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp;', 'nn'], clean_data=True))
    print(PhUtil.combine_list_items(['Pj; ', 'Lp;', 'nn;'], clean_data=True))
    print(PhUtil.combine_list_items(['Pj; ', '   ; Lp;', 'nn'], clean_data=True))
    print(PhUtil.combine_list_items(['P;j; ', 'Lp;', 'nn'], clean_data=True))
    print(PhUtil.combine_list_items(['# BulkMode; DirectoryInput; YmlInput; .YmlFiles;', '(3 Elements)'],
                                    clean_data=True))
    print(PhUtil.combine_list_items(['Pj;'], clean_data=True))
    print(PhUtil.combine_list_items(['Remarks semi colon 1;', 'Remarks semi colon 2; '], clean_data=True))
    print(PhUtil.combine_list_items(['Remarks semi colon 1;', 'Remarks semi colon 2; ; '], clean_data=True))
    print(PhUtil.combine_list_items([5, 6, 7], clean_data=True))


def test_heading():
    PhUtil.print_heading()
    PhUtil.print_heading(
        str_heading=r'..\..\Data\UserData\GSMA\SGP_22\v3_0_0\UpdateMetadataRequest\DerInput_Asn1Output_DirectInput_Asn1Element_UpdateMetadataRequest_ExportKeyword_OutputFile_export.yml')
    PhUtil.print_heading(
        str_heading='This is a long dataaaa for the testing of Trimming of remarks of individual item of the pool in asn play.; Item 100')
    PhUtil.print_heading(
        str_heading='This is a long dataaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.; Item 100')
    PhUtil.print_heading(
        str_heading='This is a long dataaaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.; Item 100')
    PhUtil.print_heading(
        str_heading='This is a long dataaaaaaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.; Item 100')
    PhUtil.print_heading(
        str_heading='This is a long dataaaaaaaaaaaaaaaaaaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.; Item 100')


def test_python_friendly_name():
    PhUtil.print_heading()
    print(PhUtil.get_python_friendly_name(
        'Error ruamel.yaml.representer.RepresenterError: cannot represent an object: <ProfileInfoListResponse (CHOICE)>...'))
    print(PhUtil.get_python_friendly_name(
        'Error ruamel.yaml.representer.RepresenterError: cannot represent an object: <ProfileInfoListResponse (CHOICE)>...; item 1'))
    print(PhUtil.get_python_friendly_name(
        'Error ruamel.yaml.representer.RepresenterError: cannot represent an object: <ProfileInfoListResponse (CHOICE)>'))
    print(PhUtil.get_python_friendly_name('#userInput'))
    print(PhUtil.get_python_friendly_name('userInput#'))
    print(PhUtil.get_python_friendly_name('#userInput#'))


def test_remarks_append_post():
    PhUtil.print_heading()
    print(PhUtil.append_remarks('StoreMetadataRequest',
                                '..\\..\\Data\\SampleData\\GSMA\\SGP_22\\v3_0_0\\StoreMetadataRequest\\StoreMetadataRequest_wo_icon.hex'))
    print(PhUtil.append_remarks('StoreMetadataRequest',
                                '..\\..\\Data\\SampleData\\GSMA\\SGP_22\\v3_0_0\\StoreMetadataRequest\\StoreMetadataRequest_Mandatory.hex'))
    print(PhUtil.append_remarks('StoreMetadataRequest',
                                'BF2581885A0A989209012143658709F591095350204E616D652031921A4F7065726174696F6E616C2050726F66696C65204E616D652031930101B621301F800204F0811974657374736D6470706C7573312E6578616D706C652E636F6DB705800392F91899020640BF220F300D8003883710A1060404C1020304BF230F300D8003883711A106040402020202'))
    print(PhUtil.append_remarks('',
                                'StoreMetadataRequest; BF2581885A0A989209012143658709F591095350204E616D652031921A4F7065726174696F6E616C2050726F66696C6...'))
    print(PhUtil.append_remarks(
        'StoreMetadataRequest; BF2581885A0A989209012143658709F591095350204E616D652031921A4F7065726174696F6E616C2050726F66696C6...',
        ''))
    print(PhUtil.append_remarks('',
                                'BF2581885A0A989209012143658709F591095350204E616D652031921A4F7065726174696F6E616C2050726F66696C65204E616D652031930101B621301F800204F0811974657374736D6470706C7573312E6578616D706C652E636F6DB705800392F91899020640BF220F300D8003883710A1060404C1020304BF230F300D8003883711A106040402020202'))
    print(PhUtil.append_remarks(
        'BF2581885A0A989209012143658709F591095350204E616D652031921A4F7065726174696F6E616C2050726F66696C65204E616D652031930101B621301F800204F0811974657374736D6470706C7573312E6578616D706C652E636F6DB705800392F91899020640BF220F300D8003883710A1060404C1020304BF230F300D8003883711A106040402020202'))
    print(PhUtil.append_remarks('', 'item 100'))
    print(PhUtil.append_remarks('T', 'item 100'))
    print(PhUtil.append_remarks(
        'This is a long data for the testing of Trimming of remarks of individual item of the pool in asn play.',
        'item 100'))
    for i in range(1, 120):
        print(PhUtil.append_remarks(
            'a' * i + ' This is a long data for the testing of Trimming of remarks of individual item of the pool in asn play.',
            'item 100'))
        i = i + 1
    print(PhUtil.append_remarks(
        'This is a long dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.',
        'item 100'))


def test_remarks_append_pre():
    PhUtil.print_heading()
    print(PhUtil.append_remarks('item 100', '', append_mode_post=False))
    print(PhUtil.append_remarks('item 100', 'T', append_mode_post=False))
    print(PhUtil.append_remarks(
        'item 100',
        'This is a long data for the testing of Trimming of remarks of individual item of the pool in asn play.',
        append_mode_post=False
    ))
    for i in range(1, 120):
        print(PhUtil.append_remarks(
            'item 100',
            'a' * i + ' This is a long data for the testing of Trimming of remarks of individual item of the pool in asn play.',
            append_mode_post=False
        ))
        i = i + 1
    print(PhUtil.append_remarks(
        'item 100',
        'This is a long dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa for the testing of Trimming of remarks of individual item of the pool in asn play.',
        append_mode_post=False))
    for i in range(1, 120):
        print(PhUtil.append_remarks(
            'item 100' + '0' * i,
            ' This is a long data for the testing of Trimming of remarks of individual item of the pool in asn play.',
            append_mode_post=False
        ))
        i = i + 1


def test_temp():
    PhUtil.print_heading()


def test_hash():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='hash_algos_list')
    print(PhCrypto.hash_algos_list())
    msg = 'First'
    PhUtil.print_heading(str_heading='Str hash')
    print(f'Input String: {msg}; hash_str_sha256: {PhCrypto.hash_str_sha256(msg=msg)}')
    print(f'Input String: {msg}; hash_str: {PhCrypto.hash_str(msg=msg)}')
    print(f'Input String: {msg}; hash_str(hash_algo=sha512) {PhCrypto.hash_str(msg=msg, hash_algo="sha512")}')


def test_get_git_info():
    PhUtil.print_heading()
    PhUtil.print_heading('get_git_info_detailed; GIT_SUMMARY')
    print(f'GIT_SUMMARY: {PhGit.get_git_info_detailed(key=PhGit.KEY_GIT_SUMMARY)}')
    PhUtil.print_heading('get_git_info_detailed')
    print(PhGit.get_git_info_detailed())
    PhUtil.print_heading('get_git_info_detailed iter')
    PhUtil.print_iter(PhGit.get_git_info_detailed())


def test_get_time_stamp_file_name():
    PhUtil.print_heading()
    outputs = []
    for _ in range(15):
        data = PhUtil.get_time_stamp(files_format=True)
        print(f'{data[:13]} {data[13:15]} {data[15:]}')
    for _ in range(500):
        outputs.append(PhUtil.get_time_stamp(files_format=True))
    dup_list = [x for x in outputs if outputs.count(x) > 1]
    PhUtil.print_iter(dup_list, header='Duplicate Items')


def test_to_file():
    PhUtil.print_heading()
    PhUtil.to_file(output_lines='abc', file_name='abc.txt')
    PhUtil.to_file(output_lines='abc', file_name=os.sep.join([PhUtil.path_default_data_folder, 'abc.txt']))
    PhUtil.to_file(output_lines='abc', file_name=os.sep.join([PhUtil.path_default_data_folder, 'abc.list']))
    PhUtil.to_file(output_lines='abc', file_name=os.sep.join([PhUtil.path_default_data_folder, 'abc.ini']))
    PhUtil.to_file(output_lines=['abc', 'def', 'ghi'],
                   file_name=os.sep.join([PhUtil.path_default_data_folder, 'abc_list.txt']))
    PhUtil.to_file(output_lines='abc', back_up_file=True)
    PhUtil.to_file(output_lines='abc', file_name=os.sep.join([PhUtil.path_default_bkp_folder, 'a_b_c.txt']),
                   back_up_file=True)
    PhUtil.to_file(output_lines='abc', file_name=PhUtil.path_default_bkp_folder, back_up_file=True,
                   file_path_is_dir=True)


def test_print_iter():
    PhUtil.print_heading()
    dic1 = {
        'raw_data': '',
        'input_format': 'url',
        'remarks_list': '',
        'sample_data': 'AmenityPj',
        'sample_option': 'Load Only',
        'sample_process': '',
    }
    dic2 = {
        'app_title': '',
        'app_description': 'url',
        'app_version': '',
        'app_github_url': 'AmenityPj',
        'app_github_pages_url': 'Load Only',
    }
    dic3 = {
        '1': dic1,
        '2': dic2,
    }
    dic4 = {}
    dic5 = {'app_title': ''}
    list1 = ['raw_data', 'input_format', 'remarks_list', 'sample_data', 'sample_option', 'sample_process']
    list2 = ['app_title', 'app_description', 'app_version', 'app_github_url', 'app_github_pages_url']
    list3 = [list1, list2]
    list4 = []
    list5 = ['app_title']
    ordered_dic1 = OrderedDict()
    ordered_dic1.update({'dic1': dic1})
    ordered_dic1.update({'dic2': dic2})
    ordered_dic1.update({'dic3': dic3})
    sep = PhConstants.SEPERATOR_MULTI_OBJ
    list_of_items = [
        [dic1, 'dic1'],
        [dic2, 'dic2'],
        [dic3, 'dic3'],
        [dic4, 'dic4'],
        [dic5, 'dic5'],
        [list1, 'list1'],
        [list2, 'list2'],
        [list3, 'list3'],
        [list4, 'list4'],
        [list5, 'list5'],
        [ordered_dic1, 'orderedDic1'],
    ]

    PhUtil.print_heading(str_heading='Simple Iters')
    PhUtil.print_iter(dic1, header='dic1')
    PhUtil.print_iter(list1, header='list1')
    PhUtil.print_iter(list1, header='list1; list_as_str=True', list_as_str=True)

    PhUtil.print_heading(str_heading='iters printing with heading')
    for item in list_of_items:
        actual_iter = item[0]
        header = item[1]
        PhUtil.print_iter(actual_iter, header=header)

    PhUtil.print_heading(str_heading='iters printing')
    for item in list_of_items:
        PhUtil.print_iter(item[0])

    PhUtil.print_heading(str_heading='iters printing; depth_level=1')
    for item in list_of_items:
        PhUtil.print_iter(item[0], depth_level=1)

    PhUtil.print_heading(str_heading='iters printing, with sep')
    for item in list_of_items:
        PhUtil.print_iter(item[0], sep=sep)

    data = sys.modules
    PhUtil.print_heading(str_heading='sys.modules; depth_level=0')
    PhUtil.print_iter(data, depth_level=0)
    PhUtil.print_heading(str_heading='sys.modules; check_for_dict_attribute=False')
    PhUtil.print_iter(data, check_for_dict_attribute=False)
    # TODO: https://pratikj.atlassian.net/browse/SML-398
    # PhUtil.print_heading(str_heading='sys.modules')
    # PhUtil.print_iter(data)

    PhUtil.print_heading(str_heading='class')
    PhUtil.print_iter(PhConstants)

    PhUtil.print_heading(str_heading='enum')
    PhUtil.print_iter(PhConstants.Position)

    PhUtil.print_heading(str_heading='enum item')
    PhUtil.print_iter(PhConstants.Position.TOP)

    PhUtil.print_heading(str_heading='dict with enum')
    dic_w_enum = {
        'app_title': '',
        'app_description': 'url',
        'app_version': '',
        'app_github_url': 'AmenityPj',
        'app_github_pages_url': 'Load Only',
        'position': PhConstants.Position.TOP,
        'items': PhConstants.Position,
    }
    PhUtil.print_iter(dic_w_enum)


def test_obj_list():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='cls_to_explore=PhUtil')
    PhUtil.get_obj_list(cls_to_explore=PhUtil, print_also=True)
    PhUtil.print_heading(str_heading="cls_to_explore=PhUtil, obj_name_filter='print'")
    PhUtil.get_obj_list(cls_to_explore=PhUtil, obj_name_filter='print', print_also=True)
    PhUtil.print_heading(str_heading='cls_to_explore=play_helpers')
    PhUtil.get_obj_list(cls_to_explore=play_helpers, print_also=True)
    PhUtil.print_heading(str_heading="cls_to_explore=play_helpers, obj_name_filter='ph'")
    PhUtil.get_obj_list(cls_to_explore=play_helpers, obj_name_filter='ph', print_also=True)


def test_get_classes_list():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='module_to_explore=play_helpers.ph_util')
    PhUtil.get_classes_list(module_to_explore=play_helpers.ph_util, print_also=True)
    PhUtil.print_heading(str_heading='module_to_explore=play_helpers.ph_util, obj_name_needed=False')
    PhUtil.get_classes_list(module_to_explore=play_helpers.ph_util, obj_name_needed=False, print_also=True)
    PhUtil.print_heading(str_heading='module_to_explore=test_util')
    PhUtil.get_classes_list(module_to_explore=test_util, print_also=True)
    PhUtil.print_heading(str_heading='module_to_explore=test_util, parent_class=unittest.TestCase')
    PhUtil.get_classes_list(module_to_explore=test_util, parent_class=unittest.TestCase, print_also=True)


def test_print_modules():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='No filter String')
    PhUtil.print_modules()
    PhUtil.print_heading(str_heading="filter_string='play_helpers'")
    PhUtil.print_modules(filter_string='play_helpers')


def test_generalise_list():
    PhUtil.print_heading()
    list1 = [1, 2, 3, 4, 5]
    PhUtil.print_iter(list1, header='list1')
    generalise_list = PhUtil.generalise_list(list1)
    PhUtil.print_iter(generalise_list, header='generalise_list')
    generalise_list_rev = PhUtil.generalise_list_reverse(generalise_list)
    PhUtil.print_iter(generalise_list_rev, header='generalise_list_rev')
    list1_rev = PhUtil.generalise_list_reverse(list1)
    PhUtil.print_iter(list1_rev, header='list1_rev')
    generalise_list_append_others = PhUtil.generalise_list(list1, append_others=True)
    PhUtil.print_iter(generalise_list_append_others, header='generalise_list_append_others')
    generalise_list_append_others_rev = PhUtil.generalise_list_reverse(generalise_list_append_others)
    PhUtil.print_iter(generalise_list_append_others_rev, header='generalise_list_append_others_rev')


def test_zipfile():
    PhUtil.print_heading()
    source_files_dir = PhUtil.path_default_data_folder
    target_dir = PhUtil.path_default_res_folder
    PhUtil.print_heading(str_heading='keep_source_dir_in_zip=True')
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir, target_dir=target_dir, keep_source_dir_in_zip=True,
                             target_file_name_wo_extn='test_zipfile_keep_source_dir_in_zip_true')
    PhUtil.print_heading(str_heading='keep_source_dir_in_zip=False')
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir, target_dir=target_dir, keep_source_dir_in_zip=False,
                             target_file_name_wo_extn='test_zipfile_keep_source_dir_in_zip_false')
    PhUtil.print_heading(str_heading='source_files_dir=target_dir')
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir, target_dir=source_files_dir,
                             target_file_name_wo_extn='test_zipfile_keep_source_path_is_dest_path')
    PhUtil.print_heading(str_heading='source_files_and_target_dir')
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir, target_dir=target_dir)
    PhUtil.print_heading(str_heading='only_source_files')
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir)
    PhUtil.print_heading(str_heading='source_dir_custom_extn_files')
    file_list = ['*.txt']
    PhUtil.zip_and_clean_dir(source_files_dir=source_files_dir, include_files=file_list,
                             target_file_name_wo_extn='test_zipfile_source_dir_custom_extn_files')


def test_chars_to_utf8():
    PhUtil.print_heading()
    target_file_name = 'test_chars_to_utf8.asn'
    lines = []
    for encoding in PhConstants.CHAR_ENCODING_POOL:
        PhUtil.print_heading(f'encoding: {encoding}')
        with open(os.sep.join([PhUtil.path_default_res_folder, target_file_name]),
                  encoding=encoding, errors=PhDefaults.CHAR_ENCODING_ERRORS) as f:
            lines = f.readlines()
        for input_data in lines:
            output_data = PhUtil.all_chars_to_utf8(input_data)
            data = PhConstants.SEPERATOR_MULTI_LINE_TABBED.join(
                [f'input_data: {input_data}', f'output_data: {output_data}'])
            print(data)


def test_traverse_it():
    PhUtil.print_heading()
    """
    Test Data
    """
    #
    target_file1_name = PhTestConst.SRC_CODE_PH_BITS_FILE_NAME
    target_file2_name = PhTestConst.SRC_CODE_PH_CONSTANTS_FILE_NAME
    target_file3_name = PhTestConst.SRC_CODE_PH_DATA_MASTER_FILE_NAME
    target_file1_name_star_w_ext = 'ph_bit*.py'
    target_file2_name_star_w_ext = 'ph_constant*.py'
    target_file3_name_star_w_ext = 'ph_data_*.py'
    target_file1_name_star_wo_ext = 'ph_bit*'
    target_file2_name_star_wo_ext = 'ph_constant*'
    target_file3_name_star_wo_ext = 'ph_data_*'
    target_file1_path = PhTestConst.SRC_CODE_PH_BITS_FILE_PATH
    target_file2_path = PhTestConst.SRC_CODE_PH_CONSTANTS_FILE_PATH
    target_file3_path = PhTestConst.SRC_CODE_PH_DATA_MASTER_FILE_PATH
    target_dir_name = PhTestConst.SRC_CODE_TEST_DIR_NAME
    target_dir_path = PhTestConst.SRC_CODE_TEST_DIR_PATH
    #
    src_dir_rel = os.sep.join([PhUtil.path_current_folder, os.pardir])
    src_dir = PhUtil.get_absolute_path(src_dir_rel)
    src_file_nok = target_file1_path
    #
    inc_files_pattern1_ok = '*.py'
    inc_files_pattern2_ok = '*__.py'
    inc_files_pattern_nok = ['*_*.py']
    inc_files_pattern_dual_ok = ['*.py', '*.txt']
    #
    inc_files_name_nok = target_file1_name
    inc_files_name_pattern_ok = '*' + target_file1_name
    inc_files_names_pattern_multi_ok = [
        '*' + target_file1_name,
        '*' + target_file2_name,
        '*' + target_file3_name
    ]
    inc_files_name_pattern_star_w_ext_ok = '*' + target_file1_name_star_w_ext
    inc_files_name_pattern_star_wo_ext_ok = '*' + target_file1_name_star_wo_ext
    inc_files_name_pattern_star_w_ext_multi_ok = [
        '*' + target_file1_name_star_w_ext,
        '*' + target_file2_name_star_w_ext,
        '*' + target_file3_name_star_w_ext
    ]
    inc_files_name_pattern_star_wo_ext_multi_ok = [
        '*' + target_file1_name_star_wo_ext,
        '*' + target_file2_name_star_wo_ext,
        '*' + target_file3_name_star_wo_ext
    ]
    #
    inc_files_path_ok = target_file1_path
    inc_files_path_multi_ok = [target_file1_path, target_file2_path, target_file3_path]
    inc_files_path_pattern_ok = '*' + target_file1_path
    inc_files_path_pattern_multi_ok = ['*' + target_file1_path, '*' + target_file2_path, '*' + target_file3_path]
    #
    exc_file_name_nok = target_file1_name
    exc_dir_name_nok = target_dir_name
    exc_file_path_ok = target_file1_path
    exc_dir_path_ok = target_dir_path
    #
    exc_files_pattern_ok = '*.pyc'
    """
    Test Cases
    """
    #
    PhUtil.print_heading(str_heading='No Args; Working')
    PhUtil.traverse_it(print_also=True)
    #
    PhUtil.print_heading(str_heading='include_files=inc_files_pattern_dual_ok')
    PhUtil.traverse_it(print_also=True, include_files=inc_files_pattern_dual_ok)
    #
    PhUtil.print_heading(str_heading='src_dir_rel')
    PhUtil.traverse_it(print_also=True, top=src_dir_rel)
    #
    PhUtil.print_heading(str_heading='src_dir_rel, include_files=inc_files_pattern1_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir_rel, include_files=inc_files_pattern1_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_pattern1_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_pattern1_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_pattern2_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_pattern2_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_pattern_nok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_pattern_nok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_nok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_nok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_pattern_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_names_pattern_multi_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_names_pattern_multi_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_pattern_star_w_ext_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_star_w_ext_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_pattern_star_w_ext_multi_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_star_w_ext_multi_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_pattern_star_wo_ext')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_star_wo_ext_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_name_pattern_star_wo_ext_multi_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_star_wo_ext_multi_ok)
    #
    PhUtil.print_heading(
        str_heading='src_dir, include_files=inc_files_name_pattern_star_wo_ext_multi_ok, excludes=exc_files_pattern_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_name_pattern_star_wo_ext_multi_ok,
                       excludes=exc_files_pattern_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_path_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_path_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_path_multi_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_path_multi_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_path_pattern_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_path_pattern_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, include_files=inc_files_path_pattern_multi_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, include_files=inc_files_path_pattern_multi_ok)
    #
    PhUtil.print_heading(str_heading='src_file_nok, include_files=inc_files_pattern1_ok')
    PhUtil.traverse_it(print_also=True, top=src_file_nok, include_files=inc_files_pattern1_ok)
    #
    PhUtil.print_heading(str_heading='src_file_nok')
    PhUtil.traverse_it(print_also=True, top=src_file_nok)
    #
    PhUtil.print_heading(str_heading='src_dir, excludes=exc_file_name_nok')
    PhUtil.traverse_it(print_also=True, top=src_dir, excludes=exc_file_name_nok)
    #
    PhUtil.print_heading(str_heading='src_dir, excludes=exc_dir_name_nok')
    PhUtil.traverse_it(print_also=True, top=src_dir, excludes=exc_dir_name_nok)
    #
    PhUtil.print_heading(str_heading='src_dir, excludes=exc_file_path_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, excludes=exc_file_path_ok)
    #
    PhUtil.print_heading(str_heading='src_dir, excludes=exc_dir_path_ok')
    PhUtil.traverse_it(print_also=True, top=src_dir, excludes=exc_dir_path_ok)


def test_eid():
    PhUtil.print_heading()
    eid_pool = [
        '89049032007008882600117893640261',
        '89049032123451234512345678901235',
    ]
    for eid in eid_pool:
        print(f'EID {eid} is Valid ? {PhCrypto.validate_eid(eid)}')


def test_luhn():
    PhUtil.print_heading()
    PhUtil.print_heading(str_heading='debit_card_pool')
    debit_card_pool = [
        '4722 5410 5101 6295',
    ]
    for debit_card in debit_card_pool:
        print(f'Debit Card {debit_card} is Valid ? {PhCrypto.validate_luhn_digit(debit_card)}')
    PhUtil.print_heading(str_heading='credit_card_pool')
    credit_card_pool = [
        '4386 2800 2898 6424',
    ]
    for cebit_card in credit_card_pool:
        print(f'Cebit Card {cebit_card} is Valid ? {PhCrypto.validate_luhn_digit(cebit_card)}')
    PhUtil.print_heading(str_heading='iccid_pool')
    iccid_pool = [
        '894461721200000114',
        '8944617212000001146',
        '89423 10220 00089 671 6',
    ]
    for iccid in iccid_pool:
        print(f'ICCID {iccid} is Valid ? {PhCrypto.validate_luhn_digit(iccid)}')
    PhUtil.print_heading(str_heading='imei_pool')
    imei_pool = [
        '501944690893758',
        '910107118819392',
        '502652252218376',
    ]
    for imei in imei_pool:
        print(f'imei {imei} is Valid ? {PhCrypto.validate_luhn_digit(imei)}')


def test_handle_dirs():
    PhUtil.print_heading()
    PhUtil.print_heading('quite_mode=True; Default')
    PhUtil.make_dirs(dir_path='sample1')
    PhUtil.remove_dirs(dir_path='sample1')
    PhUtil.print_heading('quite_mode=False')
    PhUtil.make_dirs(dir_path='sample2', quite_mode=False)
    PhUtil.remove_dirs(dir_path='sample2', quite_mode=False)


def test_normalise_list():
    PhUtil.print_heading()
    data = [1, 2, 3, 4, 5, [6, 7, 8], 9]
    for x in range(5):
        res = PhUtil.normalise_list(data)
        PhUtil.print(res)


def test_time_delay(ph_time):
    ph_time.print()
    time.sleep(5)
    ph_time.print()


def test_doc_string():
    PhUtil.print_heading()
    func = PhCrypto.hash_str
    PhUtil.print_heading('help')
    help(func)
    PhUtil.print_heading('__doc__')
    print(func.__doc__)


def test_get_help_for_param():
    PhUtil.print_heading()
    PhUtil.print(PhUtil.get_help_for_param('Sample Param'))
    PhUtil.print(PhUtil.get_help_for_param('Sample Param with Valid Default Value', '5'))
    PhUtil.print(
        PhUtil.get_help_for_param('Sample Param with None Default Value; include_none=False', None, include_none=False))
    PhUtil.print(
        PhUtil.get_help_for_param('Sample Param with None Default Value; include_none=True', None, include_none=True))


def test_parse_config():
    PhUtil.print_heading()
    test_data_set = [
        {
            'remarks': 'Simple Data Types',
            'remarks_str01': 'Simple Data Types',
            'remarks_str02': ' Simple Data Types ',
            'remarks_str03': "  Simple Data Types  ",
            'remarks_str04': '"    Simple Data Types  "  ',
            'remarks_str05': '   """Simple Data Types  """',
            'remarks_str06': " '     Simple Data Types ' ",
            'remarks_str07': '86020102',
            'remarks_str08': 'False',
            'remarks_str09': 'True',
            'remarks_str0A': '86020102.0',
            'remarks_str0B': 'None',
            'item_s01': 'False',
            'item_s02': False,
            'item_s03': 'false',
            'item_s04': 'Fals e',
            'item_s05': 'FaLse',
            'item_s06': 'False ',
            'item_s07': ' False ',
            'item_s08': '"False"',
            'item_s11': 'True',
            'item_s12': True,
            'item_s13': 'true',
            'item_s14': 'Tr ue',
            'item_s15': 'TruE',
            'item_s16': 'True ',
            'item_s17': '   True ',
            'item_s18': '"True"',
            'item_s21': 'yes',
            'item_s22': 'Yes',
            'item_s23': 'no',
            'item_s24': 'No',
            'item_s25': ' ',
            'item_s26': "",
            'item_s27': """""",
            'item_s31': '86020102',
            'item_s32': '086020102',
            'item_s33': '8 6020102',
            'item_s34': '860201020 ',
            'item_s35': '   860201020 ',
            'item_s36': '86020102.0',
            'item_s37': '86020102.0 ',
            'item_s38': """
                            86020102.0
                        """,
            'item_s39': '86020102.064654767',
            'item_s3A': "'86020102'",
            'item_s3B': '"86020102"',
            'item_s41': 'none',
            'item_s42': None,
            'item_s43': 'None',
            'item_s44': 'NONE',
        },
        {
            'remarks': 'Complex Data Types',
            'item_c1': "[{'brown': 'black'}, {'dog': 'cattttttt'}]",
            'item_c2': [{'brown': 'black'}, {'dog': 'cattttttt'}],
            'item_c3': '[]',
            'item_c4': [],
            'item_c5': "{1: {'brown': 'black'},2: {'dog': 'cattttttt'}}",
            'item_c6': {1: {'brown': 'black'}, 2: {'dog': 'cattttttt'}},
            'item_c7': '{}',
            'item_c8': {},
        },
    ]
    remarks_exclude = [int, float, bool]
    for test_data in test_data_set:
        PhUtil.print_heading(test_data.get(PhKeys.REMARKS))
        PhUtil.print_iter(the_iter=test_data, verbose=True, header='Before')
        new_config = PhUtil.dict_to_data(copy.copy(test_data))
        PhUtil.print_iter(the_iter=new_config, verbose=True, header='After')
        # Prepare Exclude
        exclude_data = {}
        for key in test_data:
            if key.startswith('remarks_str'):
                exclude_data.update({key: remarks_exclude})
        new_config = PhUtil.dict_to_data(copy.copy(test_data), data_types_exclude=exclude_data)
        PhUtil.print_iter(the_iter=new_config, verbose=True, header='After Exclude')


def test_expired_attr():
    PhUtil.print_heading()
    # TODO: This does not work as expected, check implementation in Numpy
    # makedirs()


def test_trim_white_spaces_in_str():
    PhUtil.print_heading()
    input_data_set = [
        '       ',
        ' rgdrg  rtert',
        ' rgdrg                          rtert',
        """   rgdrg                      rte
            rt""",
        '\85',
        '\85 ',
        '\x85',
        ' \85 ',
    ]
    for input_data in input_data_set:
        output_data_trim_white_spaces_in_str = PhUtil.trim_white_spaces_in_str(input_data)
        output_data_trim_and_kill_all_white_spaces = PhUtil.trim_and_kill_all_white_spaces(input_data)
        output_data_trim_and_kill_extra_white_spaces = PhUtil.trim_and_kill_extra_white_spaces(input_data)
        PhUtil.print_input_output(
            input_data=input_data,
            output_data=
            [
                output_data_trim_white_spaces_in_str,
                output_data_trim_and_kill_all_white_spaces,
                output_data_trim_and_kill_extra_white_spaces
            ],
            output_remarks=
            ['trim_white_spaces_in_str        ',
             'trim_and_kill_all_white_spaces  ',
             'trim_and_kill_extra_white_spaces',
             ],
            input_remark
            ='input Data                      ',
            verbose=True,
        )


def test_last_modification_time():
    PhUtil.print_heading()
    path_current_script = __file__
    name_current_script = os.path.basename(__file__)
    input_data_set = [
        PhTestConst.SRC_CODES_PH_FILES_PATHS,
        PhTestConst.SRC_CODE_TEST_DIR_PATH,
        PhUtil.path_current_folder,
        path_current_script,
        name_current_script,
    ]
    for input_data in PhUtil.normalise_list(input_data_set):
        print(f'{input_data}: {PhUtil.last_modification_time(file_or_folder_path=input_data)}')


def test_generate_test_data():
    PhUtil.print_heading()
    #
    sep = PhConstants.SEPERATOR_MULTI_LINE
    input_data_set = [
        0,
        1,
        -5,
        5,
        226,
        227,
        228,
        229,
        14765,
    ]
    for input_data in input_data_set:
        PhUtil.print_heading(f'require_length={input_data}')
        test_data = PhUtil.generate_test_data(require_length=input_data)
        PhUtil.get_key_value_pair(key='Test Data', value=test_data, sep=sep, print_also=True)
        PhUtil.get_key_value_pair(key='Test Data', value=test_data, print_also=True, length_needed=True)


def test_functions(ph_time):
    """

    :param ph_time:
    :return:
    """
    test_temp()
    ## Keep on the 2nd Number
    ##
    test_version()
    test_parse_config()
    test_expired_attr()
    test_doc_string()
    test_get_help_for_param()
    test_chars_to_utf8()
    test_get_git_info()
    test_get_time_stamp_file_name()
    test_to_file()
    test_misc()
    test_list()
    test_heading()
    test_python_friendly_name()
    test_remarks_append_post()
    test_remarks_append_pre()
    test_print_modules()
    test_print_iter()
    test_obj_list()
    test_get_classes_list()
    test_generalise_list()
    test_hash()
    test_zipfile()
    test_traverse_it()
    test_eid()
    test_luhn()
    test_normalise_list()
    test_handle_dirs()
    test_generate_test_data()
    test_trim_white_spaces_in_str()
    test_last_modification_time()
    ##
    ## Keep on last
    test_time_delay(ph_time)


def main():
    """

    :return:
    """
    """
    Time Object
    """
    ph_time = PhTime()
    ph_time.start()
    """
    Process
    """
    # Temp Test Cases
    # test_last_modification_time()
    # Regular Test Cases
    test_functions(ph_time)
    # test_print_iter()
    """
    Wrap up 
    """
    ph_time.stop()
    ph_time.print()
    PhUtil.print_done()


if __name__ == '__main__':
    main()
