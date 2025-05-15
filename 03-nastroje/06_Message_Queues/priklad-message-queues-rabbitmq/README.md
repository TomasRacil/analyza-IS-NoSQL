# Praktická Ukázka: Fronty Zpráv s RabbitMQ a Pythonem

Tento příklad demonstruje základní použití RabbitMQ jako message brokera s jednoduchým Python producentem, který odesílá zprávy, a Python konzumentem, který tyto zprávy přijímá a zpracovává. Vše je spravováno pomocí Docker Compose.

## Struktura adresáře

```
priklad-message-queues-rabbitmq/
├── README.md (Tento soubor)
├── docker-compose.yml
├── producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── producer.py
└── consumer/
    ├── Dockerfile
    ├── requirements.txt
    └── consumer.py
```

## Soubory

### `docker-compose.yml`

Definuje tři služby:
* `rabbitmq`: Instance RabbitMQ serveru s management pluginem (pro webové rozhraní).
* `producer`: Python aplikace, která odesílá zprávy do RabbitMQ.
* `consumer`: Python aplikace, která přijímá zprávy z RabbitMQ.

### `producer/Dockerfile` a `producer/producer.py`

* `Dockerfile`: Definuje Docker image pro Python producenta.
* `producer.py`: Skript, který se připojí k RabbitMQ, deklaruje frontu a odesílá do ní několik zpráv.

### `consumer/Dockerfile` a `consumer/consumer.py`

* `Dockerfile`: Definuje Docker image pro Python konzumenta.
* `consumer.py`: Skript, který se připojí k RabbitMQ, deklaruje stejnou frontu a začne z ní odebírat a "zpracovávat" zprávy.

### `producer/requirements.txt` a `consumer/requirements.txt`

Obsahují závislost na knihovně `pika`, což je Python klient pro RabbitMQ.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.

## Spuštění

1.  **Otevřete terminál.**
2.  **Přejděte do adresáře** `analyza-IS-NoSQL/03-nastroje/06_Message_Queues/priklad_message_queues_rabbitmq/`.
3.  **Spusťte služby pomocí Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    * `--build` zajistí sestavení Docker obrazů pro producenta i konzumenta.
    * Tento příkaz spustí všechny služby na popředí, takže uvidíte jejich logy.

## Očekávané chování a testování

Po spuštění byste měli v terminálu vidět následující:

1.  **RabbitMQ server** nastartuje a bude dostupný.
    * Management konzole RabbitMQ bude dostupná na `http://localhost:15672` (přihlašovací jméno: `guest`, heslo: `guest`). Zde můžete sledovat fronty, spojení atd.

2.  **Producent (`producer`)** se spustí, připojí k RabbitMQ, vytvoří (nebo potvrdí existenci) fronty `hello_queue` a odešle do ní několik zpráv (např. "Zprava 1", "Zprava 2", ...). Po odeslání všech zpráv se producent ukončí. V jeho logu uvidíte něco jako:
    ```
    producer_1  | [x] Odesláno 'Zprava 1 od producenta'
    producer_1  | [x] Odesláno 'Zprava 2 od producenta'
    ...
    producer_1  | Všechny zprávy odeslány. Producent se ukončuje.
    ```

3.  **Konzument (`consumer`)** se spustí, připojí k RabbitMQ, připojí se ke frontě `hello_queue` a začne čekat na zprávy. Jakmile producent odešle zprávy, konzument je začne přijímat a "zpracovávat" (v tomto příkladu je pouze vypíše). V jeho logu uvidíte:
    ```
    consumer_1  | [*] Čekání na zprávy ve frontě 'hello_queue'. Pro ukončení stiskněte CTRL+C
    consumer_1  | [x] Přijato: Zprava 1 od producenta
    consumer_1  | [x] Zpracováno: Zprava 1 od producenta
    consumer_1  | [x] Přijato: Zprava 2 od producenta
    consumer_1  | [x] Zpracováno: Zprava 2 od producenta
    ...
    ```
    Konzument bude běžet a čekat na další zprávy, dokud ho manuálně neukončíte (např. `Ctrl+C` v terminálu, kde běží `docker-compose up`).

### Experimentování

* **Spusťte více konzumentů:** Můžete škálovat službu `consumer` pomocí Docker Compose, abyste viděli, jak se zprávy rozkládají mezi více konzumentů (každá zpráva by měla být zpracována pouze jedním z nich v tomto point-to-point nastavení).
    Otevřete nový terminál (zatímco původní `docker-compose up` stále běží, nebo ho ukončete a spusťte služby na pozadí s `-d`) a spusťte:
    ```bash
    docker-compose up --scale consumer=3
    ```
    Sledujte logy jednotlivých konzumentů.

* **Perzistence zpráv:** Upravte kód producenta a deklaraci fronty tak, aby byly zprávy perzistentní. Zastavte a restartujte RabbitMQ a ověřte, zda nezpracované zprávy ve frontě zůstaly.

* **Potvrzování zpráv (Acknowledgements):** Prozkoumejte, jak funguje manuální potvrzování zpráv v konzumentovi. Pokud konzument spadne před potvrzením, zpráva by se měla vrátit do fronty.

## Zastavení služeb

Pokud jste služby spustili na popředí, stiskněte `Ctrl+C` v terminálu.
Pokud běžely na pozadí (s `-d`), použijte:
```bash
docker-compose down
```
Pro odstranění i volumes (RabbitMQ ukládá data do volume):
```bash
docker-compose down -v
```

Tento příklad poskytuje základní demonstraci asynchronní komunikace pomocí front zpráv s RabbitMQ.
