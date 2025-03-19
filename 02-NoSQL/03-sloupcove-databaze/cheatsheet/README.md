# Apache Cassandra CQL Cheat Sheet

## Základní Pojmy

*   **Keyspace:**  Analogický databázi v relačním světě. Seskupuje tabulky (column families).
*   **Table (Column Family):** Analogická tabulce v relační databázi. Obsahuje řádky.
*   **Row:**  Sada sloupců. Každý řádek má unikátní klíč (row key).
*   **Column:**  Skládá se ze jména, hodnoty a timestampu.
*   **Row Key (Primary Key):** Unikátní identifikátor řádku. Může být jednoduchý (jeden sloupec) nebo složený (více sloupců).
*   **Partition Key:** Část primárního klíče, která určuje, na kterém uzlu clusteru budou data uložena.
*   **Clustering Key:**  Část primárního klíče (pokud je složený), která určuje pořadí řádků *uvnitř* partition.
*   **CQL Data Types:**  `text`, `int`, `bigint`, `float`, `double`, `boolean`, `timestamp`, `uuid`, `blob`, `list`, `set`, `map`, a další.

## Základní CRUD Operace

### 1. CREATE KEYSPACE - Vytvoření Klíčového Prostoru

```cql
CREATE KEYSPACE mykeyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```

*   `CREATE KEYSPACE [IF NOT EXISTS] keyspace_name`:  Vytvoří nový klíčový prostor. `IF NOT EXISTS` zabrání chybě, pokud keyspace již existuje.
*   `WITH replication`:  Povinná klauzule, určuje strategii replikace.
    *   `'class': 'SimpleStrategy'` (pro vývoj/testování) - jednoduchá replikace.
    *   `'class': 'NetworkTopologyStrategy'` (pro produkci) - umožňuje určit replikaci pro různá datacentra.
    *   `'replication_factor'`:  Počet kopií dat.  Pro `NetworkTopologyStrategy` se specifikuje pro každé datacentrum zvlášť: `'datacenter1': 3, 'datacenter2': 2`.

### 2. USE - Nastavení Aktivního Klíčového Prostoru

```cql
USE mykeyspace;
```

Nastaví `mykeyspace` jako aktivní klíčový prostor, takže ho nemusíte specifikovat u každého dotazu.

### 3. CREATE TABLE - Vytvoření Tabulky (Column Family)

```cql
CREATE TABLE users (
    user_id uuid PRIMARY KEY,  -- Jednoduchý primární klíč
    username text,
    email text,
    age int
);

CREATE TABLE products_by_category (
    category text,
    product_id uuid,
    name text,
    price double,
    PRIMARY KEY (category, product_id)  -- Složený primární klíč
) WITH CLUSTERING ORDER BY (product_id DESC);
```

*   `CREATE TABLE [IF NOT EXISTS] [keyspace_name.]table_name`: Vytvoří novou tabulku.
*   `column_name data_type`: Definice sloupce a jeho datového typu.
*   `PRIMARY KEY (column_name)`:  Definuje *jednoduchý* primární klíč (jeden sloupec).
*   `PRIMARY KEY ((column1, column2), column3)`: Definuje *složený* primární klíč.
    *   `(column1, column2)`: Partition key (může být složený z více sloupců).
    *   `column3`: Clustering key.
    *  Pořadí sloupců v definici primárního klíče je *důležité*.
* `WITH CLUSTERING ORDER BY (clustering_column DESC/ASC)`: Volitelně, určuje řazení podle clustering klíče.

### 4. INSERT - Vložení Dat

```cql
INSERT INTO users (user_id, username, email, age)
VALUES (uuid(), 'johndoe', '[e-mailová adresa byla odstraněna]', 30);

INSERT INTO users (user_id, username, city)  -- Přidání sloupce, který nebyl v CREATE TABLE
VALUES (uuid(), 'janesmith', 'New York');
```

*   `INSERT INTO [keyspace_name.]table_name (column1, column2, ...) VALUES (value1, value2, ...)`: Vloží nový řádek.
*   `uuid()`: Funkce pro generování UUID (unikátní identifikátor).
*   **Důležité:**  Cassandra je schéma-flexible *na úrovni řádku*, takže můžete přidávat nové sloupce "za běhu". Pokud ale sloupec nebyl definován v `CREATE TABLE` (nebo přidán pomocí `ALTER TABLE`), musíte ho před použitím v `INSERT` (nebo `UPDATE`) explicitně přidat pomocí `ALTER TABLE table_name ADD column_name data_type`.

### 5. SELECT - Výběr Dat

```cql
SELECT * FROM users;  -- Vybere všechny sloupce a řádky

SELECT username, email FROM users;  -- Vybere jen zadané sloupce

SELECT * FROM users WHERE user_id = 123e4567-e89b-12d3-a456-426614174000; -- Filtrování podle primárního klíče

SELECT * FROM products_by_category WHERE category = 'Electronics'; -- Filtrování podle partition key

SELECT * FROM products_by_category WHERE category = 'Electronics' AND product_id > 100; --Filtrování podle partition a clustering key
```

*   `SELECT column1, column2, ... FROM [keyspace_name.]table_name`:  Vybírá data.
*   `*`:  Všechny sloupce.
*   `WHERE`:  Filtrování.  V Cassandře je `WHERE` *omezené* – primárně musíte filtrovat podle primárního klíče (partition key a clustering key).
*   `ALLOW FILTERING`:  Povoluje filtrování podle *neindexovaných* sloupců, ale je to *velmi neefektivní* a *nedoporučuje se* pro produkční prostředí. Mělo by se používat jen pro velmi malé datasety.
* **Duležité:** Cassandra je optimalizovaná pro *rychlé čtení podle klíče*. Složité dotazy s filtrováním podle neklíčových sloupců (bez indexů a `ALLOW FILTERING`) jsou *velmi pomalé*.
* `LIMIT`: Omezí počet vrácených řádků
    ```cql
        SELECT * FROM users LIMIT 5;
    ```

### 6. UPDATE - Aktualizace Dat

```cql
UPDATE users SET age = 31 WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;

UPDATE users SET city = 'Prague', email = '[e-mailová adresa byla odstraněna]'
WHERE user_id = 456f7890-e89b-12d3-a456-426614174000;
```

*   `UPDATE [keyspace_name.]table_name SET column1 = value1, column2 = value2, ... WHERE key = value`:  Aktualizuje data.
*   `WHERE`: *Povinné*, určuje, které řádky se mají aktualizovat (podle primárního klíče).
*   Aktualizace je v podstatě *nový zápis* s novým timestampem.

### 7. DELETE - Mazání Dat

```cql
DELETE FROM users WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;  -- Smaže celý řádek

DELETE email FROM users WHERE user_id = 456f7890-e89b-12d3-a456-426614174000; -- Smaže konkrétní sloupec
```

*   `DELETE [column1, column2, ...] FROM [keyspace_name.]table_name WHERE key = value`:  Maže data.
*   `WHERE`:  *Povinné*, určuje, které řádky se mají smazat (podle primárního klíče).
*  Smazání v Cassandře je ve skutečnosti *vložení "náhrobku" (tombstone)*. Data nejsou okamžitě fyzicky odstraněna, ale označí se k odstranění a odstraní se až při compaction.

### 8. ALTER TABLE - Změna Schématu Tabulky

```cql
ALTER TABLE users ADD city text; -- Přidání nového sloupce

ALTER TABLE users DROP city; -- Odstranění sloupce

ALTER TABLE users ALTER age TYPE bigint; -- Změna datového typu sloupce (omezené možnosti)
```

*   `ALTER TABLE [keyspace_name.]table_name ADD column_name data_type`:  Přidá nový sloupec.
*   `ALTER TABLE [keyspace_name.]table_name DROP column_name`:  Odstraní sloupec (data v tomto sloupci se stanou nedostupnými!).
*   `ALTER TABLE [keyspace_name.]table_name ALTER column_name TYPE new_data_type`:  Změní datový typ sloupce.  Je možné jen mezi *kompatibilními* typy (např. z `int` na `bigint`).

### 9. CREATE INDEX - Vytvoření Sekundárního Indexu

```cql
CREATE INDEX ON users (email); -- Vytvoří index na sloupci email

CREATE INDEX index_name ON users (city); -- Vytvoření indexu s daným jménem
```

*   `CREATE INDEX [IF NOT EXISTS] [index_name] ON [keyspace_name.]table_name (column_name)`: Vytvoří sekundární index.
*   **Důležité:** Sekundární indexy v Cassandře *nejsou* tak výkonné jako v relačních databázích a mají *omezení*. Používejte je *opatrně* a *jen když je to nezbytně nutné*.  Vždy se snažte primárně dotazovat podle primárního klíče.  Indexy jsou vhodné pro sloupce s *nízkou kardinalitou* (málo unikátních hodnot).
*   **SASI (Storage Attached Secondary Index):**  Alternativní typ indexu, který může být výkonnější pro některé typy dotazů (např. `LIKE`).

### 10. TRUNCATE - Smazání Všech Dat z Tabulky

```cql
TRUNCATE users;  -- Smaže *všechny* řádky z tabulky users (rychlejší než DELETE)
```

*  Rychlejší než `DELETE *`, protože obchází vytváření náhrobků.
* Odstraní *všechna* data, ale *zachová* schéma tabulky (sloupce, indexy).

### 11. BATCH - Dávkové Operace

```cql
BEGIN BATCH
    INSERT INTO users (user_id, username) VALUES (uuid(), 'user1');
    INSERT INTO users (user_id, username) VALUES (uuid(), 'user2');
    UPDATE users SET age = 30 WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;
APPLY BATCH;
```

*   `BEGIN BATCH ... APPLY BATCH`: Umožňuje provést více operací (INSERT, UPDATE, DELETE) *atomicky* (buď všechny, nebo žádná) a *efektivněji* (v jedné dávce).
*   **Důležité:**  Atomické jsou pouze operace *uvnitř jedné partition*. Operace v různých particích *nejsou* atomické.  Batch by neměl být příliš velký (doporučuje se maximálně desítky operací).
*   `BEGIN UNLOGGED BATCH`:  Ještě rychlejší, ale *neatomické*. Vhodné pro import velkého množství dat, kde není kritická atomičnost.
* `BEGIN COUNTER BATCH`: Pro operace s counter sloupci.

### 12. Lightweight Transactions (LWT) - Lehké Transakce

```cql
INSERT INTO users (user_id, username, email) VALUES (uuid(), 'newuser', '[e-mailová adresa byla odstraněna]') IF NOT EXISTS;

UPDATE users SET age = 31 WHERE user_id = 123e4567-e89b-12d3-a456-426614174000 IF age = 30;
```

*   `IF NOT EXISTS` (pro `INSERT`):  Vloží řádek, *pouze pokud* neexistuje.
*   `IF condition` (pro `UPDATE` a `DELETE`):  Provede operaci, *pouze pokud* je splněna podmínka.
*   LWT používají protokol Paxos pro zajištění konsensu a jsou *výrazně pomalejší* než běžné operace.  Používejte je *jen když je to nezbytně nutné*.
*   Výsledek LWT operace obsahuje sloupec `[applied]` (boolean), který indikuje, zda byla operace úspěšná.

    ```cql
    SELECT * FROM users WHERE user_id = 123e4567-e89b-12d3-a456-426614174000 IF EXISTS; -- Kontrola existence řádku.
    ```

### 13. UDF (User-Defined Functions) - Uživatelské Funkce

```cql
CREATE FUNCTION mykeyspace.add(a int, b int)
    CALLED ON NULL INPUT
    RETURNS int
    LANGUAGE java
    AS 'return a + b;';
```

*   Umožňují definovat vlastní funkce v Javě, JavaScriptu nebo jiných podporovaných jazycích a volat je v CQL dotazech.
* `CALLED ON NULL INPUT` / `RETURNS NULL ON NULL INPUT` určuje chování při NULL vstupech.
* `RETURNS` specifikuje návratový typ.
* `LANGUAGE` specifikuje jazyk.
* `AS` obsahuje kód funkce.

### 14. UDA (User-Defined Aggregates) - Uživatelské Agregace

```cql
CREATE AGGREGATE mykeyspace.avg_state(int)
    SFUNC avg_state_func
    STYPE tuple<int, bigint>
    INITCOND (0, 0);

CREATE FUNCTION mykeyspace.avg_state_func(state tuple<int, bigint>, val int)
    CALLED ON NULL INPUT
    RETURNS tuple<int, bigint>
    LANGUAGE java
    AS '
        if (val != null) {
            state.setInt(0, state.getInt(0) + val);
            state.setLong(1, state.getLong(1) + 1);
        }
        return state;
    ';

CREATE FUNCTION mykeyspace.avg_final_func(state tuple<int, bigint>)
    CALLED ON NULL INPUT
    RETURNS double
    LANGUAGE java
    AS '
        if (state.getLong(1) == 0) {
            return null;
        }
        return (double) state.getInt(0) / state.getLong(1);
    ';
```

*   Umožňují definovat vlastní agregační funkce (podobně jako `SUM`, `AVG` v SQL).
*   Vyžadují definici `SFUNC` (state function - provádí agregaci pro každý řádek), `STYPE` (typ stavu agregace) a volitelně `FINALFUNC` (provádí finální výpočet ze stavu). `INITCOND` definuje počáteční hodnotu.

### 15. Materialized Views (Materializované Pohledy)

```cql
CREATE MATERIALIZED VIEW users_by_email AS
    SELECT email, user_id, username
    FROM users
    WHERE email IS NOT NULL AND user_id IS NOT NULL
    PRIMARY KEY (email, user_id);
```

*   Automaticky udržovaná "kopie" dat z tabulky, uspořádaná podle jiného klíče.
*   Umožňují efektivní dotazování podle jiného klíče, než je primární klíč *základní tabulky*.
*   Aktualizace základní tabulky se *automaticky* propagují do materializovaného pohledu.
*   Mají *omezení* (např. nemůžete filtrovat podle sloupců, které nejsou součástí primárního klíče materializovaného pohledu, nebo základní tabulky).

```cql
DROP MATERIALIZED VIEW mykeyspace.users_by_email;
```

### 16. Time To Live (TTL) - Automatické Smazání Dat

*   Umožňuje nastavit dobu (v sekundách), po které budou data automaticky smazána.
*   TTL se dá nastavit na úrovni celého řádku, nebo jednotlivých sloupců.

*   **Nastavení TTL při vkládání dat:**

    ```cql
    INSERT INTO users (user_id, username, email) VALUES (uuid(), 'tempuser', '[e-mailová adresa byla odstraněna]') USING TTL 3600; -- Data expirují za 1 hodinu (3600 sekund)
    ```

*   **Nastavení TTL při aktualizaci:**

    ```cql
    UPDATE users USING TTL 86400 SET city = 'Prague' WHERE user_id = 123e4567-e89b-12d3-a456-426614174000; -- Nastaví TTL pro sloupec city na 1 den
    ```

* **Nastavení TTL pro celou tabulku**:
    ```cql
      CREATE TABLE my_table (
          id int PRIMARY KEY,
          data text
      ) WITH default_time_to_live = 604800; -- 1 týden v sekundách
    ```
* **Zjištění TTL**
    ```CQL
     SELECT TTL(city) FROM users WHERE user_id = ...;
    ```
*   **Důležité:**  TTL je užitečné pro ukládání dočasných dat (např. session data, cache). Po uplynutí TTL Cassandra data označí náhrobkem (tombstone) a smaže je při compaction.  TTL *nelze* nastavit na sloupce, které jsou součástí primárního klíče.

### 17. Counter Columns - Čítače

*   Speciální datový typ `counter` pro sloupce, které se mají inkrementovat/dekrementovat.
*   Hodnoty čítačů se *nedají přímo nastavovat*, pouze zvyšovat/snižovat.
*   Tabulka s čítači *nesmí* obsahovat jiné sloupce než čítače a primární klíč.

```cql
CREATE TABLE page_views (
    page_id uuid PRIMARY KEY,
    views counter
);

UPDATE page_views SET views = views + 1 WHERE page_id = ...; -- Inkrementace

UPDATE page_views SET views = views - 5 WHERE page_id = ...; -- Dekrementace
```

*   **Důležité:**  Operace s čítači jsou *idempotentní* – opakované provedení stejné operace má stejný efekt jako jedno provedení. To je důležité pro distribuované prostředí, kde se operace mohou ztratit nebo opakovat.  Operace s countery se musí provádět v `UNLOGGED BATCH`.

### 18. Collection Types - Kolekce (List, Set, Map)

*   Umožňují ukládat více hodnot v jednom sloupci.

*   **List:**  Uspořádaný seznam (duplicity povoleny).

    ```cql
    ALTER TABLE users ADD hobbies list<text>;

    UPDATE users SET hobbies = ['reading', 'hiking', 'coding'] WHERE user_id = ...;

    UPDATE users SET hobbies = hobbies + ['swimming'] WHERE user_id = ...; // Přidání prvku na konec

    UPDATE users SET hobbies = ['traveling'] + hobbies WHERE user_id = ...; // Přidání prvku na začátek

    UPDATE users SET hobbies[0] = 'photography' WHERE user_id = ...;  // Změna prvku na indexu 0

    DELETE hobbies[1] FROM users WHERE user_id = ...; // Smazání prvku na indexu 1.

    SELECT hobbies FROM users WHERE user_id = ...;
    ```

*   **Set:**  Neuspořádaná množina (unikátní hodnoty).

    ```cql
    ALTER TABLE users ADD tags set<text>;

    UPDATE users SET tags = {'technology', 'news', 'cassandra'} WHERE user_id = ...;

    UPDATE users SET tags = tags + {'database'} WHERE user_id = ...; -- Přidání prvku

    UPDATE users SET tags = tags - {'news'} WHERE user_id = ...; -- Odebrání prvku
    ```

*   **Map:**  Klíč-hodnota páry.

    ```cql
    ALTER TABLE products ADD attributes map<text, text>;

    UPDATE products SET attributes = {'color': 'red', 'size': 'large'} WHERE product_id = ...;

    UPDATE products SET attributes['weight'] = '1kg' WHERE product_id = ...; -- Přidání/změna hodnoty

    DELETE attributes['size'] FROM products WHERE product_id = ...; -- Smazání klíče
    ```

* **Duležité:** Kolekce jsou vhodné pro ukládání *malého* množství dat. Pro *velké* kolekce použijte raději samostatnou tabulku s kompozitním klíčem.

### 19. Static Columns - Statické Sloupce

*   Sloupce, které mají *stejnou hodnotu* pro všechny řádky v rámci *jedné partition*.
*   Užitečné pro ukládání metadat o partition.

```cql
CREATE TABLE products_by_category (
    category text,
    product_id uuid,
    name text,
    price double,
    category_description text STATIC,  -- Statický sloupec
    PRIMARY KEY (category, product_id)
);

INSERT INTO products_by_category (category, category_description) VALUES ('Electronics', 'Electronic devices and gadgets'); -- Nastaví category_description

INSERT INTO products_by_category (category, product_id, name, price) VALUES ('Electronics', uuid(), 'Laptop', 1200); -- Nemusí se nastavovat category_description

SELECT * FROM products_by_category WHERE category = 'Electronics'; -- category_description bude stejná pro všechny řádky
```

### 20. Uživatelsky Definované Typy (UDT)

* Umožňují definovat vlastní složené datové typy.
```cql
CREATE TYPE mykeyspace.address (
    street text,
    city text,
    zip_code text,
    country text
);

ALTER TABLE users ADD home_address frozen<address>;

UPDATE users
SET home_address = {
    street: '123 Main St',
    city: 'Anytown',
    zip_code: '12345',
    country: 'USA'
}
WHERE user_id = ...;
```
* `frozen`: Zmrazí typ, takže se chová jako jeden celek. Bez `frozen` by bylo možné měnit jednotlivé položky UDT.
