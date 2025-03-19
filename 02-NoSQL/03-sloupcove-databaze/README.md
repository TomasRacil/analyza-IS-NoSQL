# Sloupcové (Column-Family) Databáze

## 1. Sloupcové Databáze: Teorie

### 1.1 Datový Model

Sloupcové databáze (column-family databases, také wide-column stores) ukládají data v *sloupcích*, na rozdíl od relačních databází, které ukládají data v řádcích.  To má zásadní dopad na výkon a způsob, jakým se data dotazují.

*   **Řádkové uložení (Row-oriented):**  Relační databáze (např. MySQL, PostgreSQL) ukládají data po *řádcích*.  Celý řádek (všechny sloupce pro daný záznam) je uložen *pohromadě* na disku.
*   **Sloupcové uložení (Column-oriented):** Sloupcové databáze ukládají data po *sloupcích*.  Všechny hodnoty pro *jeden sloupec* z *různých* řádků jsou uloženy pohromadě.

**Základní pojmy:**

*   **Klíčový prostor (Keyspace):**  Analogický *databázi* v relačním světě.  Seskupuje tabulky (column families).
*   **Tabulka (Column Family):**  Analogická *tabulce* v relační databázi, ale s důležitými rozdíly.  Obsahuje *řádky*.
*   **Řádek (Row):**  Sada sloupců.  Každý řádek má *unikátní klíč* (row key).  *Nemusí* obsahovat všechny sloupce definované v tabulce (column family) – je to *schéma-less* na úrovni řádku.
*   **Sloupec (Column):**  Skládá se ze jména, hodnoty a *timestampu*.  Timestamp se používá pro řešení konfliktů při souběžných zápisech.
*   **Rodina sloupců (Column Family):**  Definuje *strukturu* tabulky. Určuje typ klíče a *může* (ale *nemusí*) definovat typy pro *některé* sloupce.  Zásadní rozdíl oproti relačním databázím:  *Nemusíte* definovat *všechny* sloupce předem.  Můžete přidávat nové sloupce "za běhu", aniž byste museli měnit schéma tabulky.
* **Super sloupec:** (Tento koncept je spíše historický a v moderních verzích Cassandry se již nedoporučuje a nepoužívá) Umožňoval seskupení více sloupců. Cassandra v moderních verzích používá složené klíče.

**Příklad (konceptuální):**

Představte si tabulku `users` s klíčovým prostorem `mykeyspace`:

```
Keyspace: mykeyspace
  Column Family: users
    Row Key: user123
      Column: name = "John Doe" (timestamp: 1678886400)
      Column: email = "[e-mailová adresa byla odstraněna]" (timestamp: 1678886400)
      Column: age = 30 (timestamp: 1678886400)
    Row Key: user456
      Column: name = "Jane Smith" (timestamp: 1678886400)
      Column: city = "New York" (timestamp: 1678886400)
```

*   `mykeyspace` je klíčový prostor (jako databáze).
*   `users` je tabulka (column family).
*   `user123` a `user456` jsou klíče řádků.
*   `name`, `email`, `age`, `city` jsou jména sloupců.
*   Každý sloupec má hodnotu a timestamp.
*   Všimněte si, že `user456` *nemá* sloupec `age` a má sloupec `city`, který `user123` nemá.  To ilustruje flexibilitu schématu.

**Klíčové vlastnosti sloupcového modelu:**

*   **Schéma-flexible (na úrovni řádku):**  Řádky ve stejné tabulce *nemusí* mít stejné sloupce.
*   **Řídké data (Sparse Data):**  Velmi efektivní pro ukládání dat, kde je mnoho sloupců, ale většina řádků má hodnoty jen pro *malou část* z nich.  Pokud sloupec pro daný řádek neexistuje, *nezabírá žádné místo* na disku.
*   **Optimalizováno pro čtení sloupců:**  Pokud potřebujete číst *pouze* určité sloupce z *velkého počtu* řádků, sloupcové databáze jsou *mnohem* efektivnější než relační databáze.  Nemusíte číst celé řádky.
*   **Optimalizováno pro agregace:**  Agregace (např. `SUM`, `AVG`, `COUNT`) nad *jedním sloupcem* jsou velmi rychlé, protože data jsou uložena pohromadě.
*   **Horizontální škálovatelnost:** Sloupcové databáze jsou navrženy pro distribuované prostředí a snadno se škálují horizontálně (přidáváním dalších serverů).
* **Denormalizace:** Data se často denormalizují, což zjednodušuje dotazy a zvyšuje rychlost čtení

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Vysoký výkon pro čtení specifických sloupců:**  Ideální pro analytické dotazy, které pracují s malým počtem sloupců z velkého počtu řádků.
*   **Vysoký výkon pro zápis:**  Zápis nových dat (nových sloupců) je velmi rychlý, protože se zapisují pouze nové hodnoty (nemusí se přepisovat celé řádky).
*   **Efektivní ukládání řídkých dat:**  Nezabírá místo pro chybějící hodnoty.
*   **Škálovatelnost:**  Dobře se škálují horizontálně (na velké clustery).
*   **Flexibilita schématu (na úrovni řádku):**  Snadné přidávání nových sloupců.

**Nevýhody:**

*   **Složitější dotazování na více sloupců:**  Pokud potřebujete *všechny* sloupce pro *konkrétní* řádek, sloupcová databáze *nemusí* být rychlejší než relační databáze. (Záleží na tom, kolik sloupců potřebujete a kolik jich v daném řádku *skutečně* existuje.)
*   **Omezené transakce (ACID):**  Podpora transakcí je obvykle *omezená* (např. na úrovni jednoho řádku).  Cassandra nabízí "lightweight transactions" (LWT) s omezenou funkcionalitou.
*   **Složitější modelování dat:**  Vyžaduje pečlivé plánování a denormalizaci dat.
*   **Nevhodné pro časté aktualizace *existujících* hodnot:**  Aktualizace hodnoty sloupce je v podstatě *nový zápis* (s novým timestampem). Staré hodnoty zůstávají (dokud neproběhne compaction), což může vést k plýtvání místem.

### 1.3 Příklady Sloupcových Databází

*   **Apache Cassandra:**  Široce používaná, vysoce škálovatelná a dostupná.  Původně vyvinutá ve Facebooku.  Používá CQL (Cassandra Query Language), který je podobný SQL.
*   **Apache HBase:**  Postavená nad Hadoopem.  Vhodná pro velmi velké datasety.
*   **Amazon DynamoDB:**  Plně spravovaná sloupcová (a dokumentová) databáze na AWS.
*   **Google Bigtable:**  Služba od Googlu, na které běží mnoho interních služeb Googlu (např. Gmail, YouTube).
*   **ScyllaDB:**  Kompatibilní s Cassandrou (používá stejný protokol a CQL), ale napsaná v C++ (místo Javy) pro vyšší výkon.

### 1.4 Kdy je sloupcová databáze lepší volbou než relační?

*   **Analytické a reportovací aplikace:**  Kde potřebujete agregovat data přes velké objemy dat (např. průměrná cena produktu za poslední rok, počet uživatelů v jednotlivých regionech).
*   **Časové řady (Time Series Data):**  Ukládání dat, která se mění v čase (např. data ze senzorů, logy, finanční data).
*   **Řídká data:**  Kde máte mnoho sloupců, ale většina řádků má hodnoty jen pro malou část z nich.
*   **Aplikace s vysokým objemem zápisu:**  Kde je důležitá rychlost zápisu nových dat.
*   **Velké objemy dat a vysoká zátěž:** Kde je třeba systém škálovat.
*   **Aplikace, kde se schéma často mění (přidávají se nové sloupce).**

**Kdy sloupcová databáze *není* dobrá volba:**

*   **Aplikace vyžadující silné ACID transakce přes více řádků/tabulek.**
*   **Aplikace, kde potřebujete často číst *všechny* sloupce pro *konkrétní* řádky.**
*   **Aplikace s komplexními vztahy mezi daty, kde jsou časté JOINy.**
*   **Aplikace s častými aktualizacemi *existujících* hodnot.**

## 2. Cassandra: Praktický Příklad

Tento příklad ukazuje, jak nastavit Cassandra a Stargate pomocí Dockeru, připojit se k databázi pomocí `cqlsh` a provádět základní operace.

### Struktura

*   **`docker-compose.yml`:** Definuje službu Cassandra

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**
2.  **Otevřete terminál** a přejděte do tohoto adresáře.
3.  **Spusťte kontejnery:**

    ```bash
    docker-compose up -d
    ```

### 2.1 CQLSH

#### Připojení k Cassandra 

*   **Pomocí `cqlsh` (v novém terminálu):**

    ```bash
    docker exec -it cassandra cqlsh
    ```

    Tím se připojíte k Cassandra serveru běžícímu uvnitř kontejneru.  `cqlsh` je interaktivní terminálový klient pro Cassandra (podobný `mysql` klientovi pro MySQL).



#### Základní operace (v `cqlsh`)

*   **Vytvoření klíčového prostoru (Keyspace):**

    ```cql
    CREATE KEYSPACE mykeyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    ```

    *   `CREATE KEYSPACE`:  Příkaz pro vytvoření klíčového prostoru.
    *   `mykeyspace`:  Název klíčového prostoru.
    *   `WITH replication`:  Určuje strategii replikace.
        *   `'class': 'SimpleStrategy'` :  Jednoduchá strategie replikace (vhodná pro vývoj/testování).
        *   `'replication_factor': 1`:  Počet kopií dat (pro produkci byste obvykle použili vyšší hodnotu, např. 3).
    *  Pro produkční prostředí by se měla používat `NetworkTopologyStrategy`.

*   **Použití klíčového prostoru:**

    ```cql
    USE mykeyspace;
    ```

*   **Vytvoření tabulky (Column Family):**

    ```cql
    CREATE TABLE users (
        user_id text PRIMARY KEY,
        name text,
        email text,
        age int
    );
    ```

    *   `CREATE TABLE`:  Příkaz pro vytvoření tabulky.
    *   `users`:  Název tabulky.
    *   `user_id text PRIMARY KEY`:  Definuje primární klíč (musí být unikátní).  V Cassandře je primární klíč *velmi důležitý* pro výkon a distribuci dat.
    *   `name text`, `email text`, `age int`:  Definují další sloupce a jejich datové typy.  Všimněte si, že *nemusíte* definovat *všechny* sloupce, které budete používat.  Můžete přidávat nové sloupce "za běhu".
    *  V cassandře se dá nastavit i složený primární klíč:
        ```cql
        CREATE TABLE users_by_city (
            city text,
            user_id text,
            name text,
            email text,
            age int,
            PRIMARY KEY (city, user_id)
        );
        ```
        V tomto případě `city` je partition key a `user_id` je clustering key. Data budou rozdělena (partitioned) podle hodnoty `city` a *uvnitř* každé partice budou seřazena podle `user_id`.

* **Vložení dat:**

    ```cql
    INSERT INTO users (user_id, name, email, age) VALUES ('user1', 'John Doe', '[e-mailová adresa byla odstraněna]', 30);
    INSERT INTO users (user_id, name, city) VALUES ('user2', 'Jane Smith', 'New York');
    ```

    *   Všimněte si, že druhý `INSERT` vkládá data do sloupce `city`, který nebyl definován při vytváření tabulky.  Tento příkaz selže i přesto že je Cassandra *schéma-flexible*. Je třeba prvně použít příkaz. 

    ```cql
    ALTER TABLE users ADD city text;
    ```

    *   Tím je zajištěno přidání sloupce.

*   **Výběr dat:**

    ```cql
    SELECT * FROM users;  -- Vrátí všechny sloupce a všechny řádky
    SELECT name, email FROM users;  -- Vrátí pouze sloupce 'name' a 'email'
    SELECT * FROM users WHERE user_id = 'user1';  -- Vrátí řádek s user_id = 'user1'
    ```

* **Aktualizace dat**

    ```cql
    UPDATE users SET age = 31 WHERE user_id = 'user1';
    ```

* **Smazání dat**
    ```cql
    DELETE FROM users WHERE user_id = 'user1'; -- Smaže celý řádek
    DELETE email FROM users WHERE user_id = 'user2'; --Smaže daný sloupec
    ```

*   **Vytvoření indexu:**

    ```cql
    CREATE INDEX ON users (email);  -- Vytvoří index na sloupci 'email'
    ```
    *   Indexy v Cassandře *nejsou* tak výkonné jako v relačních databázích. Používejte je *opatrně* a jen tam, kde je to *nezbytně nutné*. Primárně byste měli dotazovat podle primárního klíče.
    *  Cassandra nepodporuje `LIKE` operace v `WHERE` klauzuli.

### 2.2 Stargate: Přístup k Cassandra přes API

Cassandra nativně komunikuje pomocí CQL (Cassandra Query Language) přes binární protokol.  Pro aplikace, které preferují nebo vyžadují komunikaci přes HTTP (např. webové aplikace, mikroslužby), je ideální použít *Stargate*.

**Co je Stargate?**

Stargate je open-source data gateway, který se nasazuje *mezi* vaši aplikaci a Cassandra cluster.  Poskytuje několik API:

*   **REST API:** Umožňuje komunikovat s Cassandrou pomocí standardních HTTP metod (GET, POST, PUT, DELETE) a JSON formátu.  Existují dvě verze: v1 (starší) a v2 (novější, doporučená).
*   **GraphQL API:**  Umožňuje dotazovat se na data pomocí GraphQL dotazovacího jazyka.  GraphQL je flexibilnější a efektivnější než REST pro složitější dotazy.
*   **gRPC API:**  Vysoce výkonné API založené na protokolu gRPC (od Googlu).  Vhodné pro komunikaci mezi mikroslužbami.
*   **CQL API:** Umožňuje používat nativní CQL přes Stargate (přes binární protokol, stejně jako nativní Cassandra).

**Výhody použití Stargate:**

*   **Snadná integrace:**  Umožňuje aplikacím, které nejsou napsané v Javě (pro kterou existuje nativní Cassandra driver), snadno komunikovat s Cassandrou.
*   **Flexibilita:**  Můžete si vybrat API, které nejlépe vyhovuje vašim potřebám (REST, GraphQL, gRPC, CQL).
*   **Zabezpečení:**  Stargate podporuje autentizaci a autorizaci.
*   **Schématické API:** Umožňuje spravovat schéma keyspaců a tabulek.
*   **Škálovatelnost:**  Stargate je navržen pro horizontální škálovatelnost (můžete spustit více instancí Stargate).
*   **Open-source:**  Je to open-source projekt s aktivní komunitou.

**Použití Stargate API (pomocí `curl`):**

Následující příklady předpokládají, že máte spuštěný Stargate a Cassandru (např. pomocí `docker-compose.yml` z předchozích odpovědí) a že máte vytvořený klíčový prostor `mykeyspace` a tabulku `users` s alespoň sloupci `user_id` (text, primární klíč), `name` (text) a `email` (text).

*   **Stargate REST API :**
    *   **Získání autorizačního tokenu a ověření uložení tokenu**

        ```bash
        AUTH_TOKEN=$(curl -X POST http://localhost:8081/v1/auth \
        -H "Content-Type: application/json" \
        -d '{"username": "cassandra", "password": "cassandra"}' | grep '"authToken"' | cut -d '"' -f 4 | tr -d ' ')

        echo "Token: $AUTH_TOKEN"
        ```

    *   **Získání všech keyspaces:**

        ```bash
        curl -X GET http://localhost:8082/v2/schemas/keyspaces \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```

    *   **Získání informací o keyspace `mykeyspace`:**

        ```bash
        curl -X GET http://localhost:8082/v2/schemas/keyspaces/mykeyspace \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```

    *   **Získání všech tabulek v keyspace `mykeyspace`:**

        ```bash
        curl -X GET http://localhost:8082/v2/schemas/keyspaces/mykeyspace/tables \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```

     *  **Získání definice tabulky:**
        ```bash
        curl -X GET http://localhost:8082/v2/schemas/keyspaces/mykeyspace/tables/users \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```

    *   **Získání všech řádků z tabulky `users`:**

        ```bash
        curl -X GET http://localhost:8082/v2/keyspaces/mykeyspace/users/rows \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```

    *   **Získání konkrétního řádku (podle primárního klíče):**

        ```bash
        curl -L -G http://localhost:8082/v2/keyspaces/mykeyspace/users/user2 \
        -H "X-Cassandra-Token: $AUTH_TOKEN" -H "Content-Type: application/json"
        ```

    *   **Získání konkrétního řádku (podle where - pouze indexované sloupce):**

        ```bash
        curl -L -G http://localhost:8082/v2/keyspaces/mykeyspace/users \
        -H "X-Cassandra-Token: $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        --data-urlencode 'where={"name": {"$eq": "Charlie"}}'
        ```

    *   **Vložení nového řádku:**

        ```bash
        curl -X POST http://localhost:8082/v2/keyspaces/mykeyspace/users \
        -H "Content-Type: application/json" \
        -H "X-Cassandra-Token: $AUTH_TOKEN" \
        -d '{"user_id": "user3", "name": "Charlie", "email": "[e-mailová adresa byla odstraněna]"}'
        ```

        *   `-H "Content-Type: application/json"`:  Říká, že posíláme JSON data.
        *   `-d '...'`:  Obsahuje data v JSON formátu.

    *   **Aktualizace řádku:**

        ```bash
        curl -X PUT http://localhost:8082/v2/keyspaces/mykeyspace/users/user2 \
        -H "Content-Type: application/json" \
        -H "X-Cassandra-Token: $AUTH_TOKEN" \
        -d '{"name": "John Updated"}'
        ```
    *   **Smazání řádku**
        ```bash
        curl -X DELETE  http://localhost:8082/v2/keyspaces/mykeyspace/users/user3 \
        -H "X-Cassandra-Token: $AUTH_TOKEN"
        ```
    * **Filtrování (WHERE klauzule):**

        Předpokládejme, že máte sloupec `age`.
          ```bash
          curl -X GET 'http://localhost:8081/v2/keyspaces/mykeyspace/tables/users/rows?where={"age":{"$gt":30}}'
          ```
          *  Je potřeba data ve WHERE klauzuli encodovat.  V tomto případě je to `{"age":{"$gt":30}}`.

*   **Stargate GraphQL API (port 8080) - Použití GraphQL Playground/GraphiQL:**

    1.  **Otevřete GraphQL Playground:** Otevřete v prohlížeči adresu `http://localhost:8080/playground`.
    2.  **Nastavte autentizační hlavičku:**  V sekci "HTTP Headers" (obvykle dole) přidejte hlavičku:

        ```json
        {
          "X-Cassandra-Token": "<váš_token>"
        }
        ```

        `<váš_token>` nahraďte *skutečným* tokenem, který jste získali pomocí REST API v1.

    3.  **Pište a spouštějte dotazy:**  V levém panelu pište GraphQL dotazy a mutace.  Používejte Ctrl+Space (nebo Cmd+Space) pro automatické doplňování a nápovědu.  Dotazy spouštějte tlačítkem "Play" (nebo Ctrl+Enter / Cmd+Enter).  Výsledky se zobrazí v pravém panelu.

    *   **Schema deployment:** Nejdřív je nutné deploynout schema (pokud ještě neexistuje).  *Pozor*: Toto musíte udělat *přes GraphQL API*, *ne* přes `cqlsh`, pokud chcete pracovat se Stargate GraphQL. Následující příkazy je třeba provádět na endpointu `/graphql-schema`.
         * Vytvoření keyspace:
            ```graphql
            mutation {
              createKeyspace(
                name: "mykeyspace"
                ifNotExists: true
                datacenters: [{ name: "datacenter1", replicas: 1 }]
              )
            }
            ```

        * Vytvoření tabulky `users`
            ```graphql
            mutation {
                createTable(
                    keyspaceName: "mykeyspace"
                    tableName: "users"
                    partitionKeys: [
                        { name: "user_id", type: { basic: TEXT } }
                    ]
                    values: [
                        { name: "name", type: { basic: TEXT } },
                        { name: "email", type: { basic: TEXT } }
                    ]
                    ifNotExists: true
                )
            }
            ```

     Všechny následující příkazy je třeba provádět na endpointu `/graphql/mykeyspace`.

    * **Získání všech uživatelů:**

        ```graphql
        query {
          users {
            values {
              user_id
              name
              email
            }
          }
        }
        ```

    *   **Vložení uživatele:**

        ```graphql
        mutation {
          insertusers(
            value: { user_id: "user5", name: "Eve", email: "[e-mailová adresa byla odstraněna]" }
          ) {
            value {
              user_id
            }
          }
        }
        ```

    * **Filtrace uživatelů**
        ```graphql
        query {
          users (filter: {name: { eq: "Eve" }})
          {
            values {
              user_id
              name
              email
            }
          }
        }
        ```

    *   **Aktualizace uživatele:**

        ```graphql
        mutation {
          updateusers(
            value: { user_id: "user5", name: "Eve Updated", email: "[e-mailová adresa byla odstraněna]" }
          ) {
            applied
          }
        }
        ```
     * **Smazání uživatele:**

        ```graphql
         mutation {
          deleteusers(
            value: {user_id:  "user5" }
          ) {
            applied
          }
        }
        ```

### Úkoly

1.  **Základní operace:**
    *   Vytvořte nový klíčový prostor `testkeyspace`.
    *   Vytvořte tabulku `products` s primárním klíčem `product_id` (text) a sloupci `name` (text), `price` (double), `category` (text).
    *   Vložte několik produktů do tabulky (alespoň 3).
    *   Vyberte všechny produkty.
    *   Vyberte jméno a cenu všech produktů.
    *   Vyberte produkt s `product_id` = 'product1' (nebo jakýkoli jiný existující `product_id`).
    *   Aktualizujte cenu produktu s `product_id` = 'product1'.
    *   Smažte produkt s `product_id` = 'product2'.

2.  **Schéma-flexible:**
    *   Vložte nový produkt do tabulky `products`, ale tentokrát přidejte *nový* sloupec `description` (text), který nebyl definován při vytváření tabulky.  Ověřte, že to funguje.
    *   Vyberte všechny produkty a všimněte si, že starší produkty *nemají* sloupec `description`, zatímco nový produkt ho má.

3.  **Indexy:**
    *   Vytvořte index na sloupci `category` v tabulce `products`.
    *   Vyberte všechny produkty z kategorie 'Electronics' (nebo jakoukoli jinou kategorii, kterou jste použili).

4.  **Složený primární klíč:**
    *   Vytvořte novou tabulku `products_by_category` s *složeným* primárním klíčem:
        *   Partition key: `category` (text)
        *   Clustering key: `product_id` (text)
        *   Další sloupce: `name` (text), `price` (double)
    *   Vložte několik produktů do této nové tabulky (použijte stejné produkty jako v předchozích úkolech, ale s různými kategoriemi).
    *   Vyberte všechny produkty z kategorie 'Electronics'.  Všimněte si, že výsledky jsou *automaticky seřazeny* podle `product_id` (clustering key) *uvnitř* každé kategorie (partition key).
    *   Zkuste vybrat produkty podle `product_id` *bez* specifikace `category`.  Mělo by to vyvolat chybu – v Cassandře musíte v `WHERE` klauzuli specifikovat *všechny* části partition key.
    *  Zkuste přidat WHERE s nerovností na clustering key. Například:
      ```cql
      SELECT * FROM products_by_category WHERE category = 'Electronics' AND product_id > 'product1';
      ```

5. **Smazání sloupce**
   * Smažte sloupec `description` u jednoho z produktů, které ho mají, a ověřte, že to funguje.

6.  **Lightweight Transactions (LWT):**
    *   Zkuste použít LWT pro *podmíněnou* aktualizaci.  Např.:
        ```cql
        UPDATE products SET price = 99.99 WHERE product_id = 'product1' IF price = 120.00;
        ```
        Tento příkaz aktualizuje cenu produktu `product1` na 99.99 *pouze pokud* je jeho aktuální cena 120.00.  Pokud je cena jiná, aktualizace se *neprovede*.  Ověřte chování.  LWT používají Paxos protokol pro konsensus a jsou *výrazně pomalejší* než běžné operace. Používejte je *jen když je to nezbytně nutné*.

7.  **Stargate REST API:**
    *   Pomocí `curl` a Stargate REST API (v2) vytvořte nový klíčový prostor `stargate_test`.
    *   Vytvořte tabulku `products` (jako v předchozích úkolech) v tomto novém klíčovém prostoru.
    *   Vložte několik produktů pomocí `curl` a JSON dat.
    *   Získejte všechny produkty pomocí `curl`.
    *   Získejte konkrétní produkt pomocí `curl`.
    *   Aktualizujte a smažte produkt.

8.  **Stargate GraphQL API:**
    * Pomocí GraphQL vytvořte nový klíčový prostor.
    * Vytvořte v něm tabulku.
    * Vložte data.
    * Získejte data s filtrováním.

9.  **Stargate a cqlsh:**
    *   Připojte se k Cassandra přes Stargate pomocí `cqlsh` (přes `stargate` kontejner).
    *   Proveďte několik základních CQL operací (vytvoření klíčového prostoru, tabulky, vložení dat, výběr dat).

10.  **Diskuze:**  V jakých scénářích byste *nepoužili* Cassandra (nebo jinou sloupcovou databázi)?  Kdy byste dali přednost relační databázi? Kdy byste zvolili jiný typ NoSQL databáze (např. dokumentovou nebo key-value)? Uveďte konkrétní příklady. Jaké jsou výhody a nevýhody použití Stargate oproti přímému přístupu k Cassandra přes CQL?  V jakých situacích byste preferovali Stargate a v jakých přímý přístup?
