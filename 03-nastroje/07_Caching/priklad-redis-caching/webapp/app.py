from flask import Flask, jsonify
import redis
import time
import os
import logging
import json  # Pro serializaci/deserializaci komplexnějších dat do/z Redis

app = Flask(__name__)

# Nastavení logování
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Konfigurace připojení k Redisu z proměnných prostředí
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = 60  # Time To Live pro položky v cache (60 sekund)

try:
    logger.info(f"Pokouším se připojit k Redisu na {REDIS_HOST}:{REDIS_PORT}")
    # strict_decode_responses=True způsobí, že GET vrátí string, ne bytes
    redis_client = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
    )
    redis_client.ping()  # Ověření připojení
    logger.info("Úspěšně připojeno k Redisu.")
except redis.exceptions.ConnectionError as e:
    logger.error(f"Nepodařilo se připojit k Redisu: {e}")
    redis_client = None  # Nastavíme na None, abychom mohli kontrolovat v endpointu


def get_slow_data_from_source(item_id: str) -> dict:
    """
    Simuluje pomalé načítání dat z primárního zdroje (např. databáze, externí API).
    """
    logger.info(f"Generuji pomalá data pro item_id: {item_id}...")
    time.sleep(3)  # Simulace pomalé operace (3 sekundy)
    data = {
        "item_id": item_id,
        "payload": f"Toto jsou pomalu generovaná data pro {item_id}",
        "timestamp": time.time(),  # Časové razítko generování
    }
    logger.info(f"Pomalá data pro item_id: {item_id} vygenerována.")
    return data


@app.route("/")
def index():
    return jsonify(
        message="Flask Webapp s Redis Cache je spuštěna. Zkuste /data/<item_id>"
    )


@app.route("/data/<item_id>")
def get_data_endpoint(item_id: str):
    if not redis_client:
        logger.error("Redis klient není dostupný. Vracím data z pomalého zdroje.")
        slow_data = get_slow_data_from_source(item_id)
        return jsonify({**slow_data, "data_source": "Pomalý zdroj (Redis nedostupný)"})

    cache_key = f"cache:{item_id}"

    try:
        # 1. Pokus o načtení dat z Redis cache
        cached_data_json = redis_client.get(cache_key)

        if cached_data_json:
            # Cache Hit
            logger.info(f"Data pro {item_id} nalezena v cache.")
            cached_data = json.loads(cached_data_json)  # Deserializace JSON stringu
            return jsonify({**cached_data, "data_source": "Redis Cache"})
        else:
            # Cache Miss
            logger.info(f"Data pro {item_id} nenalezena v cache. Generuji a ukládám.")

            # 2. Načtení/generování dat z primárního zdroje
            actual_data = get_slow_data_from_source(item_id)

            # 3. Uložení dat do Redis cache s TTL
            # Serializujeme slovník na JSON string před uložením do Redisu
            redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(actual_data))
            logger.info(
                f"Data pro {item_id} uložena do cache s TTL {CACHE_TTL_SECONDS}s."
            )

            return jsonify(
                {**actual_data, "data_source": "Pomalý zdroj (databáze/API)"}
            )

    except redis.exceptions.RedisError as e:
        logger.error(
            f"Chyba při komunikaci s Redisem: {e}. Vracím data z pomalého zdroje."
        )
        # Fallback na pomalý zdroj v případě chyby Redisu
        slow_data = get_slow_data_from_source(item_id)
        return jsonify({**slow_data, "data_source": f"Pomalý zdroj (Redis chyba: {e})"})
    except Exception as e:
        logger.error(f"Neočekávaná chyba: {e}", exc_info=True)
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    # Flask defaultně běží na portu 5000.
    # host='0.0.0.0' zajistí, že je server dostupný zvenčí kontejneru.
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug=True pro vývoj
