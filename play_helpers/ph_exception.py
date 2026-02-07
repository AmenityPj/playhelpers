from play_helpers.ph_exception_helper import PhExceptionHelper


class PhException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return PhExceptionHelper(msg=self.msg)
