import logging
import sys
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from utils.database import Database
from utils.instance_configurator import Configurator


class Server:
    """Class representing the server."""

    def __init__(self) -> None:
        """Initialize the server instance."""

        self.app = Flask(__name__)
        Configurator.app(self.app)

        self.api = Api(app=self.app)
        Configurator.api(self.api)

        self.jwt = JWTManager(self.app)

        self.login_space = self.custom_namespace("login")
        self.search_space = self.custom_namespace("search")
        self.data_space = self.custom_namespace("data")
        self.event_space = self.custom_namespace("event")

        self.postgreSQL = Database()

        self.exceptions = Configurator.exceptions()

        Configurator.logging()
        log_handler = RotatingFileHandler("app.log", maxBytes=10240, backupCount=10)
        log_handler.setLevel(logging.DEBUG)

        # Formatar o registro no arquivo de log
        log_format = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
        log_handler.setFormatter(log_format)
        self.app.logger.addHandler(log_handler)

    def custom_namespace(self, choice):
        """Create a namespace for login."""
        try:
            chosen = Configurator.name_spaces()[choice]
            return self.api.namespace(
                name=chosen["name"],
                description=chosen["description"],
            )
        except KeyError:
            logging.error(f"Erro: A chave {choice} não existe no dicionário.")
            sys.exit()

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        load_dotenv: bool = True,
    ):
        """Run the server."""
        try:
            self.app.run(host, port, debug, load_dotenv)
        except Exception as error:
            logging.error(f"Erro ao iniciar o servidor: {str(error)}")
            sys.exit()


# Create an instance of the Server class
server = Server()
