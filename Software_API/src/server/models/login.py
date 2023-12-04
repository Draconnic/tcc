from flask_restx import fields

from server.instance import server

esp_registration_model = server.login_space.model(
    "Registration Response: 200",
    {
        "access_token": fields.String(),
    },
)
