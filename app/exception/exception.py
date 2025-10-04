class InvalidOTPService(Exception):
    pass

class InvalidAuthService(Exception):
    pass


class EmailSendError(InvalidOTPService):
    pass

class MissingArgumentError(Exception):
    pass


class PasswordFormatError(Exception):
    pass

class EmailFormatError(Exception):
    pass

class UserNotFoundError(Exception):
    pass