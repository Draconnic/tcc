import logging
from os import environ

from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from server.instance import server
from server.models.login import *
from utils.email import Email
from utils.request_parser import Request_Parser
from utils.response import Response
from utils.validator import Validator

event_ns, postgreSQL = server.event_space, server.postgreSQL
load_dotenv()


@event_ns.route("/skimmer")
class Skimmer_Event(Resource):
    request_parser = Request_Parser.skimmer()

    @event_ns.doc(parser=request_parser, security="Token JWT ACCESS")
    @Response.skimmer(name_space=event_ns)
    @jwt_required()
    def post(self):
        try:
            args: dict = self.request_parser.parse_args()
            jwt_data: dict = get_jwt_identity()
            state = Validator.state(args["state"])
            email = Email(
                sender_email=environ.get("API_EMAIL"),
                sender_password=environ.get("API_EMAIL_PASSWORD"),
                smtp_port="smtp.gmail.com",
                smtp_server=587,
            )
            email.sender = environ.get("SENDER_EMAIL")
            email.subject = f"Problema no Skimmer da máquina {jwt_data['machine_id']} - Tanque cheio"
            email.body = f"""Favor verificar se o tanque de descarte da máquina {jwt_data['machine_id']} está cheio"""
            response = email.send_email()
            if response == 200:
                return jsonify(message="Email enviado")
        except server.exceptions as error:
            logging.exception("An error occurred during ESP registration:")
            raise error


@event_ns.route("/ph")
class pH_Event(Resource):
    request_parser = Request_Parser.pH()

    @event_ns.doc(parser=request_parser, security="Token JWT ACCESS")
    @Response.pH(name_space=event_ns)
    @jwt_required()
    def post(self):
        try:
            args: dict = self.request_parser.parse_args()
            jwt_data: dict = get_jwt_identity()

            ph_value = Validator.pH_value(args["ph_value"])

            email = Email(
                "tcc@gobbo.net", "YLalw8izUZPYNONNAeJq", "smtp.gmail.com", 587
            )
            email.sender = "felipe@gobbo.net"
            email.subject = f"Problema no Ph da máquina {jwt_data['machine_id']}"
            email.body = f"""Favor ajustar o nível do pH da máquina, último valor medido: {ph_value}"""
            response = email.send_email()
            if response == 200:
                return jsonify(message="Email enviado")
        except server.exceptions as error:
            logging.exception("An error occurred during ESP registration:")
            raise error
