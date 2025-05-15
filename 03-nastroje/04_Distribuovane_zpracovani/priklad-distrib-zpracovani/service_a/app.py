from flask import Flask, jsonify
import requests
import os
import logging

app = Flask(__name__)

# Nastavení logování
logging.basicConfig(level=logging.INFO)

# Získání URL služby B z proměnné prostředí
# Docker Compose předá tuto proměnnou při spuštění kontejneru.
SERVICE_B_URL = os.environ.get(
    "SERVICE_B_URL", "http://localhost:5002"
)  # Fallback pro lokální testování mimo Docker


@app.route("/")
def hello_service_a():
    return jsonify(message="Toto je služba A!")


@app.route("/call_service_b")
def call_service_b():
    """
    Endpoint, který zavolá /data endpoint na službě B.
    """
    target_url = f"{SERVICE_B_URL}/data"
    app.logger.info(f"Služba A volá službu B na adrese: {target_url}")
    try:
        response_from_b = requests.get(target_url, timeout=5)  # Timeout 5 sekund
        response_from_b.raise_for_status()  # Vyvolá chybu pro HTTP status kódy 4xx/5xx

        data_from_b = response_from_b.json()
        app.logger.info(f"Služba A obdržela od služby B: {data_from_b}")

        return jsonify(
            {
                "response_from_a": "Služba A obdržela odpověď od služby B.",
                "data_from_b": data_from_b,
            }
        )
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Chyba při volání služby B: {e}")
        return (
            jsonify(error=f"Nepodařilo se kontaktovat službu B: {str(e)}"),
            503,
        )  # Service Unavailable


if __name__ == "__main__":
    # Flask defaultně běží na portu 5000
    # Při spuštění přes `flask run` se použije host 0.0.0.0, aby byla aplikace dostupná zvenčí kontejneru.
    app.run(host="0.0.0.0", port=5000)
