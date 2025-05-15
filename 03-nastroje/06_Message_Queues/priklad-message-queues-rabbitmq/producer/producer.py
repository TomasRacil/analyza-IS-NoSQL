# SOUBOR: analyza-IS-NoSQL/03-nastroje/06_Message_Queues/priklad_message_queues_rabbitmq/producer/producer.py
import pika
import time
import os
import logging
import sys  # Pro sys.exit

# Nastavení logování
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s: %(name)s:%(message)s"
)
logger = logging.getLogger(__name__)

# Nastavení úrovně logování pro knihovnu 'pika' na WARNING
logging.getLogger("pika").setLevel(logging.WARNING)

# Získání hostname RabbitMQ z proměnné prostředí, s fallbackem pro lokální testování
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "hello_queue"
MESSAGE_INTERVAL_SECONDS = 2  # Interval mezi odesláním zpráv


def connect_rabbitmq():
    """Pokusí se připojit k RabbitMQ s několika opakováními."""
    attempts = 0
    max_attempts = 10
    wait_time = 5  # sekundy

    while attempts < max_attempts:
        try:
            logger.info(
                f"Pokus o připojení k RabbitMQ na {RABBITMQ_HOST} (pokus {attempts + 1}/{max_attempts})..."
            )
            connection_params = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                heartbeat=600,  # Vyšší heartbeat pro delší neaktivitu
                blocked_connection_timeout=300,  # Timeout pro blokované spojení
            )
            connection = pika.BlockingConnection(connection_params)
            logger.info("Úspěšně připojeno k RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logger.warning(
                f"Připojení k RabbitMQ selhalo: {e}. Další pokus za {wait_time}s."
            )
            attempts += 1
            time.sleep(wait_time)

    logger.error(f"Nepodařilo se připojit k RabbitMQ po {max_attempts} pokusech.")
    return None


def main():
    connection = connect_rabbitmq()
    if not connection:
        sys.exit(1)  # Ukončíme skript, pokud se nepodaří připojit

    channel = connection.channel()

    try:
        # Deklarace fronty (pokud neexistuje, vytvoří se)
        # durable=True znamená, že fronta přežije restart RabbitMQ serveru
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        logger.info(
            f"Fronta '{QUEUE_NAME}' je připravena. Producent začíná odesílat zprávy..."
        )

        message_counter = 0
        while True:
            message_counter += 1
            message_body = f"Kontinuální zpráva č. {message_counter} od producenta"

            try:
                # Publikování zprávy do fronty
                channel.basic_publish(
                    exchange="",
                    routing_key=QUEUE_NAME,
                    body=message_body,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    ),
                )
                logger.info(f"[x] Odesláno '{message_body}'")
            except pika.exceptions.AMQPConnectionError:
                logger.error(
                    "Spojení s RabbitMQ bylo ztraceno. Pokouším se znovu připojit..."
                )
                connection.close()  # Uzavřeme staré, potenciálně nefunkční spojení
                connection = connect_rabbitmq()
                if not connection:
                    logger.error("Nepodařilo se znovu připojit. Ukončuji producenta.")
                    break  # Ukončíme while smyčku
                channel = connection.channel()
                # Znovu deklarujeme frontu pro případ, že by nové spojení vyžadovalo nový kanál
                channel.queue_declare(queue=QUEUE_NAME, durable=True)
                logger.info(
                    "Znovu připojeno a fronta deklarována. Pokračuji v odesílání."
                )
                # Zkusíme znovu odeslat aktuální zprávu
                channel.basic_publish(
                    exchange="",
                    routing_key=QUEUE_NAME,
                    body=message_body,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    ),
                )
                logger.info(f"[x] Znovu odesláno (po re-připojení) '{message_body}'")

            except Exception as e:
                logger.error(f"Neočekávaná chyba při odesílání zprávy: {e}")
                # Můžeme zde přidat logiku pro přerušení smyčky nebo další pokusy
                time.sleep(5)  # Krátká pauza před dalším pokusem nebo ukončením
                continue  # Pokračujeme na další iteraci, nebo můžeme přidat break

            time.sleep(MESSAGE_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Producent ukončen uživatelem (CTRL+C).")
    except Exception as e:
        logger.error(f"Nastala neočekávaná chyba v producentovi: {e}", exc_info=True)
    finally:
        if connection and connection.is_open:
            try:
                logger.info("Uzavírám spojení s RabbitMQ...")
                connection.close()
                logger.info("Spojení s RabbitMQ producenta úspěšně uzavřeno.")
            except Exception as e:
                logger.error(
                    f"Chyba při uzavírání spojení s RabbitMQ v producentovi: {e}",
                    exc_info=True,
                )
        else:
            logger.info("Spojení s RabbitMQ již bylo uzavřeno nebo nebylo navázáno.")


if __name__ == "__main__":
    # Malá pauza na start RabbitMQ, i když depends_on s healthcheck by to měl řešit
    time.sleep(5)
    main()
