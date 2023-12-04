from typing import Literal

from flask_restx import Api, fields

from server.instance import server

search_model = server.search_space.model(
    "Search",
    {
        "chip_id": fields.String(),
        "machine_id": fields.String(),
        "results": fields.List(
            fields.Nested(
                server.search_space.model(
                    "Search_Results",
                    {
                        "date_time": fields.DateTime(),
                        "ph_value": fields.Float(),
                    },
                )
            )
        ),
    },
)


def data_result_model(type_id: Literal["machine_id", "chip_id"]):
    """Define a model for data results based on the type ID.

    Args:
        type_id (Literal["machine_id", "chip_id"]): The type ID for data results.

    Returns:
        Model: The data result model.

    """
    # Create a mapping dictionary
    map = {type: type for type in ["machine_id", "chip_id"]}

    # Define a model for data list using the search namespace model method
    return server.search_space.model(
        "Data_list",
        {
            "object": fields.String(),
            "length": fields.Integer(),
            "results": fields.List(
                fields.Nested(
                    server.search_space.model(
                        "Data_Results",
                        {
                            map.get(type_id): fields.String(),
                            "date_time": fields.DateTime(dt_format="rfc822"),
                            "properties": fields.Nested(
                                server.search_space.model(
                                    "properties",
                                    {
                                        "bubbler": fields.Nested(
                                            server.search_space.model(
                                                "bubbler",
                                                {
                                                    "state": fields.Boolean(),
                                                },
                                            )
                                        ),
                                        "level_sensor": fields.Nested(
                                            server.search_space.model(
                                                "level_sensor",
                                                {
                                                    "connected_state": fields.Boolean(),
                                                    "sensor_state": fields.Boolean(),
                                                },
                                            )
                                        ),
                                        "ph_sensor": fields.Nested(
                                            server.search_space.model(
                                                "ph_sensor",
                                                {
                                                    "value": fields.Float(),
                                                },
                                            )
                                        ),
                                        "skimmer": fields.Nested(
                                            server.search_space.model(
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
                )
            ),
        },
    )
