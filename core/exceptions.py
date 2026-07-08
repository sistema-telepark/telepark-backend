class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass


class AuthenticationError(ServiceException):
    pass


class ValidationError(ServiceException):
    pass


class PermissionDeniedError(ServiceException):
    pass


class ConflictError(ServiceException):
    pass
