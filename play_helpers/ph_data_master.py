from play_helpers.ph_constants import PhConstants
from play_helpers.ph_exception_helper import PhExceptionHelper


class PhMasterDataKeys:
    DATA = 'data'
    META_DATA = 'meta_data'
    INFO_DATA = 'info_data'
    ERROR_DATA = 'error_data'


class PhMasterData:
    """

    """

    def __init__(self, data=None, meta_data=None, info_data=None, error_data=None):
        """

        :param data:
        :param meta_data:
        :param info_data:
        :param error_data:
        """
        self.master_data = {}
        if data is not None:
            self.master_data.update({PhMasterDataKeys.DATA: data})
        if meta_data is not None:
            self.master_data.update({PhMasterDataKeys.META_DATA: meta_data})
        if info_data is not None:
            self.master_data.update({PhMasterDataKeys.INFO_DATA: info_data})
        if error_data is not None:
            self.master_data.update({PhMasterDataKeys.ERROR_DATA: error_data})

    def set_master_data(self, key, value):
        if key in self.master_data:
            self.master_data[key] = value
        else:
            self.master_data.update({key: value})

    def get_master_data(self, key):
        return self.master_data.get(key, None)

    def get(self):
        return self.master_data

    def get_output_data(self, only_output):
        output_data = PhConstants.STR_EMPTY
        info_data = PhConstants.STR_EMPTY
        meta_data = self.get_master_data(PhMasterDataKeys.META_DATA)
        if meta_data is not None:
            #  MetaData Object is Present
            # if isinstance(meta_data, MetaData):
            output_data = meta_data.get_parsed_data()
            info_data = meta_data.get_info_data()
        error_data = self.get_master_data(PhMasterDataKeys.ERROR_DATA)
        if error_data is not None:
            # ErrorData Object is Present
            output_data = error_data.get_details() if isinstance(error_data, PhExceptionHelper) else error_data
        return output_data if only_output else (output_data, info_data)
