from flask import Flask, jsonify
import logging
import time  # Pro simulaci zpoždění
import os  # Pro získání hostname (ID podu)

app = Flask(__name__)

# Nastavení logování
logging.basicConfig(level=logging.INFO)

# Získání hostname, což v Kubernetes bude název podu
pod_name = os.environ.get("HOSTNAME", "unknown_pod")


@app.route("/")
def hello_service_b():
    return jsonify(message=f"Toto je služba B! (Pod: {pod_name})")


@app.route("/data")
def get_data():
    """
    Jednoduchý endpoint, který vrací nějaká data a simuluje zpoždění.
    """
    processing_time = 2  # Simulace zpoždění 2 sekundy
    app.logger.info(
        f"Služba B (Pod: {pod_name}): Endpoint /data byl zavolán. Zpracování potrvá {processing_time}s."
    )
    time.sleep(processing_time)  # Umělé zpoždění

    response_data = {
        "message_from_b": "Data ze služby B",
        "source": "service_b",
        "version": "1.0.0",
        "processed_by_pod": pod_name,  # Přidáme jméno podu, který požadavek zpracoval
    }
    app.logger.info(f"Služba B (Pod: {pod_name}): Odpovídám s: {response_data}")
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
