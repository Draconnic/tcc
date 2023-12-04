from flask_restx import Namespace

from server.models.data import insert_payload_model, insert_response_model
from server.models.event import pH_model, skimmer_model
from server.models.login import esp_registration_model
from server.models.search import search_model


class Response:
    """
    A utility class to provide standardized response decorators for Flask-RESTx namespaces.

    This class contains static methods that define decorators for different response scenarios.
    These decorators can be applied to Flask-RESTx namespace methods to provide consistent
    response structures and documentation for API endpoints.
    """

    @staticmethod
    def device_registration(name_space: Namespace):
        """
        A decorator factory for device registration response handling.

        Args:
            name_space (Namespace): The Flask-RESTx namespace.

        Returns:
            function: The decorator function to apply to the desired endpoint method.
        """

        def decorator(func):
            @name_space.response(
                200, "Device registration found.", model=esp_registration_model
            )
            @name_space.response(
                code=400,
                description="[Character limit exceeded, Invalid string, Header missing]",
            )
            @name_space.response(
                code=401,
                description="[Bearer missing in Authorization header]",
            )
            @name_space.response(
                code=402,
                description="[Invalid header content]",
            )
            @name_space.response(
                code=404,
                description="[Device (chip_id) or Company not found]",
            )
            @name_space.response(
                code=422,
                description="[Invalid authorization header, Lack of segments, Only refresh tokens are accepted]",
            )
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def data_insert(name_space: Namespace):
        """
        A decorator factory for data insertion response handling.

        Args:
            name_space (Namespace): The Flask-RESTx namespace.

        Returns:
            function: The decorator function to apply to the desired endpoint method.
        """

        def decorator(func):
            @name_space.expect(insert_payload_model)
            @name_space.response(
                200, "Data Sent Successfully.", model=insert_response_model
            )
            @name_space.response(
                code=400,
                description="[Invalid Data]",
            )
            @name_space.response(
                code=401,
                description="[Bearer missing in Authorization header]",
            )
            @name_space.response(
                code=422,
                description="[Invalid authorization header, Lack of segments, Only refresh tokens are accepted]",
            )
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def search(name_space: Namespace):
        """
        A decorator factory for user login response handling.

        Args:
            name_space (Namespace): The Flask-RESTx namespace.

        Returns:
            function: The decorator function to apply to the desired endpoint method.
        """

        def decorator(func):
            @name_space.response(200, "Data Sent Successfully.", model=search_model)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def skimmer(name_space: Namespace):
        """
        A decorator factory for user login response handling.

        Args:
            name_space (Namespace): The Flask-RESTx namespace.

        Returns:
            function: The decorator function to apply to the desired endpoint method.
        """

        def decorator(func):
            @name_space.response(200, "Device registration found.", model=skimmer_model)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def pH(name_space: Namespace):
        """
        A decorator factory for user login response handling.

        Args:
            name_space (Namespace): The Flask-RESTx namespace.

        Returns:
            function: The decorator function to apply to the desired endpoint method.
        """

        def decorator(func):
            @name_space.response(200, "Device registration found.", model=pH_model)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator
