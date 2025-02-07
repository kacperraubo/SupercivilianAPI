import typing

from django.http import HttpRequest


class ParameterError(Exception):
    def __init__(self, parameter: str, message: str = None) -> None:
        self.parameter = parameter

        super().__init__(message)


class SearchParameters:
    """Utility class for handling request parameters."""

    def __init__(self, request: HttpRequest):
        """Initialize the parameters object with a request.

        Args:
            request: The HTTP request object.
        """
        self.request = request
        self.mapping = request.GET if request.method == "GET" else request.POST

    @typing.overload
    def string(
        self,
        key: str,
        default: None = None,
        required: typing.Literal[False] = False,
        strip: bool = True,
    ) -> str | None: ...

    @typing.overload
    def string(
        self,
        key: str,
        default: None = None,
        required: typing.Literal[True] = True,
        strip: bool = True,
    ) -> str: ...

    @typing.overload
    def string(
        self, key: str, default: str, required: bool = False, strip: bool = True
    ) -> str: ...

    def string(
        self,
        key: str,
        default: str | None = None,
        required: bool = False,
        strip: bool = True,
    ) -> str | None:
        """Get a string parameter from the request.

        Args:
            key: The parameter key.
            default: The default value.
                Defaults to None.
            required: Whether the parameter is required.
                Defaults to False. Empty strings are considered missing.
            strip: Whether to strip the parameter value.
                Defaults to True.

        Returns:
            The parameter value.

        Raises:
            ParameterError: If the parameter is required and missing.
        """
        value = self.mapping.get(key, default)

        if strip and value is not None:
            value = value.strip()

        if required and value is None or value == "":
            raise ParameterError(key, f"{key} parameter is required")

        return value

    @typing.overload
    def integer(
        self, key: str, default: None = None, required: typing.Literal[False] = False
    ) -> int | None: ...

    @typing.overload
    def integer(
        self, key: str, default: None = None, required: typing.Literal[True] = True
    ) -> int: ...

    @typing.overload
    def integer(self, key: str, default: int, required: bool = False) -> int: ...

    def integer(
        self, key: str, default: int | None = None, required: bool = False
    ) -> int | None:
        """Get an integer parameter from the request.

        Args:
            key: The parameter key.
            default: The default value.
                Defaults to None.
            required: Whether the parameter is required.
                Defaults to False.

        Returns:
            The parameter value.

        Raises:
            ParameterError: If the parameter is required and missing or not an integer.
        """
        value = self.mapping.get(key, default)

        if required and value is None:
            raise ParameterError(key, f"{key} parameter is required")

        try:
            return int(value)
        except (TypeError, ValueError):
            raise ParameterError(key, f"{key} parameter must be an integer")
