# Praktická Ukázka: Sharding s Redis Clusterem pomocí Docker Compose

Tento příklad demonstruje, jak nastavit a spustit jednoduchý Redis Cluster pomocí Docker Compose. Redis Cluster automaticky zajišťuje sharding (rozdělení dat) a replikaci napříč uzly clusteru. Ukážeme si, jak se data distribuují a jak klient komunikuje s clusterem.

## Co je Redis Cluster?

Redis Cluster poskytuje způsob, jak provozovat Redis instalaci, kde jsou data automaticky rozdělena (sharded) mezi více Redis uzlů. Nabízí také určitou míru odolnosti proti chybám díky replikaci master uzlů.

Klíčové vlastnosti:
* **Automatický sharding:** Data jsou rozdělena do 16384 "hash slotů", a každý master uzel v clusteru je zodpovědný za podmnožinu těchto slotů.
* **Master-Slave replikace:** Každý master uzel může mít jednu nebo více replik (slave uzlů) pro vysokou dostupnost.
* **Odolnost proti chybám:** Pokud master uzel selže, jedna z jeho replik může být automaticky povýšena na nového mastera (pokud je cluster správně nakonfigurován a má dostatek replik).
* **Klienti podporující cluster:** Klienti Redis, kteří podporují clusterový režim, dokáží automaticky zjistit, na kterém uzlu se nachází daný klíč, a přesměrovat na něj požadavky.

## Struktura adresáře

```
priklad-sharding-redis-cluster/
├── README.md (Tento soubor)
└── docker-compose.yml
```

## Soubory

### `docker-compose.yml`

Definuje 6 Redis služeb (uzlů), které budou tvořit náš cluster (např. 3 master uzly a 3 slave uzly). Dále definuje příkaz pro inicializaci clusteru.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.

## Spuštění Clusteru

1.  **Otevřete terminál.**
2.  **Přejděte do adresáře** `analyza-IS-NoSQL/03-nastroje/05_Sharding/priklad_sharding_redis_cluster/`.
3.  **Spusťte Redis uzly pomocí Docker Compose:**
    ```bash
    docker-compose up -d
    ```
    Tím se spustí 6 Redis instancí, každá na jiném portu (7000-7005). V tuto chvíli ještě netvoří cluster, jsou to jen samostatné Redis servery.

4.  **Vytvořte Redis Cluster:**
    Po spuštění všech kontejnerů musíme cluster inicializovat. Připojíme se k jednomu z kontejnerů a použijeme `redis-cli` s volbou `--cluster create`.
    Názvy služeb v `docker-compose.yml` (např. `redis-node-1`) se v Docker síti přeloží na IP adresy kontejnerů.

    Spusťte následující příkaz v terminálu na vašem hostitelském stroji:
    ```bash
    docker exec -it redis-node-1 redis-cli --cluster create \
    redis-node-1:6379 redis-node-2:6379 redis-node-3:6379 \
    redis-node-4:6379 redis-node-5:6379 redis-node-6:6379 \
    --cluster-replicas 1 
    ```
    * `docker exec -it redis-node-1 ...`: Spustí příkaz uvnitř kontejneru `redis-node-1`.
    * `redis-cli --cluster create ...`: Nástroj pro vytvoření clusteru.
    * `redis-node-X:6379`: Seznam všech uzlů, které mají být součástí clusteru (název služby a interní port Redis).
    * `--cluster-replicas 1`: Tento příznak říká `redis-cli`, aby se pokusil pro každý master uzel vytvořit jednu repliku. S 6 uzly to znamená, že budeme mít 3 mastery a 3 repliky. `redis-cli` se pokusí repliky inteligentně rozdělit.

    Budete dotázáni, zda souhlasíte s navrženou konfigurací slotů. Napište `yes` a stiskněte Enter.

5.  **Ověřte stav clusteru:**
    Připojte se k libovolnému uzlu a zkontrolujte stav:
    ```bash
    docker exec -it redis-node-1 redis-cli cluster nodes
    # nebo
    docker exec -it redis-node-1 redis-cli -p 6379 cluster info 
    # (pokud jste uvnitř kontejneru redis-node-1, stačí redis-cli cluster nodes)
    ```
    Měli byste vidět seznam všech uzlů, jejich role (master/slave) a rozdělení slotů.

## Testování Shardingu a Přesměrování

Klienti Redis, kteří podporují clusterový režim (většina moderních klientů, včetně `redis-cli` s přepínačem `-c`), automaticky zpracovávají přesměrování.

1.  **Připojte se k libovolnému uzlu clusteru v "cluster mode" pomocí `redis-cli -c`:**
    ```bash
    docker exec -it redis-node-1 redis-cli -c -p 6379
    # Přepínač -c je důležitý pro clusterový režim (umožňuje sledovat přesměrování)
    # -p 6379 je port, na kterém Redis naslouchá uvnitř kontejneru
    ```
    Alternativně se můžete připojit k portu, který jste namapovali na hostitele, např.:
    ```bash
    redis-cli -c -p 7000 
    ```
    (Pokud máte `redis-cli` nainstalovaný na hostitelském systému.)

2.  **Zkuste nastavit a získat několik klíčů:**
    ```redis
    SET foo bar
    GET foo
    SET anotherkey "some value"
    GET anotherkey
    SET user:1000:name "Alice"
    GET user:1000:name
    ```
    Při nastavování klíčů si všimněte, že `redis-cli` může zobrazit zprávu o přesměrování, pokud klíč patří do slotu spravovaného jiným uzlem. Např.:
    `-> Redirected to slot [12182] located at 172.20.0.3:6379`
    Následný příkaz `GET` pro tento klíč bude již automaticky směrován na správný uzel.

3.  **Distribuce klíčů:**
    Zkuste vložit více klíčů a poté se připojit k různým uzlům clusteru (např. `redis-cli -c -p 7000`, `redis-cli -c -p 7001`, atd. z vašeho hosta) a pomocí příkazu `KEYS *` (použijte opatrně na produkci!) nebo `SCAN 0` zjistit, které klíče jsou uloženy na daném uzlu. Měli byste vidět, že klíče jsou distribuovány mezi master uzly.

    Například, po připojení k `redis-node-1` (port 7000):
    ```redis
    # Uvnitř redis-cli -c -p 7000
    CLUSTER KEYSLOT anotherkey  # Zjistí slot pro daný klíč
    CLUSTER GETKEYSINSLOT <slot_number> 10 # Získá až 10 klíčů z daného slotu
    ```

## Zastavení Clusteru

Pro zastavení a odstranění kontejnerů:
```bash
docker-compose down
```
Pro odstranění i volumes (pokud by byly vytvořeny pro perzistenci dat, což v tomto `docker-compose.yml` není explicitně pro data, ale Docker může vytvořit anonymní volumes pro konfiguraci):
```bash
docker-compose down -v
```

Tento příklad poskytuje základní vhled do toho, jak Redis Cluster funguje a jak se data automaticky shardují. V reálném nasazení by bylo potřeba řešit perzistenci dat, detailnější konfiguraci sítě a robustnější monitoring.
