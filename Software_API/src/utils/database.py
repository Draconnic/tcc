import logging
from datetime import datetime
from os import environ
from typing import Literal

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection
from werkzeug.exceptions import InternalServerError, NotFound, ServiceUnavailable

load_dotenv()


class PostgreSQL:
    """
    A utility class for interacting with PostgreSQL databases.
    """

    def __init__(self) -> None:
        """
        Initialize the PostgreSQL class with database connection details from environment variables.
        """
        self.host = environ.get("POSTGRES_HOST")
        self.database = environ.get("POSTGRES_DB")
        self.user = environ.get("POSTGRES_USER")
        self.password = environ.get("POSTGRES_PASSWORD")
        self.port = environ.get("POSTGRES_PORTS").replace(":5432", "")
        self._connection = None
        self._cursor = None
        self._query = None

    def connection(self) -> connection:
        """
        Create a connection to the PostgreSQL database.

        Returns:
            psycopg2.extensions.connection: A connection object.
        Raises:
            ServiceUnavailable: If the PostgreSQL server is unavailable.
        """
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                logging.info("Database connection established")
                self._connection.autocommit = True
                self._cursor = self._connection.cursor()
                self._rollback = self._connection.rollback()
                return self._connection
            except psycopg2.Error:
                raise ServiceUnavailable(description="PostgreSQL server unavailable")

    @property
    def cursor(self):
        """
        Get the cursor associated with the current connection.

        Returns:
            psycopg2.extensions.cursor: A cursor object.
        """
        return self._cursor

    @property
    def rollback(self):
        """
        Get the cursor associated with the current connection.

        Returns:
            psycopg2.extensions.cursor: A cursor object.
        """
        return self._rollback

    @property
    def query(self):
        """
        Get the currently set query.

        Returns:
            str: The SQL query string.
        """
        return self._query

    @query.setter
    def query(self, string: str):
        """
        Set the query to be executed.

        Args:
            string (str): The SQL query string to be set.
        """
        self._query = string

    def execute(self):
        """
        Execute the currently set query using the cursor.

        Returns:
            psycopg2.extensions.cursor: The cursor object after executing the query.
        """
        try:
            self.cursor.execute(self.query)
            self.query = None
            return self
        except psycopg2.Error:
            raise InternalServerError

    def fetch(self, type: Literal["one", "many", "all"], amount: int = 0):
        """
        Fetch the query result based on the fetch type.

        Args:
            type (str): The fetch type ("one", "many", or "all").
            amount (int): The number of rows to fetch (for "many" fetch type).

        Returns:
            list or tuple: The fetched data.
        Raises:
            ValueError: If an invalid fetch type is provided.
        """
        fetch_type_mapping = {"one": "fetchone", "many": "fetchmany", "all": "fetchall"}

        if type not in fetch_type_mapping:
            raise ValueError("Invalid fetch type")

        fetch_type = fetch_type_mapping[type]
        fetch_method = getattr(self.cursor, fetch_type)

        if type == "many":
            return fetch_method(amount)
        else:
            return fetch_method()

    def close(self):
        """
        Close the cursor and connection if they are open.
        """
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._connection:
            self._connection.close()
            self._connection = None


class Database(PostgreSQL):
    def device_registration(self, chip_id: str, machine_id: str, company: str) -> tuple:
        """
        Verifies and registers a device in the database.

        Args:
            chip_id (str): The ESP chip ID.
            machine_id (str): The machine ID associated with the device.
            company (str): The company name.

        Returns:
            tuple: A tuple containing the registered chip ID and company name.
        Raises:
            InternalServerError: If there's an error during registration.
            NotFound: If the requested company doesn't exist.
        """
        self.connection()

        try:
            self.query = f"""
                SELECT chip_id, machine_id  FROM {company}.devices 
                WHERE chip_id = \'{chip_id}\';
            """
            self.execute()
        except psycopg2.Error as error:
            raise NotFound(description=f"{company} does not exist.")

        device_data = self.fetch("all")

        if len(device_data) == 0 and type(machine_id) == str:
            try:
                self.query = f"""
                    INSERT INTO {company}.devices (chip_id, machine_id) VALUES (\'{chip_id}\', \'{machine_id}\');
                """
                self.execute()
                logging.info(
                    f"Registration of esp: {chip_id} in company: {company} was successful"
                )
                return chip_id, machine_id, company
            except psycopg2.Error as error:
                raise InternalServerError(description=f"Database error: {error}")
        elif len(device_data) == 0 and machine_id == None:
            raise InternalServerError(
                description=f"{chip_id} is not registered, and the machine was not defined."
            )
        try:
            self.query = f"""
                SELECT machine_id  FROM {company}.devices
                WHERE {company}.devices.chip_id = \'{chip_id}\'
            """
            print(self.query)
            self.execute()
            data = self.fetch("one")
            if len(data) == 1:
                return chip_id, data[0], company
        except:
            return None, None, None

    def esp_data_logs(
        self, company: str, chip_id: str, properties: dict, date_time: datetime, app
    ):
        """
        Log data from an ESP device into the database.

        Args:
            company (str): The company name.
            chip_id (str): The ESP chip ID.
            properties (dict): Dictionary containing data properties.
            date_time (datetime): The date and time of the data.

        Raises:
            InternalServerError: If there's an error during data logging.
        """
        self.connection()
        output2: bool = properties["output2"]["state"]
        level_sensor: bool = properties["level_sensor"]
        ph_sensor: float = properties["ph_sensor"]["value"]
        skimmer: bool = properties["skimmer"]["state"]
        try:
            self.query = f"""
                INSERT INTO {company}.measurement VALUES (\'{chip_id}\', {output2}, {level_sensor["connected_state"]}, {level_sensor["sensor_state"]}, {ph_sensor}, {skimmer}, \'{date_time.strftime("%Y-%m-%d %H:%M:%S.%f")}\');
            """
            app.logger.debug(self.query)
            self.execute()
            logging.info(
                f"Data successfully registered - chip_id: {chip_id}, company: {company}"
            )
        except psycopg2.Error as error:
            raise InternalServerError(f"Error in {error}")

    def search(self, machine_id: str, limit: int, company: str) -> tuple:
        self.connection()
        try:
            self.query = f"""
                SELECT {company}.measurement.chip_id, {company}.measurement.ph_sensor_value, {company}.measurement.date_time  FROM {company}.devices 
                JOIN {company}.measurement ON {company}.devices.chip_id = {company}.measurement.chip_id
                WHERE {company}.devices.machine_id = \'{machine_id}\'
                ORDER BY {company}.measurement.date_time DESC
                LIMIT {limit};
            """
            self.execute()
            data = self.fetch("all")

            if data == []:
                raise NotFound(f"{machine_id} not found")
            return data
        except psycopg2.Error as error:
            raise InternalServerError(f"Error in {error}")

    # def user_devices_list(self, company: str):
    #    try:
    #        with self.connection().cursor() as cursor:
    #            cursor.execute(
    #                f"""
    #                SET search_path TO {company};
    #                SELECT chip_id, machine_id FROM devices
    #                ORDER BY chip_id;
    #                """
    #            )
    #            rows = cursor.fetchall()
    #            data = {}
    #            data["length"] = len(rows)
    #            data["object"] = "list"
    #            data["results"] = [
    #                {"chip_id": row[0], "machine_id": row[1]} for row in rows
    #            ]
    #            return data
    #    except psycopg2.Error as e:
    #        print(f"Ocorreu um erro ao executar a consulta: {e}")

    # def user_data_list(
    #    self,
    #    company: str,
    #    type_id: Literal["machine_id", "chip_id"],
    #    device_id: str,
    #    limit: int = None,
    #    order: str = None,
    # ) -> list:
    #    try:
    #        if not limit:
    #            limit = 5
    #        if not order:
    #            order = "DESC"
    #        with self.connection().cursor() as cursor:
    #            cursor.execute(f"SET search_path TO {company};")
    #            cursor.execute(
    #                f"""
    #                SELECT measurement.* FROM devices
    #                JOIN measurement ON devices.chip_id = measurement.chip_id
    #                WHERE devices.{type_id} = '{device_id}' AND measurement.date_Time > devices.updated
    #                ORDER BY measurement.date_time {order}
    #                LIMIT {limit};
    #                """
    #            )
    #            rows = cursor.fetchall()
    #            data = {
    #                "length": len(rows),
    #                "object": "list",
    #            }
    #            data["results"] = [
    #                {
    #                    type_id: device_id,
    #                    "date_time": row[6],
    #                    "properties": {
    #                        "output2": {
    #                            "state": row[1],
    #                        },
    #                        "level_sensor": {
    #                            "connected_state": row[2],
    #                            "sensor_state": row[3],
    #                        },
    #                        "ph_sensor": {
    #                            "value": row[4],
    #                        },
    #                        "skimmer": {
    #                            "state": row[5],
    #                        },
    #                    },
    #                }
    #                for row in rows
    #            ]
    #            return data
    #    except psycopg2.Error as e:
    #        print(f"Ocorreu um erro ao executar a consulta: {e}")
