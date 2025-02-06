import typing

from django.http import JsonResponse


class APIResponse(JsonResponse):
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

        if success:
            response["payload"] = payload
        else:
            response["error"] = error

        super().__init__(response, status=status)


class APISuccessResponse(APIResponse):
    """Response class for successful API responses."""

    def __init__(self, status: int = 200, **kwargs: typing.Any) -> None:
        """Initialize the response object.

        Args:
            status: The HTTP status code. Defaults to 200.
            **kwargs: Keyword arguments to be included in the response payload.
        """
        super().__init__(success=True, payload=kwargs or None, status=status)


class APIErrorResponse(APIResponse):
    """Response class for failed API responses."""

    def __init__(self, status: int = 500, **kwargs: typing.Any) -> None:
        """Initialize the response object.

        Args:
            status: The HTTP status code. Defaults to 500.
            **kwargs: Keyword arguments to be included in the error payload.
        """
        super().__init__(success=False, error=kwargs or None, status=status)
