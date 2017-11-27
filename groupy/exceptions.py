

class GroupyError(Exception):
    """Base exception for all Groupy exceptions.

    :param str message: a description of the exception
    """
    #: a description of the exception
    message = None

    def __init__(self, message=None):
        self.message = message or self.message
        super().__init__(self.message)


class ApiError(GroupyError):
    """Base exception for all GroupMe API errors."""
    message = 'There was a problem communicating with the API.'


class NoResponse(ApiError):
    """Exception raised when the API server could not be reached.

    :param request: the original request that was made
    :type request: :class:`~requests.PreparedRequest`
    :param str message: a description of the exception
    """

    message = 'Could not get a response'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class BadResponse(ApiError):
    """Exception raised when the status code of the response was 400 or more.

    :param response: the response
    :type response: :class:`~requests.Response`
    :param str message: a description of the exception
    """

    message = 'Got a bad response'

    def __init__(self, response, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response


class InvalidJsonError(BadResponse):
    """Exception raised for incomplete/invalid JSON in a response."""

    def __init__(self, response, message='The JSON was incomplete/invalid'):
        super().__init__(response, message)


class MissingResponseError(BadResponse):
    """Exception raised for a response that lacks response data."""

    def __init__(self, response, message='The response contained no response data'):
        super().__init__(response, message)


class MissingMetaError(BadResponse):
    """Exception raised for a response that lacks meta data."""

    def __init__(self, response, message='The response contained no meta data'):
        super().__init__(response, message)


class ResultsError(ApiError):
    """Exception raised for asynchronous results.

    :param response: the response
    :type response: :class:`~requests.Response`
    :param str message: a description of the exception
    """

    def __init__(self, response, message):
        super().__init__(message)
        self.response = response


class ResultsNotReady(ResultsError):
    """Exception raised when results are not yet ready.

    :param response: the response
    :type response: :class:`~requests.Response`
    :param str message: a description of the exception
    """

    def __init__(self, response, message='The results are not ready yet'):
        super().__init__(response, message)


class ResultsExpired(ResultsError):
    """Exception raised when the results have expired.

    :param response: the response
    :type response: :class:`~requests.Response`
    :param str message: a description of the exception
    """

    def __init__(self, response, message='The results have expired'):
        super().__init__(response, message)
