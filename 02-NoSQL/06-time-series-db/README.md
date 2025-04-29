# Time Series Databáze (TSDB)

## 1 Time Series Databáze: Teorie

### 1.1 Datový Model

Time Series databáze (TSDB) jsou specializované databáze optimalizované pro ukládání a práci s *časovými řadami*. Časová řada je sekvence datových bodů indexovaných (nebo seřazených) v časovém pořadí.  Každý datový bod se skládá z *timestampu* (časového razítka) a jedné nebo více *hodnot*. TSDB jsou navrženy tak, aby efektivně zvládaly:

*   **Vysoký objem zápisů:** Neustálý proud dat z různých zdrojů.
*   **Dotazy zaměřené na časové intervaly:** Rychlé vyhledávání a agregace dat v daném časovém rozmezí.
*   **Data s časovou platností:**  Často je potřeba ukládat data jen po omezenou dobu (např. metrik z posledního měsíce).

**Základní pojmy:**

*   **Metrika (Metric):**  Název měřené veličiny (např. `cpu_usage`, `temperature`, `stock_price`).  V kontextu TSDB se metrika často chápe jako ekvivalent "tabulky".
*   **Timestamp (Časové razítko):**  Okamžik, kdy byla hodnota naměřena.  Obvykle se používá Unixový timestamp (počet sekund/milisekund od 1. ledna 1970, 00:00:00 UTC) nebo formát ISO 8601 (např. `2024-07-24T10:30:00Z`).  Přesnost timestampu může být různá (sekundy, milisekundy, mikrosekundy, nanosekundy) v závislosti na potřebách aplikace a možnostech TSDB.
*   **Hodnota (Value):** Naměřená hodnota metriky v daném čase.  Může být číselná (integer, float), textová, logická (boolean), nebo i složitější datový typ (např. histogram).
*   **Tag (Značka, Štítek, Atribut):**  Klíč-hodnota pár, který poskytuje *kontext* k datovému bodu.  Tagy se používají pro *dimenzionalitu* dat. Umožňují filtrovat, seskupovat a agregovat data. Například:
    *   `host=server1`
    *   `region=us-east-1`
    *   `sensor_id=abc123`
    *   `status=active`
    *   Tagy *neobsahují* časové razítko.
*   **Série (Series):**  Unikátní kombinace metriky a tagů.  Například:
    *   `cpu_usage{host=server1, region=us-east-1}`
    *   `cpu_usage{host=server2, region=us-west-2}`
    *   Každá série je *samostatná* časová řada. TSDB je optimalizovaná pro práci s *velkým počtem sérií*.
*   **Retention Policy (Zásady uchovávání dat):** Pravidla, která určují, jak dlouho se data v databázi uchovávají. Starší data se automaticky mažou nebo přesouvají do levnějšího úložiště (downsampling).

**Příklad (konceptuální):**

```
Metric: temperature
  Series: temperature{sensor=sensor1, location=room1}
    Timestamp: 2024-07-24T10:00:00Z, Value: 22.5
    Timestamp: 2024-07-24T10:01:00Z, Value: 22.7
    Timestamp: 2024-07-24T10:02:00Z, Value: 22.9
  Series: temperature{sensor=sensor2, location=room2}
    Timestamp: 2024-07-24T10:00:00Z, Value: 25.1
    Timestamp: 2024-07-24T10:01:00Z, Value: 25.3
    Timestamp: 2024-07-24T10:02:00Z, Value: 25.0
```

*   `temperature` je metrika.
*   `sensor` a `location` jsou tagy.
*   `temperature{sensor=sensor1, location=room1}` a `temperature{sensor=sensor2, location=room2}` jsou dvě *různé* série.
*   Každý řádek v sérii je datový bod s timestampem a hodnotou.

**Klíčové vlastnosti TSDB modelu:**

*   **Optimalizováno pro čas:**  Celý datový model a interní struktura jsou navrženy pro efektivní práci s časem.
*   **Vysoká komprese:**  TSDB používají pokročilé kompresní algoritmy, aby minimalizovaly nároky na úložný prostor (protože časové řady často obsahují redundantní data).
*   **Downsampling:**  Automatické agregace dat na nižší rozlišení (např. minutové hodnoty se agregují na hodinové průměry) pro dlouhodobé uchovávání dat.  Snižuje nároky na úložiště a zrychluje dotazy na starší data.
*   **Rychlé dotazy v časových intervalech:**  TSDB jsou navrženy pro rychlé vyhledávání dat v zadaném časovém rozmezí, např. "dej mi průměrnou teplotu za poslední hodinu".
*   **Agregace:**  Podporují rychlé agregace (např. `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`, percentily) přes časové intervaly a různé série.
*   **Filtrování podle tagů:**  Umožňují filtrovat data podle tagů, např. "dej mi teplotu ze všech senzorů v místnosti room1".
*   **Horizontální škálovatelnost:**  Většina TSDB je navržena pro distribuované prostředí a snadno se škálují horizontálně.

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Vysoký výkon pro zápis:** Zvládají vysoký objem dat z mnoha zdrojů.
*   **Rychlé dotazy v časových intervalech:** Optimalizované pro vyhledávání a agregaci dat v čase.
*   **Efektivní ukládání:**  Pokročilé kompresní algoritmy a downsampling.
*   **Škálovatelnost:**  Dobře se škálují horizontálně.
*   **Specializované funkce:**  Nabízí funkce specifické pro práci s časovými řadami (např. interpolace, extrapolace, vyhlazování).
*   **Snadné smazání starých dat:** Retention policy automaticky maže stará data.

**Nevýhody:**

*   **Méně flexibilní než relační databáze:** Nejsou vhodné pro složité relační dotazy (JOINy).
*   **Omezená podpora transakcí:**  Obvykle nepodporují plné ACID transakce.
*   **Složitější aktualizace a mazání *jednotlivých* datových bodů:**  TSDB jsou primárně určeny pro *přidávání* nových dat, ne pro časté aktualizace nebo mazání *existujících* dat.
*   **Nevhodné pro obecné účely:**  Nejsou univerzální databází.  Jsou specializované na časové řady.

### 1.3 Příklady Time Series Databází

*   **InfluxDB:**  Populární open-source TSDB.  Má vlastní dotazovací jazyk InfluxQL (podobný SQL) a Flux (modernější, funkcionální jazyk).  Snadno se používá a má dobrou dokumentaci.  Existuje i placená cloudová verze (InfluxDB Cloud).
*   **Prometheus:**  Open-source systém pro monitoring a alerting, který *obsahuje* integrovanou TSDB.  Používá dotazovací jazyk PromQL.  Je velmi populární v prostředí Kubernetes.
*   **TimescaleDB:**  Open-source TSDB *postavená nad PostgreSQL*.  Používá SQL s rozšířeními pro časové řady.  Výhodou je, že můžete využívat všechny funkce PostgreSQL (včetně JOINů a transakcí).
*   **OpenTSDB:**  Open-source TSDB postavená nad HBase (Hadoop).  Vhodná pro velmi velké datasety.
*   **Graphite:**  Starší open-source TSDB.  Stále se používá, ale má omezenější funkce a škálovatelnost než novější řešení.
*   **Amazon Timestream:**  Plně spravovaná TSDB na AWS.
*   **Azure Time Series Insights:**  Služba od Microsoftu pro analýzu IoT dat.
* **VictoriaMetrics:** Vysoce výkonná, nákladově efektivní a škálovatelná open-source monitorovací a time-series databáze.

### 1.4 Kdy je TSDB lepší volbou než relační nebo NoSQL databáze?

*   **Ukládání a analýza časových řad:**  To je primární účel TSDB.  Pokud máte data, která se mění v čase (např. data ze senzorů, metriky aplikací, finanční data, logy), TSDB je obvykle nejlepší volba.
*   **Vysoký objem zápisů:**  Pokud potřebujete zapisovat velké množství dat v reálném čase.
*   **Dotazy zaměřené na časové intervaly:**  Pokud potřebujete rychle vyhledávat a agregovat data v zadaném časovém rozmezí.
*   **Monitoring a alerting:**  TSDB se často používají pro monitoring systémů a aplikací a pro generování alertů (upozornění) na základě definovaných pravidel.
* **IoT (Internet of Things):** Pro ukládání dat ze senzorů a dalších zařízení.
* **Průmyslová automatizace:** Pro ukládání dat z výrobních linek a dalších průmyslových systémů.
* **Finanční analýza:** Pro ukládání a analýzu kurzů akcií, komodit a dalších finančních instrumentů.

**Kdy TSDB *není* dobrá volba:**

*   **Aplikace vyžadující silné ACID transakce přes více tabulek/entit.**
*   **Aplikace s komplexními vztahy mezi daty, kde jsou časté JOINy.**
*   **Aplikace, kde potřebujete často *aktualizovat* nebo *mazat* jednotlivé datové body.**  TSDB jsou optimalizovány pro *přidávání* nových dat.
*   **Obecné ukládání dat:**  Pokud nepotřebujete specifické funkce pro práci s časovými řadami, může být vhodnější relační nebo NoSQL databáze.

## 2. InfluxDB v2.x: Praktický Příklad

Tento příklad ukazuje, jak nastavit InfluxDB v2.x pomocí Dockeru a jak s ní interagovat pomocí **InfluxDB v2 CLI**, **Flux** dotazovacího jazyka a **Line Protocolu**. Zaměříme se na interaktivní práci v shellu uvnitř kontejneru a zmíníme i webové rozhraní.

### Struktura

* **`docker-compose.yml`:** Definuje službu InfluxDB v2.x (verze 2.7). Při prvním spuštění automaticky nastaví uživatele, organizaci, bucket a token podle proměnných prostředí.

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**
2.  **Otevřete terminál** a přejděte do tohoto adresáře.
3.  **Spusťte kontejnery:**

    ```bash
    docker-compose up -d
    ```

    Počkejte chvíli, než InfluxDB plně nastartuje a provede úvodní nastavení.

### 2.1 Práce s InfluxDB v2 CLI (Interaktivní Shell)

Nejpohodlnější způsob, jak experimentovat a učit se, je pracovat přímo v `bash` shellu uvnitř kontejneru `influxdb`. Nejprve si nastavíme konfiguraci CLI, abychom nemuseli opakovaně zadávat token a další parametry.

1.  **Spusťte interaktivní `bash` shell uvnitř kontejneru `influxdb`:**
    ```bash
    docker exec -it influxdb bash
    ```
    *(Všechny následující příkazy v této sekci zadávejte *uvnitř* tohoto shellu, pokud není uvedeno jinak.)*

2.  **Nastavte konfiguraci pro `influx` CLI:**
    Použijte hodnoty z `docker-compose.yml` (token: `my-super-secret-token`, org: `myorg`, url: `http://localhost:8086`). Nahraďte hodnoty, pokud jste je v `docker-compose.yml` změnili.
    ```bash
    # Tento příkaz stačí spustit jen jednou po prvním spuštění kontejneru
    influx config create --config-name myconfig \
      --host-url http://localhost:8086 \
      --org myorg \
      --token my-super-secret-token \
      --active
    ```
    * `--config-name`: Jméno pro vaši konfiguraci (libovolné).
    * `--host-url`: Adresa běžící InfluxDB instance.
    * `--org`: Název vaší organizace.
    * `--token`: Váš API token.
    * `--active`: Nastaví tuto konfiguraci jako aktivní pro další příkazy.
    * Nyní je CLI nakonfigurováno a připraveno k použití.

#### Základní operace (uvnitř `bash` shellu kontejneru)

* **Ověření stavu:**
    ```bash
    # Ping serveru (ověří připojení a konfiguraci)
    influx ping
    ```

* **Správa Bucketů:**
    * V InfluxDB v2.x se data ukládají do *bucketů*. Každý bucket má název a definovanou dobu uchovávání dat (retention).
    * Bucket `mybucket` byl vytvořen automaticky při startu.
    * **Výpis existujících bucketů:**
        ```bash
        influx bucket list
        # Měli byste vidět '_monitoring', '_tasks' a 'mybucket'
        ```
    * **Vytvoření nového bucketu (např. `testbucket` s uchováváním dat 7 dní):**
        ```bash
        influx bucket create -n testbucket --retention 7d
        ```
        * `-n`: Název bucketu.
        * `--retention`: Doba uchovávání dat (např. `7d`, `30d`, `0` pro nekonečnou).
        * Organizace (`-o`) a token (`-t`) se použijí z aktivní konfigurace.
    * **Aktualizace doby uchovávání pro bucket:**
        ```bash
        # Získání ID bucketu 'testbucket'
        influx bucket update --id $(influx bucket list --name testbucket --json | grep \"id\" | cut -d '"' -f 4) --retention 30d
        ```
        * `--id`: ID bucketu, který chceme aktualizovat. Získáváme ho poddotazem.
        * `--retention`: Nová doba uchovávání.

* **Zápis dat (Line Protocol):**
    * Data se zapisují pomocí příkazu `influx write` a **Line Protocolu**.
    * Formát Line Protocolu: `<measurement>[,<tag_key>=<tag_value>...] <field_key>=<field_value>[,<field_key2>=<field_value2>...] [timestamp]`
    * **Zápis datových bodů do `mybucket`:**
        ```bash
        # Zápis jednoho bodu (timestamp se doplní automaticky)
        influx write -b mybucket 'cpu,host=server1,region=us-east value=0.64'

        # Zápis s explicitním timestampem (v nanosekundách!) - Ekvivalent 1678886400 sekund
        influx write -b mybucket 'cpu,host=server1,region=us-east value=0.72 1678886400000000000'

        # Zápis více polí
        influx write -b mybucket 'temperature,location=room1,sensor=sensor1 value=22.5,humidity=55.2'

        # Zápis více bodů najednou (pomocí $'' pro interpretaci \n)
        influx write -b mybucket $'cpu,host=server2,region=us-west value=0.55\ncpu,host=server2,region=us-west value=0.58 1678886500000000000'
        ```
        * `-b`: Název cílového bucketu.

* **Dotazování (Flux):**
    * Používá se příkaz `influx query` a dotazovací jazyk **Flux**.
    * **Získání všech dat z measurementu `cpu`:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: 0) |> filter(fn: (r) => r._measurement == "cpu")'
        ```
        * `from(bucket: "...")`: Určuje zdrojový bucket.
        * `range(start: 0)`: Časový rozsah od počátku času InfluxDB.
        * `filter(fn: (r) => ...)`: Filtruje záznamy podle podmínek. `r` reprezentuje jeden záznam.
        * `|>`: Pipe-forward operátor, posílá výstup předchozí funkce na vstup další.
    * **Získání dat pro konkrétní host:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: 0) |> filter(fn: (r) => r._measurement == "cpu" and r.host == "server1")'
        ```
    * **Získání dat za poslední hodinu:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")'
        ```
    * **Výpočet průměrné hodnoty `value` za poslední hodinu, seskupeno po 10 minutách:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value") |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)'
        ```
        * `aggregateWindow()`: Funkce pro agregaci dat v časových oknech.
        * `every: 10m`: Velikost okna (10 minut).
        * `fn: mean`: Agregační funkce (průměr).
    * **Výpočet průměrné hodnoty, seskupeno po 10 minutách a hostu:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value") |> group(columns: ["host"]) |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)'
        ```
        * `group(columns: ["host"])`: Seskupí data podle hodnoty tagu `host`.
    * **Kumulativní suma:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: 0) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value") |> cumulativeSum()'
        ```
    * **Derivace (rychlost změny):**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: -5m) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value") |> derivative(unit: 1s, nonNegative: true)'
        ```
    * **Poslední hodnota:**
        ```bash
        influx query 'from(bucket: "mybucket") |> range(start: 0) |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value") |> last()'
        ```
    * **Filtrování pomocí regulárního výrazu:**
        ```bash
        influx query 'import "regexp" from(bucket: "mybucket") |> range(start: 0) |> filter(fn: (r) => r._measurement == "cpu" and regexp.matchRegexpString(r: r.host, regexp: "server[1-3]"))'
        ```

* **Mazání dat:**
    * Používá se příkaz `influx delete`. Mazání se provádí na základě časového rozsahu a predikátu (filtru).
    * **Smazání dat pro `host=server1` z measurementu `cpu` v bucketu `mybucket`:**
        ```bash
        # Pozor: Toto smaže VŠECHNA data pro daný predikát v daném rozsahu! Buďte opatrní!
        # Formát času: RFC3339 např. '2023-01-01T00:00:00Z' nebo relativní '-1h', '-7d'
        influx delete -b mybucket --start '1970-01-01T00:00:00Z' --stop $(date +%Y-%m-%dT%H:%M:%SZ) --predicate '_measurement="cpu" AND host="server1"'
        ```
        * `-b`: Cílový bucket.
        * `--start`, `--stop`: Časový rozsah pro mazání.
        * `--predicate`: Filtr (Flux syntaxe) určující, která data se mají smazat.
    * **Smazání všech dat z measurementu `cpu`:**
        ```bash
        influx delete -b mybucket --start '1970-01-01T00:00:00Z' --stop $(date +%Y-%m-%dT%H:%M:%SZ) --predicate '_measurement="cpu"'
        ```

* **Správa uživatelů a tokenů:**
    * **Výpis uživatelů:**
        ```bash
        influx user list
        ```
    * **Vytvoření nového API tokenu (např. jen pro čtení `mybucket`):**
        ```bash
        # Získání ID bucketu 'mybucket'
        influx auth create --org myorg --read-bucket $(influx bucket list --name mybucket --json | grep \"id\" | cut -d '"' -f 4) --description "Read-only token for mybucket"
        ```
        Tento příkaz vrátí nový token. Zkopírujte si ho, budete ho potřebovat pro autentizaci operací s tímto omezeným oprávněním.

* **Ukončení interaktivního shellu:**
    ```bash
    exit
    ```

### 2.2 Webové rozhraní InfluxDB (UI)

Kromě CLI poskytuje InfluxDB v2.x také **webové uživatelské rozhraní (UI)**, které je velmi užitečné pro vizualizaci dat, správu a některé pokročilejší úkony.

* **Přístup:** Po spuštění kontejneru pomocí `docker-compose up -d` je webové rozhraní dostupné ve vašem prohlížeči na adrese:
    **`http://localhost:8086`**
* **Přihlášení:** Použijte uživatelské jméno a heslo definované v `docker-compose.yml`:
    * Uživatelské jméno: `admin`
    * Heslo: `password` (nebo jaké jste si nastavili)
* **Hlavní funkce:**
    * **Data Explorer:** Umožňuje interaktivně vytvářet Flux dotazy (pomocí grafického editoru nebo přímým psaním kódu), vizualizovat výsledky v grafech a tabulkách a ukládat dotazy jako dashboardy. Skvělé pro prozkoumávání dat.
    * **Dashboards:** Vytváření a správa dashboardů s vizualizacemi vašich dat.
    * **Load Data (Buckets):** Správa bucketů (vytváření, mazání, úprava retention period). Můžete zde také spravovat tokeny a další zdroje dat (např. Telegraf konfigurace).
    * **Tasks:** Vytváření a správa úloh (Tasks) pro automatické zpracování dat (např. downsampling, alerty).
    * **Alerts:** Definování pravidel pro upozornění (alerting) na základě dat.
    * **Settings:** Správa organizací, uživatelů a dalších nastavení InfluxDB.

Webové rozhraní je skvělým doplňkem k CLI, zejména pro vizuální analýzu a konfiguraci složitějších prvků jako jsou Tasks a Alerts.

### 2.3 Pokročilejší Flux dotazy

Flux je výkonný jazyk. Zde je pár dalších příkladů (můžete je vyzkoušet v `influx query` nebo v Data Exploreru ve webovém UI):

```flux
// Spojení dvou měření (např. teplota a vlhkost) podle času a tagů
temp = from(bucket: "mybucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "temperature" and r._field == "value")

humidity = from(bucket: "mybucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "temperature" and r._field == "humidity")

join(tables: {temp: temp, hum: humidity}, on: ["_time", "location", "sensor"])
  |> map(fn: (r) => ({ r with temp_value: r._value_temp, hum_value: r._value_hum })) // Přejmenování sloupců pro přehlednost
```

Pro více informací o Fluxu viz [oficiální dokumentaci InfluxDB](https://docs.influxdata.com/flux/v0.x/).

### 2.4 InfluxDB HTTP API

InfluxDB v2.x poskytuje robustní HTTP API pro všechny operace (Flux, Line Protocol). Toto API je základem pro komunikaci s InfluxDB z aplikací a nástrojů třetích stran.

**Porovnání s `influx` CLI:**

Zatímco `influx` CLI (viz sekce 2.1) poskytuje pohodlné rozhraní pro správu a interaktivní dotazování, HTTP API vyžaduje manuální sestavení HTTP požadavků. To je typické pro programovou interakci z aplikací.

* **Příkaz CLI:** `influx write -b mybucket 'cpu,host=server1 value=0.64'`
* **Ekvivalentní HTTP požadavek:** Vyžaduje:
    * **Metodu:** `POST`
    * **URL:** `http://localhost:8086/api/v2/write?org=<org>&bucket=mybucket&precision=ns` (parametry jako organizace, bucket, přesnost jsou v URL)
    * **Hlavičky (Headers):**
        * `Authorization: Token <token>` (pro autentizaci)
        * `Content-Type: text/plain; charset=utf-8` (specifikuje formát těla požadavku)
    * **Tělo (Body):** Samotná data v Line Protocolu (`cpu,host=server1 value=0.64`)

* **Příkaz CLI:** `influx query 'from(bucket: "mybucket") |> range(start: -1h)'`
* **Ekvivalentní HTTP požadavek:** Vyžaduje:
    * **Metodu:** `POST`
    * **URL:** `http://localhost:8086/api/v2/query?org=<org>`
    * **Hlavičky (Headers):**
        * `Authorization: Token <token>`
        * `Accept: application/csv` (nebo `application/json` - určuje formát odpovědi)
        * `Content-Type: application/vnd.flux` (specifikuje, že v těle posíláme Flux dotaz)
    * **Tělo (Body):** Samotný Flux dotaz (`from(bucket: "mybucket") |> range(start: -1h)`)

**Příklady použití HTTP API (formát pro REST Client extension):**

Následující příklady jsou formátovány pro populární VS Code rozšíření **REST Client (humao.rest-client)**. Můžete je uložit do souboru s příponou `.http` a spouštět přímo z VS Code.

```http
### Nastavení proměnných (pro REST Client)
@baseUrl = http://localhost:8086
@token = my-super-secret-token
@org = myorg
@bucket = mybucket

### Zápis dat (v2 API - Line Protocol)
# Zapíše jeden datový bod do 'mybucket'
POST {{baseUrl}}/api/v2/write?org={{org}}&bucket={{bucket}}&precision=ns
Authorization: Token {{token}}
Content-Type: text/plain; charset=utf-8

cpu,host=server_api,region=eu-central value=0.99 1678887000000000000

### Čtení dat (v2 API - Flux)
# Načte data 'cpu' za posledních 5 minut z 'mybucket'
POST {{baseUrl}}/api/v2/query?org={{org}}
Authorization: Token {{token}}
Accept: application/csv
Content-Type: application/vnd.flux

from(bucket: "{{bucket}}")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "cpu")

### Čtení dat (v2 API - Flux, výstup JSON)
# Načte data 'cpu' za posledních 5 minut z 'mybucket' jako JSON
POST {{baseUrl}}/api/v2/query?org={{org}}
Authorization: Token {{token}}
Accept: application/json
Content-Type: application/vnd.flux

from(bucket: "{{bucket}}")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "cpu")

```

* **Vysvětlení formátu REST Client:**
    * `###`: Odděluje jednotlivé HTTP požadavky.
    * `@promenna = hodnota`: Definuje proměnnou, kterou lze později použít pomocí `{{promenna}}`.
    * První řádek pod `###` definuje metodu (POST) a URL.
    * Následující řádky jsou HTTP hlavičky (`Klíč: Hodnota`).
    * Prázdný řádek odděluje hlavičky od těla požadavku.
    * Tělo požadavku obsahuje data (Line Protocol pro zápis, Flux pro dotaz).

Použití HTTP API je nezbytné při integraci InfluxDB do vašich aplikací (např. v Pythonu, Javě, Go, JavaScriptu), kde budete používat HTTP klient knihovny k sestavení a odeslání těchto požadavků. Formát REST Client je užitečný pro testování a dokumentaci API volání.

### Úkoly

*(Všechny příkazy `influx` spouštějte buď v interaktivním shellu kontejneru po nastavení konfigurace, nebo z hostitelského systému s parametrem `-t my-super-secret-token`)*

1.  **Základní operace (InfluxDB v2 CLI):**
    * Vytvořte nový bucket `iotdata` s dobou uchovávání 30 dní (`influx bucket create`).
    * Vložte několik datových bodů do `iotdata` pro measurement `humidity` s různými tagy (např. `device_id`, `floor`). Použijte Line Protocol a `influx write`. Zahrňte i explicitní timestampy.
    * Napište Flux dotaz (`influx query`), který vybere data `humidity` za poslední hodinu.
    * Napište Flux dotaz, který vybere data pro konkrétní `device_id`.
    * Napište Flux dotaz, který spočítá průměrnou vlhkost za posledních 30 minut, seskupenou po 5 minutách (`aggregateWindow`).
    * Smažte data pro konkrétní `device_id` za poslední den pomocí `influx delete`.

2.  **Flux dotazy:**
    * Vložte data pro measurement `temperature` s tagy `location` a `sensor_id`.
    * Napište Flux dotaz, který vybere data `temperature` za poslední den a spočítá maximální, minimální a průměrnou hodnotu pro každý `sensor_id`. (Hint: použijte `group()` a agregační funkce jako `max()`, `min()`, `mean()`).
    * Napište Flux dotaz, který vyfiltruje data `temperature` s hodnotou `value` větší než 25.0.

3.  **HTTP API (v2):**
    * Pomocí nástroje jako `curl` nebo REST Client (s formátem uvedeným výše) a InfluxDB v2 HTTP API (`/api/v2/write`) vložte data (alespoň 2 datové body) do bucketu `iotdata`.
    * Pomocí `curl` nebo REST Client a InfluxDB v2 HTTP API (`/api/v2/query`) načtěte data z bucketu `iotdata` za poslední hodinu pomocí Flux dotazu.

4.  **Retention a Downsampling (Tasks):**
    * V InfluxDB 2.x se downsampling konfiguruje pomocí *Tasks*.
    * **Vytvořte Task:** Pomocí InfluxDB UI (viz sekce 2.2) nebo pomocí `influx task create` vytvořte task, který bude každou hodinu počítat průměrnou hodnotu `cpu` za poslední hodinu a ukládat ji do jiného bucketu (např. `downsampled_data` - ten si musíte nejdříve vytvořit) s delší dobou uchovávání.
        * Příklad Fluxu pro Task (uložte do souboru např. `downsample_task.flux`):
            ```flux
            option task = {name: "Hourly CPU Average", every: 1h}

            data = from(bucket: "mybucket")
              |> range(start: -task.every) // Zpracuj data za poslední interval tasku
              |> filter(fn: (r) => r._measurement == "cpu" and r._field == "value")
              |> mean()
              |> set(key: "_measurement", value: "cpu_hourly_avg") // Přejmenuj measurement

            data |> to(bucket: "downsampled_data", org: "myorg") // Ulož do jiného bucketu
            ```
        * Vytvoření tasku z CLI:
            ```bash
            # Vytvořte bucket downsampled_data (uvnitř shellu kontejneru nebo s docker exec)
            influx bucket create -n downsampled_data -o myorg
            # Nahrajte soubor s taskem do kontejneru (z hostitelského systému)
            # docker cp ./downsample_task.flux influxdb:/tmp/downsample_task.flux
            # Vytvořte task (uvnitř shellu kontejneru nebo s docker exec)
            influx task create -f /tmp/downsample_task.flux
            ```
    * **Ověření:** Počkejte alespoň hodinu a ověřte, že se data objevují v bucketu `downsampled_data` pomocí `influx query`.

5.  **Diskuze:**
    * Porovnejte Flux s InfluxQL (pokud máte zkušenost) nebo s SQL. Jaké jsou hlavní rozdíly v syntaxi a přístupu?
    * Kdy byste použili InfluxDB a kdy TimescaleDB? Uveďte konkrétní příklady.
    * Jaké jsou výhody a nevýhody použití HTTP API oproti `influx` CLI?
    * Vysvětlete, jak byste navrhli systém pro sběr a analýzu metrik z tisíců serverů. Jaké komponenty byste použili (např. Telegraf, InfluxDB, Grafana)?
    * Jaký je rozdíl mezi tagy a poli (fields) v InfluxDB? Proč je toto rozlišení důležité?
    * Vysvětlete problém "high cardinality". Jak byste se mu snažili předejít při návrhu schématu v InfluxDB? (Hint: nedávat unikátní ID jako tagy).
