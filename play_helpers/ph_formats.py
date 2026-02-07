class PhFormats:
    TXT = 'txt'
    ASN = 'asn'
    ASN1 = 'asn1'
    BASE_64 = 'base64'
    HEX = 'hex'
    YML = 'yml'
    YAML = 'yaml'
    JSON = 'json'
    IN = 'in'
    OUT = 'out'
    CSV = 'csv'
    XLSX = 'xlsx'
    XLS = 'xls'
    APNG = 'apng'
    PNG = 'png'
    AVIF = 'avif'
    GIF = 'gif'
    SVG = 'svg'
    JPG = 'jpg'
    JPEG = 'jpeg'
    WEBP = 'webp'
    BKP = 'bkp'
    TMP = 'tmp'
    PY = 'py'
    JAVA = 'java'
    _7Z = '7z'
    ZIP = 'zip'
    HASH = 'hash'
    FUNCTION_SPECIFIC = 'function_specific'
    ASN_ORG = 'asn_org'
    ASN_MANUALLY_CORRECTED = 'asn_manually_corrected'
    ASN_AUTO_CORRECTED = 'asn_auto_corrected'
    ASN_FORMATTED = 'asn_formatted'
    PNG_URI = 'png_uri'
    SVG_URI = 'svg_uri'
    URL = 'url'
    DER = 'der'


class PhFormatsGroups:
    ARCHIVE_OUTPUT_FORMATS_SUPPORTED = [
        PhFormats.ZIP,
    ]


class PhMimeTypes:
    """
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types#image_types
    """
    APNG = 'image/apng'
    AVIF = 'image/avif'
    GIF = 'image/gif'
    JPEG = 'image/jpeg'
    PNG = 'image/png'
    SVG = 'image/svg+xml'
    WEBP = 'image/webp'

    format_to_mimetype_mappings = {
        PhFormats.APNG: APNG,
        PhFormats.AVIF: AVIF,
        PhFormats.GIF: GIF,
        PhFormats.JPEG: JPEG,
        PhFormats.JPG: JPEG,
        PhFormats.PNG: PNG,
        PhFormats.SVG: PNG,
        PhFormats.WEBP: WEBP,
    }
