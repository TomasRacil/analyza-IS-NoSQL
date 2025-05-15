import pika
import time
import os
import logging

# Nastavení logování
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Získání hostname RabbitMQ z proměnné prostředí, s fallbackem pro lokální testování
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "hello_queue"


def connect_rabbitmq():
    """Pokusí se připojit k RabbitMQ s několika opakováními."""
    attempts = 0
    max_attempts = 10
    wait_time = 5  # sekundy

    while attempts < max_attempts:
        try:
            logging.info(
                f"Pokus o připojení k RabbitMQ na {RABBITMQ_HOST} (pokus {attempts + 1}/{max_attempts})..."
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            logging.info("Úspěšně připojeno k RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(
                f"Připojení k RabbitMQ selhalo: {e}. Další pokus za {wait_time}s."
            )
            attempts += 1
            time.sleep(wait_time)

    logging.error(f"Nepodařilo se připojit k RabbitMQ po {max_attempts} pokusech.")
    return None


def callback(ch, method, properties, body):
    """
    Funkce, která se zavolá při přijetí zprávy.
    Simuluje zpracování zprávy.
    """
    message = body.decode()
    logging.info(f"[x] Přijato: {message}")

    # Simulace zpracování zprávy
    processing_time = len(message) % 3 + 1  # Zpracování trvá 1-3 sekundy
    logging.info(f"    Zpracovávám zprávu... (potrvá {processing_time}s)")
    time.sleep(processing_time)

    logging.info(f"[x] Zpracováno: {message}")

    # Potvrzení zpracování zprávy (acknowledgement)
    # Tím se zpráva odstraní z fronty. Pokud by konzument spadl před tímto krokem,
    # zpráva by se vrátila do fronty (nebo byla doručena jinému konzumentovi).
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = connect_rabbitmq()
    if not connection:
        return

    channel = connection.channel()

    # Deklarace fronty (ujistíme se, že existuje a má stejné vlastnosti jako u producenta)
    # durable=True je důležité, aby fronta přežila restart RabbitMQ
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    logging.info(f"Fronta '{QUEUE_NAME}' je připravena.")

    # Nastavení prefetch_count=1 zajistí, že RabbitMQ nepošle konzumentovi více než jednu
    # zprávu najednou, dokud konzument nepotvrdí zpracování předchozí.
    # To je užitečné pro rozložení zátěže, pokud máme více konzumentů.
    channel.basic_qos(prefetch_count=1)

    # Nastavení konzumenta pro příjem zpráv z fronty
    # auto_ack=False znamená, že budeme zprávy potvrzovat manuálně (pomocí ch.basic_ack)
    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False
    )

    logging.info(
        f"[*] Čekání na zprávy ve frontě '{QUEUE_NAME}'. Pro ukončení stiskněte CTRL+C"
    )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Konzument ukončen uživatelem (CTRL+C).")
    except Exception as e:
        logging.error(f"Nastala chyba v konzumentovi: {e}")
    finally:
        if connection and not connection.is_closed:
            try:
                connection.close()
                logging.info("Spojení s RabbitMQ uzavřeno.")
            except Exception as e:
                logging.error(f"Chyba při uzavírání spojení: {e}")


if __name__ == "__main__":
    # Malá pauza na start RabbitMQ
    time.sleep(10)
    main()
