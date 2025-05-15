# Sharding (Horizontální Dělení Dat)

## 1. Úvod do Shardingu

Jak databáze rostou co do objemu dat a počtu požadavků, mohou narazit na limity výkonu a kapacity jednoho serveru. **Vertikální škálování** (přidávání více CPU, RAM, rychlejších disků na existující server) má své meze a může být velmi nákladné. **Sharding** (někdy označovaný jako horizontální dělení nebo horizontální škálování) je technika, která řeší tento problém rozdělením databáze na menší, rychlejší a snadněji spravovatelné části, nazývané **shardy**. Každý shard je v podstatě samostatná databáze, která obsahuje podmnožinu celkových dat, a tyto shardy mohou být hostovány na různých serverech.

Cílem shardingu je:
* **Zvýšení výkonu:** Požadavky mohou být směrovány pouze na relevantní shard(y), čímž se snižuje zátěž jednotlivých serverů a zrychluje se odezva.
* **Zvýšení kapacity:** Celková úložná kapacita systému je součtem kapacit všech shardů.
* **Zlepšení dostupnosti:** Pokud jeden shard selže, ostatní shardy mohou zůstat funkční (i když to závisí na konkrétní architektuře a kombinaci s replikací).
* **Distribuce zátěže:** Zátěž (čtení i zápis) je rozložena mezi více serverů.

## 2. Jak Sharding Funguje

Klíčovým prvkem shardingu je **sharding klíč (shard key)**. Je to jeden nebo více sloupců (atributů) v datech, jejichž hodnota určuje, na který shard budou daná data uložena. Když aplikace potřebuje přistoupit k datům, musí existovat mechanismus (často nazývaný **router** nebo **query router**), který na základě sharding klíče v dotazu určí, na který shard má dotaz směrovat.

**Základní komponenty sharded architektury:**

1.  **Shardy:** Jednotlivé databázové servery (nebo instance), které uchovávají část dat. Každý shard je sám o sobě databází. Pro zajištění vysoké dostupnosti je každý shard často replikován (např. pomocí replica setu v MongoDB).
2.  **Query Router (např. `mongos` v MongoDB):** Aplikační vrstva nebo samostatný proces, který přijímá dotazy od klientů, analyzuje je, určí na základě sharding klíče cílový shard(y) a přesměruje na ně dotaz. Poté shromáždí výsledky z jednotlivých shardů a vrátí je klientovi.
3.  **Config Servers (Konfigurační servery):** Ukládají metadata o sharded clusteru, včetně informací o tom, jak jsou data rozdělena mezi shardy (mapování sharding klíčů na shardy). Query routery se dotazují konfiguračních serverů, aby zjistily, kam směrovat dotazy. Tyto servery musí být vysoce dostupné.

## 3. Strategie Shardingu (Výběr Shard Klíče)

Výběr správného sharding klíče a strategie je kritický pro efektivitu shardingu. Špatně zvolený klíč může vést k nevyváženému rozložení dat nebo zátěže (tzv. "hot spots").

* **Range-Based Sharding (Dělení podle rozsahu):**
    * Data jsou rozdělena na základě rozsahů hodnot sharding klíče. Například, pokud je sharding klíčem PSČ, shard 1 může obsahovat PSČ 10000-19999, shard 2 PSČ 20000-29999 atd.
    * **Výhody:** Snadné pro dotazy na rozsahy (např. "najdi všechny uživatele s PSČ mezi 15000 a 18000" půjde na jeden nebo malý počet shardů).
    * **Nevýhody:** Může vést k nevyváženému rozložení dat a zátěže, pokud hodnoty sharding klíče nejsou rovnoměrně distribuovány (např. více uživatelů v určitých rozsazích PSČ). Může také vést k "hot spotům" při sekvenčním vkládání dat (např. pokud je sharding klíčem časové razítko, všechny nové zápisy půjdou na poslední shard).

* **Hash-Based Sharding (Dělení podle hashe):**
    * Hodnota sharding klíče je nejprve zahashována a na základě výsledku hashe jsou data přiřazena shardu.
    * **Výhody:** Obvykle vede k rovnoměrnějšímu rozložení dat a zátěže napříč shardy, protože hashovací funkce distribuuje klíče náhodněji.
    * **Nevýhody:** Dotazy na rozsahy hodnot sharding klíče jsou neefektivní, protože data s blízkými hodnotami klíče mohou skončit na různých shardech. Vyžadují dotazování všech shardů (scatter-gather).

* **Directory-Based Sharding (Dělení podle adresáře/lookup tabulky):**
    * Používá se lookup tabulka (adresář), která explicitně mapuje každou hodnotu (nebo rozsah) sharding klíče na konkrétní shard.
    * **Výhody:** Velká flexibilita při mapování dat na shardy.
    * **Nevýhody:** Lookup tabulka se může stát úzkým hrdlem a vyžaduje správu.

* **Geo-Based Sharding (Geografické dělení):**
    * Data jsou distribuována na základě geografické polohy (např. uživatelé z Evropy na evropských serverech, uživatelé z Asie na asijských serverech).
    * **Výhody:** Snižuje latenci pro uživatele, pomáhá splnit legislativní požadavky na suverenitu dat.
    * **Nevýhody:** Složitější implementace, vyžaduje logiku pro směrování na základě polohy.

## 4. Výhody Shardingu

* **Horizontální škálovatelnost:** Téměř neomezená schopnost růstu přidáváním dalších serverů (shardů).
* **Zvýšený výkon:** Rozdělení dat a zátěže vede k rychlejším dotazům a vyšší propustnosti.
* **Vylepšená dostupnost:** V kombinaci s replikací může selhání jednoho shardu ovlivnit pouze část dat, nikoli celý systém.
* **Možnost geografické distribuce dat.**

## 5. Nevýhody a Výzvy Shardingu

* **Zvýšená komplexita architektury:** Správa sharded clusteru (routery, config servery, shardy) je složitější než správa jedné databáze.
* **Složitost dotazování:**
    * Dotazy, které nezahrnují sharding klíč, mohou vyžadovat prohledání všech shardů (scatter-gather), což může být pomalé.
    * JOIN operace napříč shardy jsou obvykle velmi neefektivní nebo nepodporované. Data se často musí denormalizovat nebo se JOINy provádějí na aplikační úrovni.
* **Výběr sharding klíče:** Kritické rozhodnutí, které je těžké později změnit. Špatná volba může vést k nevyváženosti.
* **Transakce:** Distribuované transakce napříč shardy jsou složité na implementaci a často mají dopad na výkon nebo nejsou plně podporovány (mnoho systémů nabízí ACID pouze v rámci jednoho shardu).
* **Rebalancing (Přerozdělování dat):** Pokud přidáte nový shard nebo pokud se data nerovnoměrně rozdělí, je potřeba data mezi shardy přerozdělit (rebalance). Tento proces může být náročný na zdroje a čas.
* **"Hot Spots":** Některé shardy mohou být více zatížené než jiné kvůli nerovnoměrné distribuci dat nebo přístupových vzorců.
* **Provozní náklady:** I když jednotlivé servery mohou být levnější, celkový počet serverů a složitost správy mohou zvýšit provozní náklady.

## 6. Kdy Zvážit Sharding?

Sharding není univerzálním řešením a měl by být zvažován, až když jiné metody optimalizace (např. optimalizace dotazů, indexace, vertikální škálování, cachování, replikace pro čtení) již nestačí.

Typické scénáře pro sharding:
* Velmi velké datové sady, které se nevejdou na jeden server nebo jejichž správa na jednom serveru je neefektivní.
* Vysoká zátěž pro zápis, kterou jeden server nezvládá.
* Požadavky na vysokou propustnost pro čtení, které nelze uspokojit pouze replikací.
* Potřeba geografické distribuce dat.

## 7. Sharding v Různých Databázových Systémech

* **MongoDB:** Nativně podporuje automatický sharding. Používá `mongos` routery, config servery a replica sety pro každý shard. Podporuje range-based i hash-based sharding.
* **Cassandra:** Je navržena jako distribuovaná databáze "bez mastera". Data jsou automaticky distribuována (partitioned) napříč clusterem pomocí konzistentního hashování primárního klíče. Replikace je také vestavěná.
* **Elasticsearch:** Distribuovaný vyhledávací a analytický engine. Indexy jsou rozděleny na shardy, které jsou distribuovány mezi uzly clusteru.
* **Redis Cluster:** Poskytuje způsob, jak automaticky rozdělit data (sharding) a zajistit redundanci (replikaci) napříč více Redis uzly.
* **Relační databáze (např. PostgreSQL, MySQL):** Nemají nativní podporu pro automatický sharding tak robustní jako některé NoSQL systémy. Sharding se často implementuje pomocí:
    * **Aplikační logiky:** Aplikace sama rozhoduje, na který databázový server (shard) se připojit.
    * **Proxy vrstev:** Nástroje jako Vitess (pro MySQL) nebo Pgpool-II, Patroni (pro PostgreSQL s určitými omezeními) mohou poskytovat transparentní sharding.
    * **Federovaných databází.**
* **CockroachDB, YugabyteDB:** Distribuované SQL databáze navržené od základu pro horizontální škálovatelnost a odolnost proti chybám, kde je sharding (často nazývaný partitioning nebo ranges/tablets) klíčovou součástí architektury.

## 8. Praktická Ukázka

Praktická demonstrace plnohodnotného shardingu s více databázovými instancemi, routery a config servery pomocí Docker Compose může být poměrně komplexní. Například nastavení sharded clusteru MongoDB vyžaduje několik kontejnerů pro shard servery (každý jako replica set), config servery (také jako replica set) a `mongos` routery.

Pro výukové účely se zaměříme na **konceptuální ukázku shardingu Redis Clusteru**, která ilustruje základní principy rozdělení dat na základě sharding klíče a směrování dotazů.

**Kde příklad najdete:**

* Adresář: `priklad-sharding-redis-cluster/` (v rámci této sekce `05_Sharding`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad-sharding-redis-cluster/README.md`.

**Co příklad ukáže (Redis Cluster):**

* Jak nastavit jednoduchý Redis Cluster s několika master a replica uzly pomocí Docker Compose.
* Jak se Redis Cluster automaticky stará o distribuci dat (sharding) mezi master uzly na základě hashe klíče.
* Jak se připojit ke clusteru a provádět operace čtení a zápisu, přičemž klient (nebo cluster sám) transparentně směruje požadavky na správný shard.

Tato ukázka demonstruje jak sharding funguje v praxi u databáze, která jej nativně podporuje.
