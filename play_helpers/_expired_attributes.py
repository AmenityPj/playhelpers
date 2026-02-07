"""
Dict of expired attributes that are discontinued since x.0 release.
Each item is associated with a migration note and version.

"""

__expired_attributes__ = {
    # Sample Structure
    # 'KEY': {'since': 'VERSION', 'alternate': 'CAN_BE_USED_INSTEAD'},
    # Sample Message
    # ('{KEY} is removed from {SINCE}, use {CAN_BE_USED_INSTEAD} instead !!!')
    # ('set_if_not_none() is removed from v4.4.0, use set_if_none() instead !!!')

    'set_if_not_none': {'since': 'v4.4.0', 'alternate': 'set_if_none'},
    'set_if_not_empty': {'since': 'v4.4.0', 'alternate': 'set_if_empty'},
    'line_is_comment': {'since': 'v5.0.0', 'alternate': 'is_empty_or_comment_string'},
    'line_is_comment_or_empty': {'since': 'v5.0.0', 'alternate': 'is_empty_or_comment_string'},
    'string_is_blank': {'since': 'v5.0.0', 'alternate': 'is_empty_string'},
    'string_is_not_blank': {'since': 'v5.0.0', 'alternate': 'is_not_empty_string'},
    'print_': {'since': 'v5.0.0', 'alternate': 'print'},
    'makedirs': {'since': 'v5.0.0', 'alternate': 'make_dirs'},
    'clean_dirs': {'since': 'v5.0.0', 'alternate': 'clean_dirs'},
    'parse_config': {'since': 'v5.2.0', 'alternate': 'dict_to_data'},

    # copied from np
    # 'seterrobj': 'Use the np.errstate context manager instead.',
    # 'cast': 'Use `np.asarray(arr, dtype=dtype)` instead.',
    # 'source': 'Use `inspect.getsource` instead.',
    # 'set_numeric_ops':
    #     'For the general case, use `PyUFunc_ReplaceLoopBySignature`. '
    #     'For ndarray subclasses, define the ``__array_ufunc__`` method '
    #     'and override the relevant ufunc.',
    # 'PINF': 'Use `np.inf` instead.',
    # 'add_newdoc':
    #     'It\'s still available as `np.lib.add_newdoc`.',
    # 'add_newdoc_ufunc':
    #     'It\'s an internal function and doesn''t have a replacement.',
    # 'compat': 'There\'s no replacement, as Python 2 is no longer supported.',
    # 'NaN': 'Use `np.nan` instead.',
    # 'obj2sctype': 'Use `np.dtype(obj).type` instead.',
    # 'nbytes': 'Use `np.dtype(<dtype>).itemsize` instead.',
}
