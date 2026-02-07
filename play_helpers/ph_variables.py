from play_helpers.ph_keys import PhKeys


class PhVariables:
    #####################
    # asn1Play
    INPUT_FORMAT = f'${PhKeys.INPUT_FORMAT}'
    OUTPUT_FORMAT = f'${PhKeys.OUTPUT_FORMAT}'
    ASN1_ELEMENT = f'${PhKeys.ASN1_ELEMENT}'
    TLV_PARSING_OF_OUTPUT = f'${PhKeys.TLV_PARSING_OF_OUTPUT}'
    RE_PARSE_OUTPUT = f'${PhKeys.RE_PARSE_OUTPUT}'

    # asn1Play Web

    # asn1

    # asn1 Web

    # tlvPlay
    LENGTH_IN_DECIMAL = f'${PhKeys.LENGTH_IN_DECIMAL}'
    VALUE_IN_ASCII = f'${PhKeys.VALUE_IN_ASCII}'
    ONE_LINER = f'${PhKeys.ONE_LINER}'
    NON_TLV_NEIGHBOR = f'${PhKeys.NON_TLV_NEIGHBOR}'

    # qrPlay
    # OUTPUT_FORMAT = f'${PhKeys.OUTPUT_FORMAT}'
    SIZE = f'${PhKeys.SIZE}'
    QR_CODE_VERSION = f'${PhKeys.QR_CODE_VERSION}'
    SPLIT_QRS = f'${PhKeys.SPLIT_QRS}'
    DECORATE_QR = f'${PhKeys.DECORATE_QR}'
    LABEL = f'${PhKeys.LABEL}'
    LABEL_POSITION = f'${PhKeys.LABEL_POSITION}'

    # qrPlay Web

    # certPlay
    INPUT_FORMAT = f'${PhKeys.INPUT_FORMAT}'
    URL_TIME_OUT = f'${PhKeys.URL_TIME_OUT}'
    URL_PRE_ACCESS = f'${PhKeys.URL_PRE_ACCESS}'
    URL_CERT_FETCH_ONLY = f'${PhKeys.URL_CERT_FETCH_ONLY}'
    URL_ALL_CERTS = f'${PhKeys.URL_ALL_CERTS}'

    # certPlay Web

    # dataPlay
    CONTENT_MAPPINGS = f'${PhKeys.CONTENT_MAPPINGS}'
    NAME_MAPPINGS = f'${PhKeys.NAME_MAPPINGS}'

    #####################
    VERSION = f'${PhKeys.VERSION}'
    REMARKS = f'${PhKeys.REMARKS}'
    ITEM_INDEX = '$ITEM_INDEX'
    KEY_NAME = '$KEY_NAME'
