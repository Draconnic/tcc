from typing import Literal

from flask_restx import Api, fields

from server.instance import server

skimmer_model = server.event_space.model(
    "Data Response: 200",
    {
        "message": fields.String(),
    },
)

pH_model = server.event_space.model(
    "Data Response: 200",
    {
        "message": fields.String(),
    },
)
