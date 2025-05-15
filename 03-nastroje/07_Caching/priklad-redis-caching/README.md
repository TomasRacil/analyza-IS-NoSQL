# Praktická Ukázka: Cachování s Redisem a Python Flask Aplikací

Tento příklad demonstruje použití Redisu jako cache pro jednoduchou webovou aplikaci napsanou v Pythonu pomocí frameworku Flask. Aplikace bude mít endpoint, který simuluje pomalou operaci (např. komplexní databázový dotaz nebo volání externího API), a výsledek této operace bude cachován v Redisu, aby se následné požadavky vyřídily rychleji.

## Struktura adresáře

```
priklad-redis-caching/
├── README.md (Tento soubor)
├── docker-compose.yml
└── webapp/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

## Soubory

### `docker-compose.yml`

Definuje dvě služby:
* `webapp`: Naše Python Flask aplikace.
* `redis_cache`: Instance Redis serveru, kterou bude `webapp` používat pro cachování.

### `webapp/Dockerfile`

Definuje Docker image pro Python Flask aplikaci.

### `webapp/requirements.txt`

Obsahuje závislosti pro Flask aplikaci (Flask a redis klient pro Python).

### `webapp/app.py`

Obsahuje kód Flask aplikace:
* Připojení k Redisu.
* Endpoint (např. `/data/<item_id>`), který:
    1. Zkontroluje, zda jsou data pro daný `item_id` v Redis cache.
    2. Pokud ano (cache hit), vrátí data z cache.
    3. Pokud ne (cache miss), provede simulovanou "pomalou operaci", uloží výsledek do Redis cache s nastaveným TTL (Time To Live) a vrátí výsledek.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.

## Spuštění

1.  **Otevřete terminál.**
2.  **Přejděte do adresáře** `analyza-IS-NoSQL/03-nastroje/07_Caching/priklad_redis_caching/`.
3.  **Spusťte služby pomocí Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```
    * `--build` zajistí sestavení Docker image pro webovou aplikaci.
    * `-d` spustí kontejnery na pozadí.

Služby by nyní měly běžet:
* `webapp` bude dostupná na portu `5000` hostitelského systému.
* `redis_cache` bude dostupná pro `webapp` přes interní Docker síť na názvu služby `redis_cache` a portu `6379`.

## Testování Cachování

1.  **První požadavek (Cache Miss):**
    Otevřete v prohlížeči nebo pomocí `curl` adresu:
    ```bash
    curl http://localhost:5000/data/item123
    ```
    První odpověď bude trvat déle (simulované 3 sekundy), protože data nejsou v cache. Aplikace provede "pomalou operaci" a uloží výsledek do cache.
    Očekávaná odpověď (příklad):
    ```json
    {
      "data_source": "Pomalý zdroj (databáze/API)",
      "item_id": "item123",
      "payload": "Toto jsou pomalu generovaná data pro item123",
      "timestamp": "<aktuální čas>"
    }
    ```
    V logu kontejneru `webapp_caching` ( `docker-compose logs webapp` ) byste měli vidět zprávu jako "Data pro item123 nenalezena v cache. Generuji a ukládám."

2.  **Druhý (a další) požadavek (Cache Hit):**
    Ihned poté (nebo během několika sekund, než vyprší TTL nastavené v `app.py`, např. 60 sekund) znovu zavolejte stejný endpoint:
    ```bash
    curl http://localhost:5000/data/item123
    ```
    Tato odpověď by měla být téměř okamžitá, protože data budou načtena z Redis cache.
    Očekávaná odpověď (příklad, timestamp se může lišit od prvního požadavku, pokud se cachuje i ten):
    ```json
    {
      "data_source": "Redis Cache",
      "item_id": "item123",
      "payload": "Toto jsou pomalu generovaná data pro item123",
      "timestamp": "<čas prvního generování>"
    }
    ```
    V logu kontejneru `webapp_caching` byste měli vidět zprávu jako "Data pro item123 nalezena v cache."

3.  **Požadavek na jiná data (Cache Miss):**
    Zavolejte endpoint s jiným `item_id`:
    ```bash
    curl http://localhost:5000/data/item456
    ```
    Tento požadavek opět způsobí cache miss a bude trvat déle.

4.  **Po vypršení TTL (Cache Miss):**
    Pokud počkáte déle, než je nastavené TTL pro položku v cache (v našem příkladu `app.py` to může být např. 60 sekund), a znovu zavoláte původní endpoint (`http://localhost:5000/data/item123`), mělo by opět dojít k cache miss a operace bude trvat déle, protože cachovaná položka mezitím expirovala.

5.  **Přímá kontrola Redisu (volitelné):**
    Můžete se připojit k Redis kontejneru a zkontrolovat obsah cache:
    ```bash
    docker exec -it redis_cache_server redis-cli
    ```
    Uvnitř `redis-cli`:
    ```redis
    KEYS *
    GET "cache:item123" 
    TTL "cache:item123" 
    exit
    ```

## Zastavení služeb

Pro zastavení a odstranění kontejnerů:
```bash
docker-compose down
```
Pro odstranění i volumes (Redis může ukládat data do volume, pokud je tak nakonfigurován, i když v tomto jednoduchém příkladu to není explicitně pro perzistenci dat):
```bash
docker-compose down -v
```

Tento příklad ilustruje základní princip server-side cachování pomocí strategie cache-aside a ukazuje, jak může Redis pomoci zrychlit odezvu aplikace.
