import logging
from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_restx import Resource

from server.instance import server
from server.models.login import *
from utils.request_parser import Request_Parser
from utils.response import Response
from utils.validator import Validator

login_ns, postgreSQL = server.login_space, server.postgreSQL


@login_ns.route("/device_registration")
class Registration(Resource):
    request_parser = Request_Parser.device_registration()

    @login_ns.doc(parser=request_parser, security="Token JWT REFRESH")
    @Response.device_registration(name_space=login_ns)
    @jwt_required(refresh=True)
    def post(self):
        """
        Verificar o registro do ESP na api, para obter um token JWT temporário.
        """
        try:
            args: dict = self.request_parser.parse_args()

            Validator.device_secret(args["segredo"])
            chip_id = Validator.chip_id(args["chip_id"])
            machine_id = Validator.machine_id(args["machine"])
            company = Validator.company(args["company"])

            _, machine_id, _ = postgreSQL.device_registration(
                chip_id=chip_id, machine_id=machine_id, company=company
            )

            logging.info("ESP registration successful")

            return jsonify(
                access_token=create_access_token(
                    identity={
                        "type": "ESP",
                        "chip_id": chip_id,
                        "machine_id": machine_id,
                        "company": company,
                    },
                    expires_delta=timedelta(seconds=6000000),
                ),
            )
        except server.exceptions as error:
            logging.exception("An error occurred during ESP registration:")
            raise error


@login_ns.route("/esp_jwt")
class Protected(Resource):
    # @login_ns.doc(security="apikey")
    def post(self):
        try:
            logging.info("Refresh token created successfully for identity 'TCC'")
            return jsonify(refresh_token=create_refresh_token(identity="TCC"))
        except Exception as error:
            logging.exception(
                "An error occurred while creating access and refresh tokens:"
            )
            raise error
