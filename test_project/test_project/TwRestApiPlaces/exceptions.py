

class YahooSearchException(Exception):
    """
    This class handles all exceptions directly based on Yahoo Woeid Search Exceptions.
    """

    _error_codes = {
        1000 : 'Place unknown'
    }

    def __init__(self, code, msg = None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)


class TwitterRestAPIException(Exception):
    """
    This class handles all exceptions directly based on Twitter Rest API Exceptions.
    """
    _error_codes = {
        304 : 'Not Modified. There was no new data to return.',
        400 : 'Bad Request: The request was invalid',
        401 : 'Unauthorized: Authentication credentials were missing or incorrect',
        403 : 'Forbidden: The request is understood, but it has been refused or access is not allowed',
        404 : 'Not Found: The URI requested is invalid or the resource requested does not exists',
        406 : 'Not Acceptable: Invalid format is specified in the request',
        410 : 'Gone: This resource is gone',
        420 : 'Enhance Your Calm:  You are being rate limited',
        422 : 'Unprocessable Entity: Image unable to be processed',
        429 : 'Too Many Requests: Request cannot be served due to the application\'s rate limit having been exhausted for the resource',
        500 : 'Internal Server Error: Something is broken',
        502 : 'Bad Gateway: Twitter is down or being upgraded',
        503 : 'Service Unavailable: The Twitter servers are up, but overloaded with requests',
        504 : 'Gateway timeout: The request couldn\'t be serviced due to some failure within our stack',
    }

    def __init__(self, code, msg = None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)