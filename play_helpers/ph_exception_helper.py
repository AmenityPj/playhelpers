from play_helpers._common import _PhCommon
from play_helpers.ph_constants import PhConstants


def get_exception_object(e):
    return e.args[0] if len(e.args) > 0 else e


class PhExceptionHelper:
    def __init__(self, msg_key=None, function_name=None, line_num=None, exception=None, msg_value=None,
                 key_value_sep=PhConstants.SEPERATOR_KEY_VALUE, additional_msgs_list=None, summary_msg=None,
                 known=None):
        self.msg_key = msg_key
        self.msg_value = str(msg_value) if msg_value else None
        self.key_value_sep = key_value_sep
        self.summary_msg = summary_msg
        self.known = known
        if additional_msgs_list:
            if not isinstance(additional_msgs_list, list):
                additional_msgs_list = [additional_msgs_list]
        self.additional_msgs_list = additional_msgs_list
        self.function_name = function_name
        self.line_num = line_num
        self.exception = exception
        self.exception_str = str(self.exception) if self.exception else None
        #
        self.msg = None
        self.__set_exception()
        self.details = None
        self.__set_details()

    def __set_exception(self):
        self.msg = self.key_value_sep.join(filter(None, [self.msg_key, self.msg_value]))

    def get_exception(self):
        return self.exception(self.msg)

    def set_summary_msg(self, msg, known=False):
        if msg is not None:
            self.summary_msg = msg
            self.known = known
            self.__set_details()

    def get_details(self):
        msg = PhConstants.SEPERATOR_TWO_WORDS.join(
            [PhConstants.KNOWN if self.known else PhConstants.UNKNOWN, self.details])
        return msg

    def __set_details(self):
        exception_summary = _PhCommon.get_key_value_pair(PhConstants.SUMMARY, self.summary_msg, pair_is_must=True)
        exception_details = _PhCommon.get_key_value_pair(PhConstants.DETAILS, PhConstants.SEPERATOR_MULTI_OBJ.join(
            filter(None, [self.exception_str, self.msg])))
        exception_additional_data = PhConstants.SEPERATOR_MULTI_OBJ.join(
            filter(None, self.additional_msgs_list)) if self.additional_msgs_list else None
        exception_header = _PhCommon.get_key_value_pair(PhConstants.EXCEPTION_OCCURRED_AT_FUNC,
                                                        self.function_name) if self.function_name else PhConstants.EXCEPTION_OCCURRED
        self.details = PhConstants.SEPERATOR_MULTI_OBJ.join(
            filter(None, [exception_header, exception_summary, exception_details, exception_additional_data]))
