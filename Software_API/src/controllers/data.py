import logging

import requests
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import Resource

from server.instance import server
from utils.response import Response
from utils.validator import Validator

data_ns, postgreSQL, app = server.data_space, server.postgreSQL, server.app


def pH_function(pH_value: dict, token_jwt_sub):
    if 6.0 > pH_value < 9.0:
        token = create_access_token(identity=token_jwt_sub)
        requests.post(
            url="http://127.0.0.1:5000/event/ph",
            data={"ph_value": f"{pH_value}"},
            headers={"Authorization": f"Bearer {token}"},
        )


@data_ns.route("/insert")
class Request_Chip(Resource):
    @data_ns.doc(security="Token JWT ACCESS")
    @Response.data_insert(data_ns)
    @jwt_required()
    def post(self):
        try:
            jwt_data: dict = get_jwt_identity()

            logging.info(f"Requisição recebida de Autorization.")

            if jwt_data["type"] == "ESP":
                payload = data_ns.payload
                chip_id = Validator.chip_id(jwt_data["chip_id"])
                company = Validator.company(jwt_data["company"])
                properties = Validator.properties(payload["properties"])
                date_time = Validator.date_time(payload["date_time"])

                postgreSQL.esp_data_logs(
                    company=company,
                    chip_id=chip_id,
                    properties=properties,
                    date_time=date_time,
                    app=app,
                )
                pH_function(
                    pH_value=properties["ph_sensor"]["value"],
                    token_jwt_sub=get_jwt()["sub"],
                )
                return {"message": "Dado registrado com sucesso"}, 201
        except server.exceptions as error:
            logging.error(f"Erro ao processar requisição: {str(error)}")
            raise error
