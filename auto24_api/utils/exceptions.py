class InvalidArgsException(Exception):
    """Exception raised when invalid input class arguments"""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class QueryParamsValidationError(Exception):
    """Exception raised when input for query params is invalid"""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class DataNotFoundException(Exception):
    """Exception raised when data is not found from the response"""

    message = "Max retries reached. The could not be found in the response."

    def __init__(self) -> None:
        super().__init__(self.message)


class ReCaptchaRequiredException(Exception):
    """Exception raised when the reCAPTCHA is required"""

    message = "reCAPTCHA verification is required."

    def __init__(self) -> None:
        super().__init__(self.message)
