# Redis Cheat Sheet

## 1. Základní Příkazy

*   **`SET key value [EX seconds|PX milliseconds|KEEPTTL] [NX|XX]`**: Nastaví hodnotu klíče.
    *   `EX seconds`: Nastaví expiraci v sekundách.
    *   `PX milliseconds`: Nastaví expiraci v milisekundách.
    *   `NX`: Nastaví hodnotu, pouze pokud klíč *neexistuje*.
    *   `XX`: Nastaví hodnotu, pouze pokud klíč *existuje*.
    * `KEEPTTL`: Zachová existující TTL (Time To Live)
*   **`GET key`**: Získá hodnotu klíče.
*   **`DEL key [key ...]`**: Smaže klíč(e).
*   **`EXISTS key [key ...]`**: Zkontroluje, zda klíč(e) existuje(í).
*   **`EXPIRE key seconds`**: Nastaví expiraci klíče v sekundách.
*   **`PEXPIRE key milliseconds`**: Nastaví expiraci v milisekundách
*   **`TTL key`**: Získá zbývající čas do expirace klíče v sekundách (-1 = nemá expiraci, -2 = klíč neexistuje).
*   **`PTTL key`**: Získá zbývající čas v milisekundách.
*   **`PERSIST key`**: Odstraní expiraci klíče.
*   **`TYPE key`**: Vrátí typ hodnoty uložené pod klíčem (string, list, set, zset, hash, stream, none).
*   **`RENAME key newkey`**: Přejmenuje klíč.
*   **`RENAMENX key newkey`**: Přejmenuje klíč, pouze pokud nový klíč neexistuje.
*   **`RANDOMKEY`**: Vrátí náhodný klíč z databáze.
*   **`KEYS pattern`**: Najde klíče odpovídající vzoru (`*` = libovolný řetězec, `?` = jeden libovolný znak, `[abc]` = jeden ze znaků a, b, c).  *Pozor*: `KEYS` může *zablokovat* Redis server na dlouhou dobu, pokud máte mnoho klíčů.  Používejte opatrně (v produkci se *nedoporučuje*).
*    **`SCAN cursor [MATCH pattern] [COUNT count] [TYPE type]`**: *Iterativně* prochází klíče (bez blokování serveru).  Lepší alternativa k `KEYS`.
    ```redis
    SCAN 0 MATCH user:* COUNT 100
    ```
*   **`FLUSHDB [ASYNC]`**: Smaže *všechny* klíče z *aktuální* databáze. `ASYNC` smaže asynchronně (neblokuje).
*   **`FLUSHALL [ASYNC]`**: Smaže *všechny* klíče ze *všech* databází.
*  **`DBSIZE`**: Vrátí počet klíčů v aktuální databázi
* **`SELECT index`**: Přepne aktivní databázi (Redis má ve výchozím stavu 16 databází, indexovaných od 0 do 15).
* **`PING [message]`**: Otestuje spojení se serverem (vrátí "PONG" nebo zadanou zprávu).
* **`ECHO message`**: Vypíše zadanou zprávu.
* **`QUIT`**: Uzavře spojení.

## 2. Řetězce (Strings)

*   **`SET key value [EX seconds|PX milliseconds] [NX|XX]`**: (Viz výše).
*   **`GET key`**: (Viz výše).
*   **`GETSET key value`**: Nastaví novou hodnotu a vrátí *starou* hodnotu.
*   **`APPEND key value`**: Přidá hodnotu na konec existujícího řetězce.
*   **`STRLEN key`**: Vrátí délku řetězce.
*   **`INCR key`**: Inkrementuje (zvýší o 1) hodnotu klíče (musí být číslo).
*   **`INCRBY key increment`**: Inkrementuje o zadanou hodnotu.
*   **`INCRBYFLOAT key increment`** Inkrementuje o zadané desetinné číslo
*   **`DECR key`**: Dekrementuje (sníží o 1).
*   **`DECRBY key decrement`**: Dekrementuje o zadanou hodnotu.
*   **`MSET key value [key value ...]`**: Nastaví více klíčů najednou.
*   **`MGET key [key ...]`**: Získá více hodnot najednou.
*   **`MSETNX key value [key value ...]`**: Nastaví více klíčů, pouze pokud *žádný* z nich neexistuje.
*  **`GETRANGE key start end`:** Vrací substring.
*  **`SETRANGE key offset value`**: Přepíše část stringu od offsetu.

## 3. Seznamy (Lists)

*   **`LPUSH key value [value ...]`**: Přidá prvek/prvky na *začátek* seznamu.
*   **`RPUSH key value [value ...]`**: Přidá prvek/prvky na *konec* seznamu.
*   **`LPOP key`**: Odstraní a vrátí *první* prvek seznamu.
*   **`RPOP key`**: Odstraní a vrátí *poslední* prvek seznamu.
*   **`LINDEX key index`**: Vrátí prvek na zadaném indexu (0 = první, -1 = poslední).
*   **`LLEN key`**: Vrátí délku seznamu.
*   **`LRANGE key start stop`**: Vrátí *rozsah* prvků (včetně start a stop). `LRANGE key 0 -1` vrátí *celý* seznam.
*   **`LREM key count value`**: Odstraní ze seznamu *prvních* `count` výskytů hodnoty `value`.
    *   `count > 0`: Odstraní zleva (od začátku).
    *   `count < 0`: Odstraní zprava (od konce).
    *   `count = 0`: Odstraní *všechny* výskyty.
*   **`LSET key index value`**: Nastaví hodnotu prvku na zadaném indexu.
*   **`LTRIM key start stop`**: Ořízne seznam – ponechá pouze prvky v zadaném rozsahu (včetně start a stop).
*   **`RPOPLPUSH source destination`**: Odstraní poslední prvek ze seznamu `source` a přidá ho na začátek seznamu `destination`. *Atomická operace*.  Používá se pro implementaci spolehlivých front.
*   **`BRPOPLPUSH source destination timeout`**: Blokující verze `RPOPLPUSH`. Čeká na prvek po zadaný `timeout` (v sekundách).
*   **`BLPOP key [key ...] timeout`**: Blokující `LPOP`. Čeká na prvek v *některém* ze zadaných seznamů.
*   **`BRPOP key [key ...] timeout`**: Blokující `RPOP`.

## 4. Množiny (Sets)

*   **`SADD key member [member ...]`**: Přidá prvek/prvky do množiny.
*   **`SREM key member [member ...]`**: Odstraní prvek/prvky z množiny.
*   **`SMEMBERS key`**: Vrátí *všechny* prvky množiny.
*   **`SISMEMBER key member`**: Zkontroluje, zda je prvek členem množiny (vrátí 1 nebo 0).
*   **`SCARD key`**: Vrátí počet prvků v množině (kardinalitu).
*   **`SPOP key [count]`**: Odstraní a vrátí náhodný prvek (nebo `count` prvků) z množiny.
*   **`SRANDMEMBER key [count]`**: Vrátí náhodný prvek (nebo `count` prvků) z množiny *bez odstranění*.
*   **`SMOVE source destination member`**: Přesune prvek z množiny `source` do množiny `destination`. *Atomická operace*.
*   **`SDIFF key [key ...]`**: Vrátí *rozdíl* množin (prvky, které jsou v první množině, ale ne v dalších).
*   **`SDIFFSTORE destination key [key ...]`**: Uloží rozdíl množin do množiny `destination`.
*   **`SINTER key [key ...]`**: Vrátí *průnik* množin.
*   **`SINTERSTORE destination key [key ...]`**: Uloží průnik do `destination`.
*   **`SUNION key [key ...]`**: Vrátí *sjednocení* množin.
*   **`SUNIONSTORE destination key [key ...]`**: Uloží sjednocení do `destination`.

## 5. Uspořádané Množiny (Sorted Sets)

*   **`ZADD key [NX|XX] [GT|LT] [CH] [INCR] score member [score member ...]`**: Přidá prvek/prvky do uspořádané množiny se skóre.
    *   `NX`: Přidá *pouze nové* prvky (neaktualizuje skóre existujících).
    *   `XX`: *Pouze aktualizuje* skóre existujících prvků (nepřidává nové).
    * `GT`: Aktualizuje, pouze pokud je nové skóre *větší*.
    * `LT`: Aktualizuje, pouze pokud je nové skóre *menší*.
    *   `CH`: Vrátí počet *změněných* prvků (včetně nově přidaných).
    *   `INCR`: Zvýší skóre prvku o zadanou hodnotu (jako `ZINCRBY`).
*   **`ZREM key member [member ...]`**: Odstraní prvek/prvky z uspořádané množiny.
*   **`ZRANGE key start stop [WITHSCORES]`**: Vrátí rozsah prvků (seřazených podle skóre *vzestupně*).  `start` a `stop` jsou indexy (0 = první, -1 = poslední).  `WITHSCORES` vrátí i skóre.
*   **`ZREVRANGE key start stop [WITHSCORES]`**: Vrátí rozsah prvků (seřazených *sestupně*).
*   **`ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]`**: Vrátí prvky se skóre mezi `min` a `max` (včetně).  `LIMIT` omezí počet výsledků.  `-inf` a `+inf` reprezentují nekonečno.
*   **`ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]`**: Podobné jako `ZRANGEBYSCORE`, ale seřazeno sestupně.
*  **`ZRANGEBYLEX key min max [LIMIT offset count]`**: Vrací prvky lexikograficky (jako ve slovníku)
*  **`ZREVRANGEBYLEX key max min [LIMIT offset count]`**: Vrací prvky lexikograficky sestupně
*   **`ZSCORE key member`**: Vrátí skóre prvku.
*   **`ZCARD key`**: Vrátí počet prvků v uspořádané množině.
*   **`ZCOUNT key min max`**: Vrátí počet prvků se skóre mezi `min` a `max`.
*   **`ZINCRBY key increment member`**: Zvýší skóre prvku o `increment`.
*   **`ZREM key member [member ...]`**: Smaže prvek
*  **`ZREMRANGEBYRANK key start stop`** Smaže prvky na daných pozicích
*  **`ZREMRANGEBYSCORE key min max`** Smaže prvky mezi minimálním a maximálním score
* **`ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]`**: Spočítá sjednocení uspořádaných množin a uloží výsledek do `destination`.
    * `numkeys`: Počet vstupních množin.
    * `WEIGHTS`: Volitelné váhy pro jednotlivé množiny (pro výpočet výsledného skóre).
    * `AGGREGATE`: Určuje, jak se kombinují skóre (výchozí: `SUM`).
*   **`ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]`**: Spočítá průnik (podobně jako `ZUNIONSTORE`).

## 6. Hashe (Hashes)

*   **`HSET key field value [field value ...]`**: Nastaví pole (field) v hashi.
*   **`HGET key field`**: Získá hodnotu pole.
*   **`HMSET key field value [field value ...]`**: Nastaví více polí najednou (zastaralé, používejte `HSET`).
*   **`HMGET key field [field ...]`**: Získá hodnoty více polí najednou.
*   **`HGETALL key`**: Vrátí *všechna* pole a hodnoty hashe (jako asociativní pole).
*   **`HKEYS key`**: Vrátí *všechna* pole (klíče) hashe.
*   **`HVALS key`**: Vrátí *všechny* hodnoty hashe.
*   **`HLEN key`**: Vrátí počet polí v hashi.
*   **`HEXISTS key field`**: Zkontroluje, zda pole existuje.
*   **`HDEL key field [field ...]`**: Smaže pole z hashe.
*   **`HINCRBY key field increment`**: Inkrementuje hodnotu pole (musí být číslo).
*   **`HINCRBYFLOAT key field increment`**: Inkrementuje hodnotu pole (desetinné číslo).
* **`HSCAN key cursor [MATCH pattern] [COUNT count]`**: Iterativně prochází pole hashe.

## 7. Bitmaps

* **`SETBIT key offset value`**: Nastaví bit na pozici `offset` na hodnotu `value` (0 nebo 1).
* **`GETBIT key offset`**: Získá hodnotu bitu na pozici `offset`.
* **`BITCOUNT key [start end]`**: Spočítá počet bitů nastavených na 1 (v celém řetězci nebo v rozsahu `start`-`end`).
* **`BITOP operation destkey key [key ...]`**: Provede bitovou operaci (AND, OR, XOR, NOT) mezi více bitmapami a uloží výsledek do `destkey`.
* **`BITPOS key bit [start] [end]`**: Najde pozici prvního bitu nastaveného na `bit` (0 nebo 1).

## 8. HyperLogLog

*   **`PFADD key element [element ...]`**: Přidá prvek/prvky do HyperLogLog struktury.
*   **`PFCOUNT key [key ...]`**: Vrátí *odhad* počtu unikátních prvků.
*   **`PFMERGE destkey sourcekey [sourcekey ...]`**: Sloučí více HyperLogLog struktur do jedné (do `destkey`).

## 9. Transakce

*   **`MULTI`**: Označí začátek transakce.
*   **`EXEC`**: Provede všechny příkazy ve frontě transakce.
*   **`DISCARD`**: Zruší transakci (zahodí frontu příkazů).
*   **`WATCH key [key ...]`**: Sleduje klíč(e). Pokud se některý ze sledovaných klíčů změní *před* zavoláním `EXEC`, transakce selže.
*   **`UNWATCH`**: Zruší sledování všech klíčů.

## 10. Pub/Sub

*   **`PUBLISH channel message`**: Publikuje zprávu na kanál.
*   **`SUBSCRIBE channel [channel ...]`**: Přihlásí se k odběru kanálu/kanálů.
*   **`UNSUBSCRIBE [channel [channel ...]]`**: Odhlásí se z odběru kanálu/kanálů (pokud nejsou specifikovány, odhlásí se ze všech).
*   **`PSUBSCRIBE pattern [pattern ...]`**: Přihlásí se k odběru kanálů odpovídajících vzoru (např. `news.*`).
*   **`PUNSUBSCRIBE [pattern [pattern ...]]`**: Odhlásí se z odběru dle vzoru.

## 11. Skriptování (Lua)

Redis umožňuje spouštět skripty napsané v jazyce Lua *přímo na serveru*. To má několik výhod:

*   **Snížení latence:** Skript se provede přímo na serveru, kde jsou data, takže není nutné přenášet data mezi klientem a serverem tam a zpět.
*   **Atomické operace:** Skript se provede *atomicky*. Po dobu běhu skriptu nebudou prováděny žádné jiné příkazy (ani od jiných klientů).
*   **Opakované použití:** Skripty můžete uložit na serveru a volat je jménem.

**Příkazy:**

*   **`EVAL script numkeys key [key ...] arg [arg ...]`**: Spustí Lua skript.
    *   `script`: Samotný Lua skript (jako řetězec).
    *   `numkeys`: Počet *klíčů*, které skript používá. Tyto klíče *musí* být předány jako argumenty (viz níže).
    *   `key [key ...]`: Názvy klíčů, které skript používá.  Redis používá tyto názvy klíčů pro směrování příkazů v clusteru (Redis Cluster).
    *   `arg [arg ...]`: Další argumenty, které můžete předat skriptu.

*   **`EVALSHA sha1 numkeys key [key ...] arg [arg ...]`**: Spustí skript podle jeho SHA1 hashe (pokud byl předtím načten pomocí `SCRIPT LOAD`). Je to efektivnější, než posílat celý skript pokaždé.
* **`SCRIPT LOAD script`:** Nahraje skript na server a vrátí jeho SHA1 hash. Skript se *nevykoná*, pouze se uloží.
    ```redis
     SCRIPT LOAD "return 'Hello, world!'"  # Vrátí "a1b2c3d4..." (SHA1 hash)
     EVALSHA a1b2c3d4... 0  # Spustí skript podle hashe
    ```

*   **`SCRIPT EXISTS sha1 [sha1 ...]`**: Zkontroluje, zda skript(y) s daným SHA1 hashem existuje(í) na serveru (vrátí pole 0 a 1).
*   **`SCRIPT FLUSH [ASYNC|SYNC]`**: Odstraní *všechny* skripty z cache serveru.
*   **`SCRIPT KILL`**: Ukončí právě běžící skript (pokud se zasekl v nekonečné smyčce).

**Přístup k datům v Lua skriptu:**

*   **`KEYS[index]`**: Pole obsahující názvy klíčů předané skriptu.
*   **`ARGV[index]`**: Pole obsahujících další argumenty předané skriptu.
*   **`redis.call(command, arg1, arg2, ...)`**: Zavolá Redis příkaz. Pokud příkaz selže, skript se *ukončí*.
*   **`redis.pcall(command, arg1, arg2, ...)`**: Zavolá Redis příkaz. Pokud příkaz selže, skript *neskončí*, ale `pcall` vrátí chybovou hodnotu.

**Příklad (v `redis-cli`):**

```redis
EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey "My Value"
GET mykey  # Vrátí "My Value"

-- Složitější příklad: Inkrementace čítače a nastavení TTL, pokud ještě neexistuje.
EVAL "if redis.call('EXISTS', KEYS[1]) == 0 then redis.call('SET', KEYS[1], ARGV[1]); redis.call('EXPIRE', KEYS[1], ARGV[2]); return 1; else return redis.call('INCR', KEYS[1]); end" 1 mycounter 1 60
```

**Důležité poznámky k Lua skriptování:**

*   Lua skripty běží v *sandboxu*. Nemají přístup k souborovému systému, síti, atd.
*   Skripty by měly být *krátké* a *rychlé*. Dlouhotrvající skript zablokuje Redis server.
*   Používejte `redis.pcall` místo `redis.call`, pokud chcete ošetřit chyby a zabránit ukončení skriptu.
*   Při práci s Redis Clusterem *všechny klíče, které skript používá, musí být předány jako argumenty* (`KEYS`). Redis to používá k určení, na kterém nodu se má skript spustit.

## 12. Redis Modules

*   Umožňují *rozšířit* funkcionalitu Redis o nové příkazy a datové typy.
*   Moduly se píší v C/C++ a načítají se do Redis serveru.
*   Příklady populárních modulů:
    *   **RedisJSON:** Umožňuje ukládat a dotazovat se na JSON dokumenty.
    *   **RedisGraph:** Umožňuje ukládat a dotazovat se na grafy.
    *   **RedisTimeSeries:** Umožňuje ukládat a dotazovat se na časové řady.
    *   **RedisBloom:** Implementuje pravděpodobnostní datové struktury (Bloom filter, Cuckoo filter).
    *   **RediSearch:**  Fulltextové vyhledávání a sekundární indexy.

## Redis CLI

*   **`redis-cli`**: Interaktivní terminálový klient pro Redis.
*   **Připojení:**
    *   `redis-cli` (připojí se k výchozímu hostu a portu: localhost:6379).
    *   `redis-cli -h <host> -p <port>` (připojení k jinému hostu/portu).
    *   `redis-cli -a <password>` (připojení s heslem).
    * `redis-cli --tls --cert <cert_file> --key <key_file> --cacert <ca_cert_file>` (zabezpečené připojení)
    * `redis-cli --scan --pattern "user:*" ` Prohledá klíče
    * `redis-cli --bigkeys` Najde největší klíče.
    * `redis-cli --stat` Vypíše statistiky
    * `redis-cli --latency` Změří latenci.
*   **Nápověda:** `redis-cli --help`
*   **Spuštění příkazu a ukončení:** `redis-cli PING` (spustí příkaz `PING` a ukončí `redis-cli`).
*   **Monitorování:** `redis-cli MONITOR` (vypisuje *všechny* příkazy, které Redis server přijímá – *používejte opatrně*).
* **Vyhodnocení latence** `redis-cli --latency-history` a `redis-cli --latency-dist`

## Redis a bezpečnost

*   **Heslo:**
    *   Nastavte *silné* heslo v `redis.conf` pomocí direktivy `requirepass`.
    *   Použijte příkaz `AUTH password` pro autentizaci.
*   **Rename Command:**
    *   Zvažte *přejmenování* nebo *zakázání* nebezpečných příkazů (např. `FLUSHALL`, `CONFIG`) v `redis.conf` pomocí direktivy `rename-command`.
        ```
        rename-command FLUSHALL ""  # Zakáže FLUSHALL
        rename-command CONFIG ""
        rename-command KEYS ""
        ```
*   **Síťová bezpečnost:**
    *   Spouštějte Redis na *důvěryhodné síti*.
    *   Omezte přístup k Redis serveru pomocí firewallu (povolte přístup pouze z důvěryhodných IP adres).
    *   Pokud je to možné, *nepřipojujte* Redis přímo k internetu.
* **TLS/SSL:**
     * Používejte Redis s TLS/SSL pro šifrovanou komunikaci.

## Best Practices

*   **Používejte popisné názvy klíčů:**  Např. `user:123:email` místo `u123e`.
*   **Používejte namespace:** Oddělujte různé typy dat pomocí prefixů (např. `user:`, `product:`, `session:`).
*   **Vyhněte se příkazu `KEYS` v produkci.** Používejte `SCAN`.
*   **Zvažte použití expirace (TTL) pro dočasná data.**
*   **Sledujte využití paměti:**  Redis je primárně in-memory databáze.
*   **Používejte správný datový typ pro daný účel:**  Např. Sorted Sets pro žebříčky, Sets pro unikátní hodnoty, Lists pro fronty, atd.
* **Omezte velikost transakcí**.
* **Používejte pipelining pro snížení latence,** pokud provádíte velké množství operací. Pipelining umožňuje klientovi poslat více příkazů najednou, aniž by čekal na odpověď na každý z nich.
*   **Pravidelně zálohujte data.**
* **Používejte Redis Cluster pro vysokou dostupnost a škálovatelnost.**
