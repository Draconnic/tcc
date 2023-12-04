from flask_restx import reqparse


class Request_Parser:
    """
    A utility class to provide request parsing configurations for Flask-RESTx API endpoints.

    This class contains static methods that define different request parsing configurations
    for different API endpoint scenarios. These configurations are used to validate and extract
    data from incoming requests before processing them in the API endpoint.
    """

    @staticmethod
    def device_registration():
        """
        Get a request parser configuration for device registration endpoint.

        Returns:
            RequestParser: The configured request parser for device registration.
        """
        return (
            reqparse.RequestParser()
            .add_argument(name="chip_id", type=str, required=True, location="form")
            .add_argument(name="machine", type=str, required=False, location="form")
            .add_argument(name="company", type=str, required=True, location="form")
            .add_argument(name="segredo", type=str, required=True, location="form")
        )

    @staticmethod
    def search():
        """
        Get a request parser configuration for searching modules list endpoint.

        Returns:
            RequestParser: The configured request parser for searching modules list.
        """
        return (
            reqparse.RequestParser()
            .add_argument(name="company", type=str, required=True)
            .add_argument(name="machine_id", type=str, required=True)
            .add_argument(name="days", type=int, required=True)
        )

    @staticmethod
    def skimmer():
        """
        Get a request parser configuration for user login endpoint.

        Returns:
            RequestParser: The configured request parser for user login.
        """
        return reqparse.RequestParser().add_argument(
            name="state", type=str, required=True, location="form"
        )

    @staticmethod
    def pH():
        """
        Get a request parser configuration for user login endpoint.

        Returns:
            RequestParser: The configured request parser for user login.
        """
        return reqparse.RequestParser().add_argument(
            name="ph_value", type=float, required=True, location="form"
        )
