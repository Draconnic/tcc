import base64
import logging
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import requests
from flask import render_template
from matplotlib.dates import DateFormatter, date2num
from matplotlib.figure import Figure

from server.instance import server

app, postgreSQL = server.app, server.postgreSQL


@app.route("/display/")
def graph():
    try:
        # Generate the figure **without using pyplot**.
        data = {
            "chip_id": "1640E0",
            "machine_id": "abacate",
            "results": [
                {"date_time": "2023-11-14 00:00", "value": 4.87},
                {"date_time": "2023-11-14 00:30", "value": 10.12},
                {"date_time": "2023-11-14 01:00", "value": 6.45},
                {"date_time": "2023-11-14 01:30", "value": 1.23},
                {"date_time": "2023-11-14 02:00", "value": 8.76},
                {"date_time": "2023-11-14 02:30", "value": 2.34},
                {"date_time": "2023-11-14 03:00", "value": 9.81},
                {"date_time": "2023-11-14 03:30", "value": 3.45},
                {"date_time": "2023-11-14 04:00", "value": 7.89},
                {"date_time": "2023-11-14 04:30", "value": 4.56},
                {"date_time": "2023-11-14 05:00", "value": 11.11},
                {"date_time": "2023-11-14 05:30", "value": 5.67},
                {"date_time": "2023-11-14 06:00", "value": 12.34},
                {"date_time": "2023-11-14 06:30", "value": 6.78},
                {"date_time": "2023-11-14 07:00", "value": 8.90},
                {"date_time": "2023-11-14 07:30", "value": 9.01},
                {"date_time": "2023-11-14 08:00", "value": 2.12},
                {"date_time": "2023-11-14 08:30", "value": 13.45},
                {"date_time": "2023-11-14 09:00", "value": 3.56},
                {"date_time": "2023-11-14 09:30", "value": 14.0},
                {"date_time": "2023-11-14 10:00", "value": 1.0},
                {"date_time": "2023-11-14 10:30", "value": 5.0},
                {"date_time": "2023-11-14 11:00", "value": 8.0},
                {"date_time": "2023-11-14 11:30", "value": 11.0},
                {"date_time": "2023-11-14 12:00", "value": 2.0},
                {"date_time": "2023-11-14 12:30", "value": 6.0},
                {"date_time": "2023-11-14 13:00", "value": 10.0},
                {"date_time": "2023-11-14 13:30", "value": 14.0},
                {"date_time": "2023-11-14 14:00", "value": 3.0},
                {"date_time": "2023-11-14 14:30", "value": 7.0},
                {"date_time": "2023-11-14 15:00", "value": 11.0},
                {"date_time": "2023-11-14 15:30", "value": 1.0},
                {"date_time": "2023-11-14 16:00", "value": 4.0},
                {"date_time": "2023-11-14 16:30", "value": 8.0},
                {"date_time": "2023-11-14 17:00", "value": 12.0},
                {"date_time": "2023-11-14 17:30", "value": 2.0},
                {"date_time": "2023-11-14 18:00", "value": 6.0},
                {"date_time": "2023-11-14 18:30", "value": 10.0},
                {"date_time": "2023-11-14 19:00", "value": 14.0},
                {"date_time": "2023-11-14 19:30", "value": 3.0},
                {"date_time": "2023-11-14 20:00", "value": 7.0},
                {"date_time": "2023-11-14 20:30", "value": 11.0},
                {"date_time": "2023-11-14 21:00", "value": 1.0},
                {"date_time": "2023-11-14 21:30", "value": 4.0},
                {"date_time": "2023-11-14 22:00", "value": 8.0},
                {"date_time": "2023-11-14 22:30", "value": 12.0},
                {"date_time": "2023-11-14 23:00", "value": 2.0},
                {"date_time": "2023-11-14 23:30", "value": 6.0},
            ],
        }

        response = requests.get(
            "http://127.0.0.1:5000/search/?company=finetornos&machine_id=ABACATE&days=0"
        )
        if response.status_code == 200:
            data = response.json()

        results = sorted(
            data["results"],
            key=lambda x: datetime.strptime(x["date_time"], "%Y-%m-%d %H:%M"),
        )

        # Configurando os dados
        dates = [
            date2num(datetime.strptime(result["date_time"], "%Y-%m-%d %H:%M"))
            for result in results
        ]
        ph_values = [result["value"] for result in results]
        # Plotando os pontos no gráfico

        fig = Figure()
        ax = fig.subplots()
        ax.plot(dates, ph_values)
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.set_title("Gráfico de pH ao longo do tempo")

        ax.set_xlabel("Hora do Dia")
        ax.set_ylabel("Valor de pH")
        fig.autofmt_xdate(rotation=45)
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(DateFormatter("%d-%m %H:%m"))
        ax.legend()
        #
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        graph_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template("graph_display.html", graph_data=graph_data, data=data)
    except Exception as error:
        # Log any exceptions that occur during the execution of the route
        logging.exception("An error occurred: %s", str(error))
        # You can choose to raise the exception or handle it gracefully
        # raise e
        return error
