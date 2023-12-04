import re
from datetime import datetime, timedelta

from werkzeug.exceptions import BadRequest, Unauthorized


class BaseValidator:
    _value = None
    key = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class String_Validator(BaseValidator):
    max_length: int = None
    condition: str = None
    text: str = None
    required: bool = True

    @BaseValidator.value.setter
    def value(self, new_value):
        if new_value != None:
            if type(new_value) != str:
                raise BadRequest(description=f"{self.key} must be a string.")
            elif new_value == None:
                raise BadRequest(description=f"{self.key} cannot be empty.")
            elif len(new_value) > self.max_length:
                raise BadRequest(
                    f"Character limit ({self.max_length}) exceeded in {self.key}."
                )
            elif not re.match(rf"{self.condition}", new_value):
                raise BadRequest(description=self.text.format(self.key))
            self._value = new_value
        else:
            self._value = None


class Boolean_Validator(BaseValidator):
    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) != bool:
            raise BadRequest(description=f"{self.key} must be a boolean.")
        self._value = new_value


class Float_Validator(BaseValidator):
    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) == int:
            return float(new_value)
        elif type(new_value) != float:
            raise BadRequest(description=f"{self.key} must be a float.")
        self._value = new_value


class Integer_Validator(BaseValidator):
    condition: str = None
    text: str = None

    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) == float:
            return int(new_value)
        elif type(new_value) != int:
            raise BadRequest(description=f"{self.key} must be a integer.")
        elif self.condition != None and not re.match(
            rf"{self.condition}", str(new_value)
        ):
            raise BadRequest(description=self.text.format(self.key))
        self._value = new_value


class Dict_Validator(BaseValidator):
    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) != dict:
            raise BadRequest(description=f"{self.key} must be a dict.")
        self._value = new_value


class Date_Time_Validator(BaseValidator):
    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) != str:
            raise BadRequest(description=f"{self.key} must be a string.")
        try:
            dt_value = datetime.fromisoformat(new_value[:-1])
        except ValueError:
            raise BadRequest(
                description=f"{self.key} must follow this pattern: %Y-%m-%dT%H:%M:%S.%fZ"
            )
        current_datetime = datetime.now()
        if dt_value < current_datetime - timedelta(days=30):
            raise BadRequest(
                description=f"The provided date for {self.key} is invalid as it's in the past. (1 Month)"
            )
        elif dt_value > current_datetime + timedelta(days=1):
            raise BadRequest(
                description=f"The provided date for {self.key} is invalid as it's in the future."
            )
        self._value = new_value


class Device_Secret_Validator(BaseValidator):
    @BaseValidator.value.setter
    def value(self, new_value):
        if type(new_value) != str:
            raise BadRequest(description=f"{self.key} must be a string")
        if new_value != "secret":
            raise Unauthorized(description=f"{self.key}: Invalid authorization data")
        self._value = new_value


class Validator:
    _string = String_Validator
    _boolean = Boolean_Validator
    _float = Float_Validator
    _dict = Dict_Validator
    _date_time = Date_Time_Validator
    _device_secret = Device_Secret_Validator
    _days = Integer_Validator
    _ph_value = Float_Validator
    _state = String_Validator

    @classmethod
    def chip_id(cls, value):
        string = cls._string()
        string.key = "chip_id"
        string.max_length = 15
        string.condition = "^[a-zA-Z0-9]*$"
        string.text = "{} must contain only letters and numbers."
        string.value = value
        if string.value:
            return string.value.upper()
        else:
            return None

    @classmethod
    def machine_id(cls, value):
        string = cls._string()
        string.key = "machine_id"
        string.max_length = 20
        string.required = False
        string.condition = "^[a-zA-Z0-9]*$"
        string.text = "{} must contain only letters and numbers."
        string.value = value
        if string.value:
            return string.value.lower()
        else:
            return None

    @classmethod
    def company(cls, value):
        string = cls._string()
        string.key = "company"
        string.max_length = 20
        string.condition = "^[a-zA-Z]+$"
        string.text = "{} must contain only letters."
        string.value = value
        if string.value:
            return string.value.lower()
        else:
            return None

    @classmethod
    def device_secret(cls, value):
        device_secret = cls._device_secret()
        device_secret.key = "segredo"
        device_secret.value = value
        return None

    @classmethod
    def days(cls, value):
        integer = cls._days()
        integer.condition = "^[1-7]*$"
        integer.text = "{} must contain only numbers from 1 to 7."
        integer.key = "days"
        integer.value = value
        return integer.value

    @classmethod
    def state(cls, value):
        string = cls._state()
        string.key = "state"
        string.max_length = 5
        string.condition = "^[a-z]*$"
        string.text = "{} must contain only letters."
        string.value: str = value
        if string.value:
            return string.value.lower()
        else:
            return None

    @classmethod
    def pH_value(cls, value):
        float = cls._ph_value()
        float.key = "ph_value"
        float.value = value
        return float.value

    @classmethod
    def date_time(cls, value):
        date_time = cls._date_time()
        date_time.key = "date_time"
        date_time.value = value
        return datetime.fromisoformat(date_time.value[:-1])

    @classmethod
    def properties(cls, value):
        def dict_func(value, key):
            dict = cls._dict()
            dict.key = key
            dict.value = value
            return dict.value

        def float_func(value, key):
            float = cls._float()
            float.key = key
            float.value = value
            return float.value

        def boolean_func(value, key):
            boolean = cls._boolean()
            boolean.key = key
            boolean.value = value
            return boolean.value

        dict_func(value, "properties")

        required_keys = ["output2", "level_sensor", "ph_sensor", "skimmer"]

        for key in value:
            if key not in required_keys:
                raise BadRequest(f"{key} must not be in the main tree")

        try:
            output2 = dict_func(value["output2"], "output2")
            level_sensor = dict_func(value["level_sensor"], "level_sensor")
            ph_sensor = dict_func(value["ph_sensor"], "ph_sensor")
            skimmer = dict_func(value["skimmer"], "skimmer")
        except KeyError as error:
            raise BadRequest(
                f"{error} missing in the main tree. Please verify the dict format."
            )

        try:
            boolean_func(output2["state"], "output2: { state }")
            boolean_func(
                level_sensor["connected_state"], "level_sensor:{ connected_state }"
            )
            boolean_func(level_sensor["sensor_state"], "level_sensor:{ sensor_state }")
            float_func(ph_sensor["value"], "ph_sensor:{ value }")
            boolean_func(skimmer["state"], "skimmer:{ state }")
        except KeyError as error:
            raise BadRequest(
                f"{error} missing in a sub-tree. Please verify the dict format."
            )
        return value
