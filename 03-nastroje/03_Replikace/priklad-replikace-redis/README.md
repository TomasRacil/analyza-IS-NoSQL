# Praktická Ukázka: Redis Master-Slave Replikace s Docker Compose

Tento příklad demonstruje nastavení jednoduché Master-Slave replikace pro Redis pomocí Docker Compose. Budeme mít jednu Redis instanci jako master a jednu (nebo více) instancí jako slave. Zápisy budou probíhat na mastera a automaticky se replikovat na slave(s). Čtení bude možné provádět jak z mastera, tak ze slave(s).

## Struktura adresáře

```
priklad-redis-replikace/
├── README.md (Tento soubor)
└── docker-compose.yml
```

## Soubory

### `docker-compose.yml`

Definuje dvě Redis služby:
* `redis-master`: Hlavní Redis server, který přijímá zápisy.
* `redis-slave`: Redis server nakonfigurovaný jako replika (slave) `redis-master` instance.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.

## Spuštění

1.  Otevřete terminál.
2.  Přejděte do adresáře `analyza-IS-NoSQL/03-nastroje/03_Replikace/priklad_redis_replikace/`.
3.  Spusťte Redis instance pomocí Docker Compose:
    ```bash
    docker-compose up -d
    ```
    * `-d` spustí kontejnery na pozadí.

Služby by nyní měly běžet:
* `redis-master` na portu `6379` (výchozí Redis port, mapovaný na hostitele).
* `redis-slave` na portu `6380` (mapovaný na hostitele, aby se předešlo konfliktu s masterem, pokud byste chtěli přistupovat k oběma přímo z hostitele pro testování).

## Testování Replikace

K testování použijeme `redis-cli` (Redis command-line interface).

### 1. Připojení k Master instanci a zápis dat

Otevřete nový terminál a připojte se k `redis-master`:
```bash
docker exec -it redis-master-repl redis-cli
```

Uvnitř `redis-cli` mastera proveďte nějaké zápisy:
```redis
SET mujklic "Toto je hodnota z mastera"
INCR pocitadlo
LPUSH mojefronta "prvek1"
LPUSH mojefronta "prvek2"
```
Ukončete `redis-cli` mastera: `exit`

### 2. Připojení k Slave instanci a čtení dat

Nyní se připojte k `redis-slave` v jiném terminálu (nebo ve stejném po ukončení master `redis-cli`):
```bash
docker exec -it redis-slave-repl redis-cli
```

Uvnitř `redis-cli` slavea zkuste přečíst data, která jste zapsali na mastera:
```redis
GET mujklic
GET pocitadlo
LRANGE mojefronta 0 -1
```
Měli byste vidět stejné hodnoty, jaké jste nastavili na masteru, což potvrzuje, že replikace funguje.

### 3. Pokus o zápis na Slave instanci (mělo by selhat nebo být ignorováno)

Redis slave je ve výchozím nastavení read-only. Zkuste na slave něco zapsat:
```redis
SET novyklicnaslavu "tato hodnota by se neměla zapsat"
```
Pravděpodobně dostanete chybu `(error) READONLY You can't write against a read only replica.` nebo příkaz proběhne bez chyby, ale data se neuloží a nebudou replikována zpět na mastera.

Ukončete `redis-cli` slavea: `exit`

### 4. Ověření informací o replikaci (volitelné)

Na masteru můžete zobrazit informace o připojených slavech:
```bash
docker exec -it redis-master-repl redis-cli INFO replication
```
Hledejte sekci `# Replication` a informace o `connected_slaves`.

Na slaveu můžete zobrazit informace o jeho masteru:
```bash
docker exec -it redis-slave-repl redis-cli INFO replication
```
Hledejte informace jako `master_host`, `master_port`, `master_link_status`.

## Zastavení služeb

Pro zastavení a odstranění kontejnerů definovaných v `docker-compose.yml` použijte:
```bash
docker-compose down
```
Pokud chcete smazat i volumes (pokud by byly definovány pro perzistenci, což v tomto jednoduchém příkladu nejsou explicitně pro Redis data, ale Docker může vytvářet anonymní volumes):
```bash
docker-compose down -v
```

Tento příklad ukazuje základní princip Master-Slave replikace. V produkčních prostředích by konfigurace zahrnovala více slave instancí, perzistenci dat a často také Redis Sentinel pro automatické failover (přepnutí na slavea, pokud master selže) nebo Redis Cluster pro pokročilejší distribuci a vysokou dostupnost.
