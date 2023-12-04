import json
import logging
from collections import defaultdict
from datetime import datetime

from flask import jsonify
from flask_restx import Resource

from server.instance import server
from utils.request_parser import Request_Parser
from utils.response import Response
from utils.validator import Validator

app, postgreSQL, search_ns = server.app, server.postgreSQL, server.search_space


@search_ns.route("/")
class Search(Resource):
    request_parser = Request_Parser.search()

    @search_ns.doc(parser=request_parser)
    @Response.search(search_ns)
    def get(self):
        args: dict = self.request_parser.parse_args()

        machine_id = Validator.machine_id(args["machine_id"])
        days = Validator.days(args["days"])
        company = Validator.company(args["company"])

        db_fetch: tuple = postgreSQL.search(
            machine_id=machine_id, limit=(days * 48), company=company
        )

        dict = {"machine_id": machine_id, "results": []}

        for chip_id, value, timestamp in db_fetch:
            dict["chip_id"] = chip_id
            dict["results"].append(
                {
                    "date_time": timestamp.strftime("%Y-%m-%d %H:%M:%S")[:-3],
                    "value": value,
                }
            )

        return jsonify(dict)
