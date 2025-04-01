# Databáze Klíč-Hodnota (Hash)

## 1. Databáze Klíč-Hodnota: Teorie

### 1.1 Datový Model

Databáze klíč-hodnota (key-value store) jsou nejjednodušším typem NoSQL databází. Data jsou ukládána v párech *klíč-hodnota*.

*   **Klíč (Key):** Unikátní identifikátor, obvykle řetězec (string). Slouží k vyhledání a získání hodnoty.
*   **Hodnota (Value):** Data asociovaná s klíčem.  Může to být:
    *   **Jednoduchá hodnota:**  Řetězec, číslo, boolean.
    *   **Složitější struktura:** Seznam (list), množina (set), hash (asociativní pole), atd. (Toto je specifické pro Redis a odlišuje ho od *čistých* key-value storů).

**Příklad:**

| Klíč (Key)   | Hodnota (Value)                |
| :----------- | :----------------------------- |
| `"user:123"` | `"John Doe"`                   |
| `"product:42"` | `"{name: 'Tričko', price: 20}"` |
| `"counter:1"`  | `15`                          |

**Klíčové vlastnosti modelu klíč-hodnota:**

*   **Schéma-less (Schemaless):** Neexistuje žádné předdefinované schéma.  Ke každému klíči můžete přiřadit libovolnou hodnotu.
*   **Vysoká rychlost:** Díky jednoduchosti modelu jsou operace čtení a zápisu *extrémně rychlé*.  Vyhledávání probíhá obvykle v konstantním čase (O(1)) pomocí hashovací tabulky.
*   **Omezené dotazování:**  Můžete získat hodnotu *pouze* na základě jejího *přesného* klíče.  Nelze provádět složité dotazy, filtrování nebo vyhledávání podle rozsahu hodnot (bez použití speciálních struktur, jako jsou sorted sets v Redisu).
*   **Horizontální škálovatelnost:**  Key-value stores jsou obvykle dobře škálovatelné, protože data lze snadno distribuovat na více serverů (sharding) na základě klíče.

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Extrémní rychlost:** Operace čtení a zápisu jsou velmi rychlé, ideální pro aplikace vyžadující nízkou latenci.
*   **Jednoduchost:**  Snadné na pochopení a použití.
*   **Škálovatelnost:** Dobře se škálují horizontálně.
*   **Flexibilita:**  Žádné omezení na typ hodnoty (v závislosti na konkrétní implementaci).

**Nevýhody:**

*   **Omezené dotazování:**  Můžete dotazovat *pouze* na základě *přesné* shody klíče.  Nelze provádět složité dotazy jako WHERE klauzule v SQL.
*   **Žádné transakce (typicky):** Většina key-value stores *nepodporuje* ACID transakce (Atomicity, Consistency, Isolation, Durability) přes více klíčů. (Redis podporuje transakce, ale s omezeními – viz níže).
*   **Žádné vztahy:** Nelze definovat vztahy mezi klíči (jako cizí klíče v relačních databázích).
*   **Relační Integrita:** Databáze nevynucuje integritu vztahů, pokud ukládáte referenční informace

### 1.3 Příklady Databází Klíč-Hodnota

*   **Redis:**  In-memory databáze (data jsou primárně uložena v RAM), která podporuje *různé datové struktury* (řetězce, seznamy, množiny, hashe, sorted sets, atd.).  To z něj dělá *více než jen* čistý key-value store.  Podporuje perzistenci (ukládání na disk), replikaci a clustering.
*   **Memcached:**  In-memory key-value store zaměřený na *čisté cachování*.  Podporuje pouze řetězce jako hodnoty.
*   **Riak KV:**  Distribuovaná key-value databáze zaměřená na vysokou dostupnost a odolnost proti chybám.
*   **Amazon DynamoDB:**  Plně spravovaná key-value a dokumentová databáze nabízená jako služba na AWS.
*   **LevelDB a RocksDB (Key-Value *Knihovny*):**
    *   **LevelDB:** Rychlá key-value storage *knihovna* od Googlu. Není to samostatný server, ale *knihovna*, která se vkládá do vaší aplikace.  Používá Log-Structured Merge-Tree (LSM-Tree) pro optimalizaci zápisů a udržuje klíče *seřazené*. Je vhodný pro embedded systémy a jako úložiště pro jiné databáze.
    *   **RocksDB:** Fork LevelDB od Facebooku, optimalizovaný pro SSD a vysokou zátěž.  Také knihovna, ne server.  Široce používaný (např. v CockroachDB, Apache Cassandra – dříve, Flink, atd.).
    *   **Klíčové rozdíly oproti Redis:** LevelDB/RocksDB jsou *knihovny* (ne servery), nemají nativní síťový přístup (musí se integrovat do aplikace), jsou optimalizované pro perzistentní uložení na disku (i když mohou využívat i RAM), a nepodporují tak širokou škálu datových typů jako Redis (jen klíč-hodnota, kde klíč i hodnota jsou bajtová pole).


### 1.4 Kdy je databáze klíč-hodnota (jako Redis) lepší volbou než relační?
*   **Cachování:**  Ukládání často používaných dat (např. výsledky dotazů do databáze, data relace) v paměti pro rychlý přístup.
*   **Počítadla:**  Udržování počítadel (např. počet zobrazení stránky, počet lajků).
*   **Fronty zpráv:**  Redis Lists mohou sloužit jako jednoduché fronty zpráv.
*   **Žebříčky (Leaderboards):**  Redis Sorted Sets jsou ideální pro udržování žebříčků (např. ve hrách).
*   **Real-time analýza:**  Redis může sloužit k ukládání a agregaci dat v reálném čase (např. počet návštěvníků webu za poslední minutu).
*   **Data s jednoduchou strukturou:**  Pokud nepotřebujete složité vztahy mezi daty, key-value store je jednoduché a efektivní řešení.
*   **Aplikace, kde je rychlost *kritičtější* než složité dotazování a transakce.**

**Kdy Redis *není* dobrá volba:**

*   **Aplikace vyžadující ACID transakce přes *více* klíčů/záznamů:**  Např. bankovní aplikace.  Redis transakce jsou omezené (viz níže).
*   **Aplikace s komplexními vztahy mezi daty:**  Kde potřebujete JOINy a relační integritu.
*   **Aplikace vyžadující složité dotazování a filtrování:**  Kde potřebujete WHERE klauzule, agregace, atd.
*   **Velké objemy dat, které se nevejdou do paměti:**  I když Redis podporuje perzistenci, jeho primární síla je v in-memory operacích.  Pokud data výrazně překračují kapacitu RAM, zvažte jiný typ databáze.

## 2. Redis: Praktický Příklad

Tento příklad ukazuje, jak nastavit Redis pomocí Dockeru, připojit se k němu pomocí `redis-cli` a provádět základní operace s různými datovými typy.

### Struktura

*   **`docker-compose.yml`:** Definuje službu Redis.

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**
2.  **Otevřete terminál** a přejděte do tohoto adresáře.
3.  **Spusťte Redis kontejner:**

    ```bash
    docker-compose up -d
    ```

### Připojení k Redis

*   **Pomocí `redis-cli` (v novém terminálu):**

    ```bash
    docker exec -it redis-server redis-cli
    ```

    Tím se připojíte k Redis serveru běžícímu uvnitř kontejneru.  `redis-cli` je interaktivní terminálový klient pro Redis.

### Základní operace

*   **Nastavení hodnoty (řetězec):**

    ```redis
    SET mykey "Hello Redis"
    ```

    *   `SET`: Příkaz pro nastavení hodnoty.
    *   `mykey`: Klíč.
    *   `"Hello Redis"`: Hodnota (řetězec).

*   **Získání hodnoty:**

    ```redis
    GET mykey
    ```

    *   `GET`: Příkaz pro získání hodnoty.

*   **Smazání klíče:**

    ```redis
    DEL mykey
    ```
    * `DEL`: příkaz pro smazání klíče a hodnoty

*   **Inkrementace čítače:**

    ```redis
    SET counter 10
    INCR counter  # Zvýší hodnotu counter o 1
    GET counter   # Vrátí 11
    INCRBY counter 5 # Zvýší hodnotu o 5
    GET counter   # Vráti 16
    ```

    *   `INCR`: Inkrementuje (zvýší o 1) hodnotu klíče (který musí obsahovat číslo).
    *   `INCRBY`: Inkrementuje o zadanou hodnotu.
    *   Pokud klíč neexistuje, `INCR` a `INCRBY` ho vytvoří s počáteční hodnotou 0.

*   **Decrmentace:**

    ```redis
    DECR counter
    DECRBY counter 3
    ```

### Datové typy v Redis

Redis není *čistý* key-value store, protože podporuje různé datové struktury jako hodnoty.

#### 1. Řetězce (Strings)

*   Základní datový typ.  Může obsahovat text, čísla, binární data.
*   Maximální velikost řetězce je 512 MB.

    ```redis
    SET name "John Doe"
    GET name
    APPEND name " Jr."  # Přidá k existující hodnotě
    GET name
    STRLEN name #Vrátí délku řetězce
    ```
    * `APPEND` přidá text k hodnotě

#### 2. Seznamy (Lists)

*   Uspořádané seznamy řetězců.  Implementované jako *spojové seznamy* (linked lists) – vkládání na začátek/konec je rychlé (O(1)), přístup k prvku podle indexu je pomalejší (O(n)).
*   Použití: fronty zpráv, logy, atd.

    ```redis
    LPUSH mylist "item1"  # Přidá prvek na začátek seznamu
    RPUSH mylist "item2"  # Přidá prvek na konec seznamu
    LRANGE mylist 0 -1  # Vrátí všechny prvky seznamu (0 = první, -1 = poslední)
    LPOP mylist      # Odstraní a vrátí první prvek
    RPOP mylist      # Odstraní a vrátí poslední prvek
    LLEN mylist #vrátí délku seznamu
    LINDEX mylist 0 #Vrátí prvek s indexem 0
    LREM mylist 1 "item2" #Odstraní jeden výskyt prvku item2
    LTRIM mylist 1 -1 #Ořeže na prvky mezi indexy.
    ```
    * `LPUSH`, `RPUSH`: vkládá na začátek, nebo konec
    * `LRANGE`: vypíše seznam, 0 -1, je vše.
    * `LPOP`, `RPOP`: odstranění z příslušného konce.

#### 3. Množiny (Sets)

*   *Neuspořádané* kolekce *unikátních* řetězců.
*   Použití: sledování unikátních návštěvníků, tagy, atd.

    ```redis
    SADD myset "item1"
    SADD myset "item2"
    SADD myset "item1"  # Duplicitní přidání je ignorováno
    SMEMBERS myset  # Vrátí všechny prvky množiny
    SISMEMBER myset "item1" # Zkontroluje, zda prvek existuje v množině (vrátí 1 nebo 0)
    SREM myset "item1" # Odstranění prvku
    SCARD myset #Vrátí počet prvků
    SPOP myset #Odstraní a vrátí náhodný prvek.
    ```
    * `SADD`: přídá prvek
    * `SMEMBERS`: vypíše členy
    * `SISMEMBER`: test na přítomnost

#### 4. Uspořádané Množiny (Sorted Sets)

*   Podobné množinám, ale každý prvek má přiřazené *skóre* (číslo).  Prvky jsou *seřazeny* podle skóre.
*   Použití: žebříčky, časové řady (skóre = timestamp).

    ```redis
    ZADD myzset 10 "item1"  # Přidá prvek se skóre 10
    ZADD myzset 20 "item2"
    ZADD myzset 15 "item3"
    ZRANGE myzset 0 -1 WITHSCORES # Vrátí všechny prvky se skóre (seřazené vzestupně)
    ZRANGEBYSCORE myzset 12 16 WITHSCORES #Vrátí prvky mezi 12 a 16
    ZREVRANGE myzset 0 -1 WITHSCORES # Vrátí prvky se skóre (seřazené sestupně)
    ZREM myzset "item1"
    ZSCORE myzset item3 #Vrátí score pro prvek item3
    ```
    * `ZADD`: přidání
    * `ZRANGE`: rozsah, seřazeno vzestupně
    * `ZREVRANGE`: rozsah, seřazeno sestupně
    * `WITHSCORES`: volitelný parametr pro zobrazení skóre

#### 5. Hashe (Hashes)

*   Ukládají mapování mezi *poli* (fields) a *hodnotami* (values) – podobné objektům v JavaScriptu nebo slovníkům v Pythonu.
*   Použití: ukládání objektů (např. uživatelských profilů).

    ```redis
    HSET user:1 name "John Doe"
    HSET user:1 age 30
    HSET user:1 email "[e-mailová adresa byla odstraněna]"
    HGETALL user:1  # Vrátí všechny pole a hodnoty hashe
    HGET user:1 name   # Vrátí hodnotu pole "name"
    HMGET user:1 name age # Vrati vice hodnot najednou
    HKEYS user:1 #Vrátí všechny klíče.
    HVALS user:1 #vrátí všechny hodnoty
    HEXISTS user:1 name #Zjistí, jestli pole existuje
    HDEL user:1 age #Smaže dané pole
    ```
    * `HSET`: nastaví pole
    * `HGETALL`: získá celou hash
    * `HGET`: získá hodnotu pole

#### 6. Bitmaps
Umožnují pracovat s řetězci jako s polem bitů
```redis
SETBIT mykey 7 1
GETBIT mykey 7 #vrátí 1
BITCOUNT mykey #Vrátí počet jedničkových bitů.
```
* `SETBIT` nastaví bit na pozici
* `GETBIT` vrátí hodnotu bitu
* `BITCOUNT` počet jedničkových bitů

#### 7. HyperLogLog
Pravděpodobnostní datová struktura pro odhad kardinality (počet unikátních prvků v datasetu)
```redis
PFADD myHLL item1 item2 item1 item3
PFCOUNT myHLL #Vrátí odhad 3
```
* `PFADD` Přidá prvek do HyperLogLog. Opakované přidání stejného prvku nemá vliv.
* `PFCOUNT` Vrátí odhadovaný počet unikátních prvků.
* `PFMERGE` Spojí více HyperLogLog struktur do jedné (užitečné pro distribuované počítání).

### Expirace klíčů (TTL)

*   Můžete nastavit, aby klíč automaticky *vypršel* (byl smazán) po určité době.  To je užitečné pro cachování.

    ```redis
    SET mykey "value" EX 60  # Klíč vyprší za 60 sekund
    TTL mykey                # Vrátí zbývající čas do vypršení (v sekundách)
    PERSIST mykey             # Odstraní expiraci (klíč bude existovat neomezeně)
    ```

    ```redis
    SETEX mykey2 60 "hodnota" #Alternativní příkaz, který kombinuje SET a EX.
    ```
    * `EX` (nebo `SETEX`) Nastaví expiraci v sekundách.
    * `PX` (nebo `PSETEX`) Nastaví expiraci v milisekundách.
    * `TTL` Vrátí zbývající čas do vypršení (v sekundách). -1 znamená, že klíč nemá nastavenou expiraci. -2 znamená, že klíč neexistuje.
    * `PTTL` Vrátí zbývající čas do vypršení v milisekundách.
    * `PERSIST` Odstraní expiraci.

### Transakce

Redis podporuje transakce, ale *nejsou* to ACID transakce v plném slova smyslu, jak je známe z relačních databází. V Redisu transakce zaručují:

1.  **Atomicitu (částečně):** Všechny příkazy v transakci jsou provedeny *sekvenčně*, bez interference jiných klientů. *Ale*, pokud některý příkaz v transakci *selže*, Redis *neprovede rollback* (nevrátí změny provedené předchozími příkazy v *téže* transakci).  Redis transakce je tedy atomická v tom smyslu, že se provede celá, *nebo* se v případě *syntaktické* chyby (špatný příkaz) neprovede vůbec. Ale není atomická v případě *runtime* chyb (např. pokus o provedení operace nad nekompatibilním typem).
2.  **Izolaci:** Příkazy od jiných klientů nebudou vloženy mezi příkazy v probíhající transakci.

**Průběh transakce:**

1.  `MULTI`: Označuje začátek transakce.
2.  Příkazy (např. `SET`, `INCR`, `LPUSH`, ...): Tyto příkazy se *nevykonají ihned*, ale zařadí se do *fronty*.
3.  `EXEC`: Spustí všechny příkazy ve frontě.
4.  `DISCARD`: Zruší transakci (zahodí frontu příkazů).
5.  `WATCH`:  Umožňuje *optimistické zamykání*.  Sledujete klíč/e.  Pokud se *před* zavoláním `EXEC` změní hodnota sledovaného klíče jiným klientem, transakce *selže* (nevykoná se).

**Příklad:**

```redis
WATCH mykey  # Sledujeme klíč 'mykey'
MULTI
SET mykey "new value"
INCR counter
EXEC
```

*   Pokud se mezi `WATCH mykey` a `EXEC` změní hodnota `mykey` (jiným klientem), transakce se *neprovede*.  `EXEC` vrátí `nil`.
*   Pokud se `mykey` nezmění, transakce se provede (nastaví se `mykey` a inkrementuje se `counter`).

**Omezení transakcí v Redisu:**

*   **Žádný rollback:**  Jakmile se příkaz v transakci úspěšně provede, jeho změny *zůstanou*, i když následující příkaz v *téže* transakci selže.
*   **Omezená podpora chyb:**  Redis kontroluje *syntaktické* chyby před `EXEC`, ale *runtime* chyby (např. pokus o `INCR` na řetězci) způsobí selhání *pouze* daného příkazu, *ne* celé transakce.
*   **Blokování:** Po dobu provádění transakce, je klient blokován.

### Perzistence (Persistence)

Redis je primárně in-memory databáze, ale nabízí možnosti *perzistence* (ukládání dat na disk), aby se data neztratila při restartu.

1.  **RDB (Redis Database Backup):**
    *   Vytváří *snapshot* (kopii) celého datasetu v daném okamžiku a uloží ho do souboru `.rdb`.
    *   Konfiguruje se v `redis.conf` (např. `save 900 1` – uložit, pokud se za 900 sekund změní alespoň 1 klíč).
    *   Je kompaktnější než AOF (viz níže).
    *   Rychlejší načítání při startu.
    *   *Nevýhoda:*  Můžete ztratit data mezi dvěma snapshoty.
    *  Příkazy: `SAVE` (blokující), `BGSAVE` (neblokující)

2.  **AOF (Append Only File):**
    *   Loguje *každou* operaci zápisu (každý příkaz, který mění data) do souboru.
    *   Při restartu Redis přehraje AOF soubor, čímž obnoví data.
    *   Je *odolnější* proti ztrátě dat než RDB (můžete ztratit maximálně data za 1 sekundu – viz `appendfsync`).
    *   Konfiguruje se v `redis.conf` (např. `appendonly yes`, `appendfsync everysec`).
    *   `appendfsync`:
        *   `always`:  Zapisovat na disk *po každém* příkazu (nejbezpečnější, nejpomalejší).
        *   `everysec`:  Zapisovat na disk *každou sekundu* (dobrý kompromis).
        *   `no`:  Nechat na operačním systému (nejrychlejší, nejméně bezpečné).
    * *Nevýhoda*: AOF soubor může být větší než RDB snapshot a pomalejší při nahrávání

**Doporučení:**  Pro maximální bezpečnost *kombinujte* RDB a AOF.

### Replikace

Redis podporuje *master-slave* replikaci.

*   **Master:** Primární instance, na kterou se provádějí zápisy.
*   **Slave(s):**  Kopie mastera.  Automaticky se synchronizují s masterem.  Mohou obsluhovat *čtení* (read-only).
*   **Výhody:**
    *   **Zvýšení dostupnosti:** Pokud master selže, můžete "povýšit" slave na nového mastera.
    *   **Škálování čtení:**  Čtecí operace můžete rozložit na více slaves.
    *   **Zálohování:**  Slave může sloužit jako záloha.
*   **Konfigurace:**  V `redis.conf` na slave nastavíte `replicaof <master_ip> <master_port>`.

### Redis Cluster

*   Umožňuje *automatické sharding* (rozdělení dat na více Redis instancí).
*   Poskytuje *vysokou dostupnost* a *škálovatelnost* (jak pro čtení, tak pro zápis).
*   Data jsou rozdělena do *slotů* (16384 slotů).  Každý node v clusteru je zodpovědný za určitý rozsah slotů.
*   Klienti se mohou připojit k *libovolnému* nodu v clusteru.  Pokud node neobsahuje data pro daný klíč, přesměruje klienta na správný node.
*   **Konfigurace:**  Složitější než replikace.  Vyžaduje alespoň 3 master nody (a obvykle i odpovídající počet slaves pro zajištění vysoké dostupnosti). Používá se příkaz `redis-cli --cluster create`.

### Pub/Sub (Publish/Subscribe)

*   Redis umožňuje *publish/subscribe* mechanismus pro zasílání zpráv.
*   **Publikování (Publish):** Klient publikuje zprávu na *kanál*.
*   **Odebírání (Subscribe):**  Klienti se přihlásí k odběru kanálu.
*   Všichni klienti, kteří odebírají daný kanál, obdrží zprávu, která je na tento kanál publikována.
*   Použití:  real-time notifikace, chat, atd.

**Příkazy:**

*   `PUBLISH channel message`: Publikuje zprávu na kanál.
*   `SUBSCRIBE channel1 channel2 ...`: Přihlásí klienta k odběru kanálů.
*   `UNSUBSCRIBE [channel1 channel2 ...]`: Odhlásí klienta z odběru kanálů (pokud nejsou specifikovány kanály, odhlásí se ze všech).
*   `PSUBSCRIBE pattern`: Přihlásí k odběru kanálů odpovídajících vzoru (např. `PSUBSCRIBE news.*`).
*   `PUNSUBSCRIBE [pattern]`: Odhlásí z odběru dle vzoru

**Příklad (v `redis-cli`):**

*   **Terminál 1 (subscriber):**

    ```redis
    SUBSCRIBE mychannel
    ```

*   **Terminál 2 (publisher):**

    ```redis
    PUBLISH mychannel "Hello world!"
    ```

*   **Terminál 1 (subscriber) obdrží:**

    ```
    Reading messages... (press Ctrl-C to quit)
    1) "subscribe"
    2) "mychannel"
    3) (integer) 1
    1) "message"
    2) "mychannel"
    3) "Hello world!"
    ```

### Úkoly

1.  **Základní operace a Expirace:**
    * Nastavte klíč `user:name` na vaše jméno.
    * Nastavte klíč `session:123:user_id` na `5`. Nastavte mu expiraci (TTL) na 30 sekund pomocí `EXPIRE` nebo `SETEX`.
    * Pomocí `TTL` ověřte zbývající čas. Počkejte déle než 30 sekund a zkuste získat hodnotu klíče `session:123:user_id` pomocí `GET`. Co se stane?
    * Nastavte čítač `page_views:/home` na 100. Zvyšte ho o 5 pomocí `INCRBY`. Snižte ho o 1 pomocí `DECR`. Získejte aktuální hodnotu.

2.  **Seznamy (Simulace fronty a historie):**
    * Vytvořte seznam `log_messages`. Přidejte 5 různých logovacích zpráv na *začátek* seznamu pomocí `LPUSH`.
    * Zobrazte posledních 5 zpráv (v pořadí, v jakém byly přidány) pomocí `LRANGE`.
    * Simulujte zpracování zprávy: Odstraňte a získejte *nejstarší* zprávu ze seznamu (použijte `RPOP`).
    * **(Bonus - fronta):** Zkuste použít `BRPOP log_messages 10`. Co příkaz dělá, pokud je seznam prázdný? (Vyzkoušejte v jednom terminálu `BRPOP` a v druhém `LPUSH` nějakou zprávu).

3.  **Množiny (Správa tagů a unikátních návštěvníků):**
    * Do množiny `tags:article:101` přidejte tagy "nosql", "redis", "database". Zkuste přidat "redis" znovu. Co se stane?
    * Do množiny `tags:article:102` přidejte tagy "redis", "performance", "caching".
    * Zkontrolujte, zda článek 101 obsahuje tag "java" pomocí `SISMEMBER`.
    * Získejte všechny tagy pro článek 101 pomocí `SMEMBERS`.
    * Najděte tagy, které jsou *společné* pro články 101 a 102 (použijte `SINTER`).
    * Najděte *všechny unikátní* tagy použité v obou článcích (použijte `SUNION`).
    * Kolik tagů má článek 101? (Použijte `SCARD`).

4.  **Uspořádané množiny (Žebříček a časové řady):**
    * Vytvořte žebříček `game:scores`. Přidejte hráče: "Alice" (1500 bodů), "Bob" (1200), "Charlie" (1800), "David" (1500).
    * Zobrazte Top 3 hráče (s nejvyšším skóre) včetně jejich skóre (použijte `ZREVRANGE ... WITHSCORES`).
    * Zobrazte hráče se skóre mezi 1300 a 1600 (použijte `ZRANGEBYSCORE ... WITHSCORES`).
    * Zvyšte skóre hráče "Bob" o 250 bodů (použijte `ZINCRBY`).
    * Zjistěte aktuální skóre hráče "Alice" (`ZSCORE`).
    * Zjistěte pořadí (rank) hráče "Bob" v žebříčku (od nejlepšího, tj. index 0 = nejvyšší skóre) (použijte `ZREVRANK`).

5.  **Hashe (Ukládání strukturovaných dat):**
    * Uložte informace o uživateli s ID `user:99` do Hashe: `name`="Eva Novakova", `email`="[e-mailová adresa byla odstraněna]", `city`="Brno", `visits`=50. Použijte `HSET` nebo `HMSET` (starší verze).
    * Získejte pouze email uživatele 99 (`HGET`).
    * Získejte jméno a město uživatele 99 najednou (`HMGET`).
    * Zvyšte počet návštěv (`visits`) uživatele 99 o 1 (použijte `HINCRBY`).
    * Získejte všechna pole a hodnoty pro uživatele 99 (`HGETALL`).
    * Zkontrolujte, zda má uživatel 99 nastavené pole `zip_code` (`HEXISTS`).

6.  **Kombinace typů (Profil uživatele):**
    * Uložte základní data uživatele `user:7` jako Hash (jméno, email).
    * Uložte seznam posledních 5 ID akcí uživatele `user:7` do Seznamu (List) s klíčem `user:7:recent_actions`. Použijte `LPUSH` a `LTRIM` k udržení pouze posledních 5 akcí.
    * Uložte ID přátel uživatele `user:7` do Množiny (Set) s klíčem `user:7:friends`.

7.  **Transakce (Bezpečný převod bodů):**
    * Představte si, že chcete převést 100 bodů z `user:alice:points` na `user:bob:points`. Oba klíče obsahují čísla (řetězce).
    * Nastavte počáteční hodnoty: `SET user:alice:points 500`, `SET user:bob:points 200`.
    * Napište transakci pomocí `WATCH`, `MULTI`, `DECRBY`, `INCRBY`, `EXEC`, která bezpečně převede 100 bodů.
    * Otestujte: Zkuste spustit transakci. Poté zkuste v jiném terminálu změnit hodnotu `user:alice:points` *mezi* tím, než první terminál spustí `WATCH` a `EXEC`. Co se stane s transakcí? Proč je `WATCH` důležitý?

8.  **Pub/Sub (Notifikace):**
    * V terminálu 1 se přihlaste k odběru kanálu `user:notifications:7` (pro uživatele 7).
    * V terminálu 2 publikujte zprávu `{"type": "new_message", "from_user_id": 8}` na kanál `user:notifications:7`.
    * Ověřte příjem zprávy v terminálu 1.
    * **(Bonus):** V terminálu 1 se přihlaste k odběru vzoru `system:alerts:*` pomocí `PSUBSCRIBE`. V terminálu 2 publikujte zprávu "CPU load high" na kanál `system:alerts:cpu` a zprávu "Disk space low" na `system:alerts:disk`. Ověřte příjem obou zpráv v terminálu 1.

9.  **Bitmaps (Sledování denní aktivity):**
    * Představte si, že chcete sledovat, kteří uživatelé byli aktivní v daný den. Použijte Bitmap. Klíč bude `active_users:2025-03-26`. ID uživatele bude offset bitu.
    * Označte uživatele s ID 10, 55 a 10 jako aktivní pro dnešek (`SETBIT active_users:2025-03-26 <user_id> 1`).
    * Zkontrolujte, zda byl uživatel 55 aktivní (`GETBIT`). Zkontrolujte uživatele 100.
    * Kolik unikátních uživatelů bylo dnes aktivních? (`BITCOUNT`).

10. **Iterace pomocí SCAN:**
    * Přidejte několik klíčů s prefixem `temp:`. Např. `SET temp:a 1`, `SET temp:b 2`, `SET temp:c 3`.
    * Použijte příkaz `SCAN 0 MATCH temp:* COUNT 2`. Co příkaz vrátí? Jak byste pokračovali v iteraci, abyste získali všechny klíče `temp:*`? (Všimněte si vráceného kurzoru). Proč je to lepší než `KEYS temp:*`?

11. **Diskuze:**
    * V jakých konkrétních scénářích z vaší potenciální praxe (webové aplikace, hry, analýza dat...) by byl Redis ideální volbou a proč? Uveďte příklady využití různých datových typů.
    * Kdy byste naopak sáhli po relační databázi (např. PostgreSQL, MySQL) nebo dokumentové databázi (např. MongoDB, CouchDB) místo Redisu? Jaké vlastnosti Redisu by byly limitující?
