import logging
from os import environ

from dotenv import load_dotenv
from flask import Flask
from flask_restx import Api
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
    NotFound,
    ServiceUnavailable,
)

load_dotenv()


class Configurator:
    """
    A utility class for configuring Flask application and Flask-RESTx API settings.

    This class provides static methods to configure various aspects of the Flask application
    and Flask-RESTx API, including application-wide settings, API version and metadata,
    authorization configurations, namespaces, exception handling, and logging settings.
    """

    @staticmethod
    def app(app: Flask):
        """
        Configure the Flask application.

        Args:
            app (Flask): The Flask application instance.

        Returns:
            None
        """
        # Application-wide settings
        app.config.update(
            {
                "SWAGGER_UI_OAUTH_CLIENT_ID": "MyClientId",
                "SWAGGER_UI_OAUTH_REALM": "-",
                "SWAGGER_UI_OAUTH_APP_NAME": "Demo",
                "JWT_SECRET_KEY": "super-secret",  # Change this!
                "MAX_CONTENT_LENGTH": 16 * 1024,
            }
        )
        app.template_folder = "../templates/"

    @staticmethod
    def api(api: Api):
        """
        Configure the Flask-RESTx API.

        Args:
            api (Api): The Flask-RESTx API instance.

        Returns:
            None
        """
        # API settings
        api.version = "0.9"
        api.title = "TCC"
        api.authorizations = {
            "Token JWT REFRESH": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
            },
            "Token JWT ACCESS": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
            },
        }
        api.doc = "/"
        api.description = "TEST"

    @staticmethod
    def name_spaces():
        """
        Define and return namespace configurations.

        Returns:
            dict: Namespace configurations.
        """
        return {
            "login": {
                "name": "login",
                "description": "Area to request a temporary token for the user or by the esp device.",
            },
            "search": {"name": "search", "description": "To develop"},
            "data": {
                "name": "data",
                "description": "This is the point where data is inserted into the database.",
            },
            "event": {
                "name": "event",
                "description": "This is the endpoint where the HUB use for warning the user.",
            },
        }

    @staticmethod
    def exceptions():
        """
        Get a tuple of custom exceptions for handling in the application.

        Returns:
            tuple: Tuple of exception classes.
        """
        return (
            BadRequest,
            InternalServerError,
            NotFound,
            ServiceUnavailable,
        )

    @staticmethod
    def logging():
        """
        Configure logging settings based on the specified log level.

        Returns:
            None
        """

        log_level = environ.get("LOGGING")
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        LEVEL = levels[log_level]
        if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                "Invalid log level. Please choose from DEBUG, INFO, WARNING, ERROR, or CRITICAL."
            )
        elif LEVEL == logging.DEBUG:
            # Set up logging format for DEBUG level
            logging.basicConfig(
                level=LEVEL,
                format="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif LEVEL == logging.INFO:
            # Set up logging format for INFO level
            logging.basicConfig(
                level=LEVEL,
                format="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif LEVEL == logging.WARNING:
            # Set up logging format for WARNING level
            logging.basicConfig(
                level=LEVEL,
                format="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif LEVEL == logging.ERROR:
            # Set up logging format for ERROR level
            logging.basicConfig(
                level=LEVEL,
                format="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif LEVEL == logging.CRITICAL:
            # Set up logging format for CRITICAL level
            logging.basicConfig(
                level=LEVEL,
                format="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
