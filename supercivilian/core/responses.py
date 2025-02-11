import typing

from rest_framework.response import Response


class APIResponse(Response):
    """Base response class for API responses.

    Defines a standard structure for API responses consisting of:
        - success: A boolean indicating the success of the request.
        - payload: A dictionary containing the response data.
            Should be populated when success is True. Defaults to None.
        - error: A dictionary containing error details.
            Should be populated when success is False. Defaults to None.
    """

    def __init__(
        self,
        success: bool,
        error: dict[str, typing.Any] | None = None,
        payload: dict[str, typing.Any] | None = None,
        status: int = 200,
    ) -> None:
        """Initialize the response object.

        Args:
            success: A boolean indicating the success of the request.
            error: A dictionary containing error details.
                Should be populated when success is False. Defaults to None.
            payload: A dictionary containing the response data.
                Should be populated when success is True. Defaults to None.
            status: The HTTP status code. Defaults to 200.
        """
        response = {
            "success": success,
        }

        if success and payload is not None:
            response["payload"] = payload
        elif not success and error is not None:
            response["error"] = error

        super().__init__(response, status=status)


class APISuccessResponse(APIResponse):
    """Response class for successful API responses."""

    def __init__(
        self, status: int = 200, payload: typing.Any = None, **kwargs: typing.Any
    ) -> None:
        """Initialize the response object.

        Args:
            status: The HTTP status code. Defaults to 200.
            payload: The response payload.
            **kwargs: If specified, the payload will be a dictionary containing
                these keyword arguments.
        """
        if payload is None:
            payload = kwargs or None

        super().__init__(success=True, payload=payload, status=status)


class APIErrorResponse(APIResponse):
    """Response class for failed API responses."""

    def __init__(
        self, status: int = 500, error: typing.Any = None, **kwargs: typing.Any
    ) -> None:
        """Initialize the response object.

        Args:
            status: The HTTP status code. Defaults to 500.
            error: The error payload.
            **kwargs: If specified, the error payload will be a dictionary
                containing these keyword arguments.
        """
        if error is None:
            error = kwargs or None

        super().__init__(success=False, error=error, status=status)
