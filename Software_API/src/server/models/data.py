from flask_restx import fields

from server.instance import server

insert_payload_model = server.data_space.model(
    "Data Payload",
    {
        "date_time": fields.DateTime(dt_format="rfc822"),
        "properties": fields.Nested(
            server.data_space.model(
                "properties",
                {
                    "bubbler": fields.Nested(
                        server.data_space.model(
                            "bubbler",
                            {
                                "state": fields.Boolean(),
                            },
                        )
                    ),
                    "level_sensor": fields.Nested(
                        server.data_space.model(
                            "level_sensor",
                            {
                                "connected_state": fields.Boolean(),
                                "sensor_state": fields.Boolean(),
                            },
                        )
                    ),
                    "ph_sensor": fields.Nested(
                        server.data_space.model(
                            "ph_sensor",
                            {
                                "value": fields.Float(),
                            },
                        )
                    ),
                    "skimmer": fields.Nested(
                        server.data_space.model(
                            "skimmer",
                            {
                                "state": fields.Boolean(),
                            },
                        )
                    ),
                },
            )
        ),
    },
)

insert_response_model = server.data_space.model(
    "Data Response: 200",
    {
        "message": fields.String(),
    },
)
