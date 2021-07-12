
class LemonException(Exception):
    """Baseclass for exceptions raised by the sdk"""
    pass


class LemonConnectionException(LemonException):
    """Raised when there is a problem with the network connection"""
    pass


class LemonAPIException(LemonException):
    """Raised when the request goes through, but there is an error with the api"""
    def __init__(self, status, errormessage):
        self.status = status
        self.errormessage = errormessage

    def get_error_message(self):
        return self.errormessage

    def get_status_code(self):
        return self.status
