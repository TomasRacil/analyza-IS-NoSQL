## 5. NoSQL databáze pro Big Data (přehled a srovnání)

V předchozích kapitolách jsme se seznámili s různými typy NoSQL databází a také s problematikou Big Data. Nyní tyto dvě oblasti propojíme a podíváme se, jak specifické vlastnosti různých NoSQL databází vyhovují požadavkům na ukládání, správu a analýzu velkých objemů dat.

### 5.1 Proč NoSQL pro Big Data?

Jak jsme již diskutovali v úvodu do Big Data, tradiční relační databáze (RDBMS) narážejí při práci s charakteristikami Big Data (objem, rychlost, rozmanitost) na své limity. NoSQL databáze byly často navrženy právě s ohledem na tyto výzvy a nabízejí:

-   **Horizontální škálovatelnost:** Většina NoSQL databází je navržena pro snadné horizontální škálování (přidáváním dalších serverů do clusteru), což je klíčové pro zvládnutí velkých objemů dat a vysoké zátěže.
-   **Flexibilita schématu:** Schopnost pracovat s polostrukturovanými a nestrukturovanými daty bez nutnosti předem definovat rigidní schéma (schema-on-read) je pro rozmanitost Big Data ideální.
-   **Vysoký výkon pro specifické operace:** Různé typy NoSQL databází jsou optimalizovány pro specifické přístupové vzory a operace (např. rychlé zápisy, rychlé čtení podle klíče, efektivní travers grafem).
-   **Odolnost proti chybám a vysoká dostupnost:** Mnoho NoSQL systémů má vestavěné mechanismy pro replikaci a failover.

### 5.2 Přehled typů NoSQL databází a jejich vhodnost pro Big Data

Připomeňme si hlavní typy NoSQL databází a zhodnoťme jejich silné a slabé stránky v kontextu Big Data:

#### a) Dokumentové databáze (např. MongoDB, CouchDB, Azure Cosmos DB)

-   **Silné stránky pro Big Data:**
    -   **Flexibilní schéma:** Ideální pro ukládání různorodých dat (JSON/BSON dokumenty), častých v Big Data scénářích (např. data z webových aplikací, logy, uživatelské profily).
    -   **Škálovatelnost:** Dobrá podpora horizontálního škálování (sharding).
    -   **Výkon:** Rychlé dotazy na základě indexovaných polí v dokumentech. Vnořené dokumenty mohou snížit potřebu joinů.
    -   **Vývojářská přívětivost:** Přirozené mapování na objekty v programovacích jazycích.

-   **Slabé stránky / Výzvy pro Big Data:**
    -   **Komplexní transakce:** Transakce přes více dokumentů mohou být omezené nebo náročnější na implementaci než v RDBMS.
    -   **JOIN operace:** Absence nativních JOINů znamená, že propojení dat z různých kolekcí se musí řešit na aplikační úrovni nebo denormalizací, což nemusí být vždy efektivní pro komplexní analytické dotazy nad velkými daty.
    -   **Agregace:** I když podporují agregace (např. MongoDB Aggregation Framework), pro extrémně velké analytické úlohy mohou být méně výkonné než specializované analytické platformy.

-   **Typické použití v Big Data:**
    -   Ukládání a správa velkých objemů polostrukturovaných dat (např. produktové katalogy, obsahové systémy, data z IoT zařízení s proměnlivou strukturou).
    -   Uživatelské profily a personalizace ve velkém měřítku.
    -   Real-time analýza menšího rozsahu, pokud struktura dat dobře odpovídá dokumentovému modelu.

#### b) Sloupcové (Column-Family) databáze (např. Apache Cassandra, HBase, Google Bigtable)

-   **Silné stránky pro Big Data:**
    -   **Masivní škálovatelnost:** Navrženy pro extrémní horizontální škálovatelnost na stovky až tisíce uzlů.
    -   **Vysoká propustnost zápisu:** Optimalizovány pro velmi rychlé zápisy velkého objemu dat (ideální pro ingesci streamovaných dat).
    -   **Efektivní práce s řídkými daty:** Ukládají pouze existující sloupce, což šetří místo.
    -   **Vysoká dostupnost a odolnost proti chybám:** Architektura bez mastera (v případě Cassandry) a automatická replikace.
    -   **Dobré pro časové řady a analytické dotazy na podmnožinu sloupců:** Rychlé čtení, pokud se dotazujeme na specifické sloupce napříč mnoha řádky.

-   **Slabé stránky / Výzvy pro Big Data:**
    -   **Omezená flexibilita dotazování:** Dotazy jsou primárně vázány na primární klíč (partition key a clustering columns). Ad-hoc dotazy na neindexované sloupce jsou neefektivní.
    -   **Náročnější modelování dat:** Vyžaduje pečlivé navrhování datového modelu (denormalizace, tabulky optimalizované pro konkrétní dotazy).
    -   **Eventual consistency:** Často nabízejí nastavitelnou konzistenci, ale dosažení silné konzistence může ovlivnit výkon a dostupnost.

-   **Typické použití v Big Data:**
    -   Ukládání a analýza obrovských objemů časových řad (např. data z IoT senzorů, metriky monitoringu, logy událostí).
    -   Real-time analytické platformy, kde je klíčová rychlost zápisu a škálovatelnost.
    -   Systémy pro detekci podvodů, personalizované doporučování ve velkém měřítku.
    -   Jako backendové úložiště pro jiné Big Data nástroje.

#### c) Klíč-hodnota (Key-Value) a Hashovací databáze (např. Redis, Amazon DynamoDB, Memcached)

-   **Silné stránky pro Big Data:**
    -   **Extrémní rychlost a nízká latence:** Pro jednoduché operace GET/SET na základě klíče.
    -   **Vysoká škálovatelnost:** Relativně snadno škálovatelné horizontálně.
    -   **Jednoduchost:** Jednoduchý datový model a API.
    -   **Caching:** Ideální pro cachovací vrstvy před pomalejšími databázemi nebo službami. Redis navíc nabízí pokročilé datové struktury (seznamy, množiny, hashe, sorted sets), které rozšiřují jeho použitelnost.

-   **Slabé stránky / Výzvy pro Big Data:**
    -   **Velmi omezené možnosti dotazování:** Pouze na základě klíče. Analýza dat uložených tímto způsobem je obtížná bez externích nástrojů.
    -   **Správa vztahů:** Nejsou navrženy pro ukládání komplexních vztahů mezi daty.
    -   **Perzistence a velikost dat (pro in-memory varianty jako Redis):** I když Redis podporuje perzistenci, jeho síla je v in-memory operacích. Velikost datasetu je omezena dostupnou RAM (i když clustering pomáhá).

-   **Typické použití v Big Data:**
    -   **Cachovací vrstvy:** Pro zrychlení přístupu k často čteným datům.
    -   **Ukládání uživatelských relací (session store).**
    -   **Fronty zpráv (Redis Lists/Streams).**
    -   **Real-time počítadla, žebříčky (Redis Sorted Sets).**
    -   Rychlé úložiště pro dočasná data nebo metadata v rámci Big Data pipeline.

#### d) Grafové databáze (např. Neo4j, Amazon Neptune, ArangoDB)

-   **Silné stránky pro Big Data:**
    -   **Efektivní práce s komplexními vztahy a sítěmi:** Ideální pro datové sady, kde jsou vztahy mezi entitami klíčové.
    -   **Rychlé traversy grafem:** Dotazy sledující vztahy (např. "najdi přátele přátel", "doporuč produkty na základě nákupů podobných uživatelů") jsou velmi výkonné.
    -   **Intuitivní modelování propojených dat.**

-   **Slabé stránky / Výzvy pro Big Data:**
    -   **Horizontální škálovatelnost (pro některé implementace):** Škálování grafových databází na extrémně velké grafy rozložené na mnoho uzlů může být technicky náročné. Některé (Neo4j) tradičně preferovaly vertikální škálování nebo replikaci pro čtení, i když se objevují řešení pro lepší distribuci.
    -   **Agregace nad celým grafem:** Provedení agregací nad všemi uzly nebo hranami (pokud nesouvisí s traversy) nemusí být tak efektivní jako v jiných typech databází.
    -   **Méně vhodné pro data bez výrazných vztahů.**

-   **Typické použití v Big Data:**
    -   Analýza sociálních sítí a vlivu.
    -   Doporučovací systémy (collaborative filtering, content-based filtering na základě vztahů).
    -   Detekce podvodů a anomálií v propojených datech (např. finanční transakce, sítě).
    -   Správa znalostních grafů (knowledge graphs).
    -   Master Data Management, kde je důležité pochopit vztahy mezi datovými entitami.
    -   Síťová a IT operations analýza.

#### e) Time Series Databáze (TSDB) (např. InfluxDB, Prometheus, TimescaleDB)

-   **Silné stránky pro Big Data:**
    -   **Optimalizace pro časová data:** Vysoká propustnost zápisu pro data s časovým razítkem.
    -   **Efektivní ukládání a komprese:** Časové řady mají často specifické vzory, které TSDB umí využít pro kompresi.
    -   **Rychlé časově orientované dotazy a agregace:** Funkce pro downsampling, klouzavé průměry, výběry časových oken.
    -   **Retention policies:** Automatická správa životního cyklu dat.

-   **Slabé stránky / Výzvy pro Big Data:**
    -   **Specializované použití:** Navrženy specificky pro časové řady; méně vhodné pro jiné typy dat.
    -   **Vztahy a JOINy:** Obvykle nepodporují komplexní vztahy mezi různými metrikami nebo entitami (TimescaleDB jako rozšíření PostgreSQL je výjimkou).

-   **Typické použití v Big Data:**
    -   Monitorování IT infrastruktury, serverů, aplikací.
    -   Sběr a analýza dat z IoT senzorů a zařízení.
    -   Analýza finančních trhů (ceny akcií, měn).
    -   Logování událostí v reálném čase.
    -   DevOps a monitoring výkonu aplikací (APM).

### 5.3 Srovnávací tabulka klíčových charakteristik pro Big Data

| Charakteristika | Dokumentové DB | Sloupcové DB | Klíč-Hodnota DB | Grafové DB | Time Series DB |
| :-------------------------- | :-------------------- | :---------------------- | :---------------------- | :---------------------- | :---------------------- |
| **Horizontální škálovatelnost** | Dobrá až velmi dobrá | Velmi dobrá až excelentní | Velmi dobrá až excelentní | Omezená až dobrá | Dobrá až velmi dobrá |
| **Flexibilita schématu** | Vysoká | Vysoká (na úrovni řádku) | Velmi vysoká (hodnota) | Vysoká | Střední (tagy flexibilní, pole méně) |
| **Flexibilita dotazování** | Střední až dobrá | Nízká až střední | Velmi nízká | Velmi vysoká (pro vztahy) | Střední (časové filtry, tagy) |
| **Propustnost zápisu** | Dobrá | Velmi vysoká | Extrémně vysoká | Střední až dobrá | Velmi vysoká |
| **Propustnost čtení (klíč)**| Velmi dobrá | Velmi dobrá | Extrémně vysoká | Dobrá | Dobrá |
| **Propustnost čtení (analytické)** | Střední | Dobrá (pro sloupce) | Nízká | Střední (pro traversy) | Dobrá (agregace v čase) |
| **Konzistence (typicky)** | Eventual/Nastavitelná | Eventual/Nastavitelná | Eventual/Nastavitelná | ACID (Neo4j) / Eventual | Eventual/Nastavitelná |
| **Složitost modelu** | Nízká až střední | Střední až vysoká | Velmi nízká | Střední až vysoká | Střední |


### 5.4 Výběr správné NoSQL databáze pro Big Data scénář

Výběr konkrétní NoSQL databáze (nebo kombinace databází) pro Big Data projekt závisí na mnoha faktorech:

1.  **Charakteristiky dat (3V + další):**
    -   **Objem:** Jak velká data očekáváte nyní a v budoucnu? (Ovlivňuje potřebu škálovatelnosti).
    -   **Rychlost:** Jak rychle data přicházejí a jak rychle je potřeba je zpracovat/analyzovat? (Ovlivňuje požadavky na propustnost zápisu a latenci dotazů).
    -   **Rozmanitost:** Jsou data strukturovaná, polostrukturovaná, nebo nestrukturovaná? Jak často se bude měnit jejich struktura? (Ovlivňuje potřebu flexibility schématu).
    -   **Věrohodnost:** Jaká je kvalita dat a jaké jsou požadavky na jejich čištění a validaci?
    -   **Hodnota:** Jaké vhledy a akce chcete z dat získat? (Ovlivňuje typy analýz a dotazů).

2.  **Přístupové vzory a typy dotazů:**
    -   Budete provádět hlavně jednoduché vyhledávání podle ID, nebo komplexní analytické dotazy?
    -   Potřebujete prohledávat text, analyzovat vztahy, nebo pracovat s časovými řadami?
    -   Jaké jsou požadavky na latenci odpovědí?

3.  **Požadavky na konzistenci:**
    -   Je pro vaši aplikaci kritická silná konzistence (všechny čtecí operace vrací nejaktuálnější data), nebo je přijatelná konečná konzistence (eventual consistency)? Toto je zásadní otázka související s CAP teorémem.

4.  **Provozní aspekty:**
    -   Máte k dispozici tým pro správu komplexních distribuovaných systémů, nebo preferujete spravované cloudové služby?
    -   Jaké jsou požadavky na monitoring, zálohování a zotavení po havárii?
    -   Jaké jsou rozpočtové možnosti?

5.  **Ekosystém a integrace:**
    -   Jak dobře se databáze integruje s ostatními nástroji a frameworky, které plánujete použít (např. Apache Spark, Kafka, analytické nástroje)?
    -   Jak velká je komunita kolem dané technologie a jaká je dostupnost dokumentace a podpory?

**Příklady rozhodování:**

-   **Scénář 1: Logování událostí z distribuované aplikace a jejich téměř real-time analýza pro detekci anomálií.**
    -   *Data:* Velký objem (miliardy událostí denně), vysoká rychlost zápisu, polostrukturovaná (např. JSON logy).
    -   *Dotazy:* Filtrování podle časových oken, tagů (např. ID služby, typ chyby), agregace (počty chyb za minutu).
    -   *Možné volby:*  **Sloupcová databáze** (Cassandra, HBase) pro masivní ingesci a škálovatelnost, nebo **Time Series DB** (InfluxDB, Prometheus) pokud jsou data primárně metrikami s časovým razítkem. Elasticsearch (i když není čistě NoSQL DB, ale vyhledávací engine) je také velmi populární pro log analýzu.

-   **Scénář 2: E-commerce platforma s rozsáhlým katalogem produktů, kde každý produkt má mnoho různých a často se měnících atributů, a potřebou personalizovaných doporučení.**
    -   *Data:* Střední až velký objem produktových dat, polostrukturovaná. Data o chování uživatelů pro doporučení.
    -   *Dotazy:* Vyhledávání produktů podle různých atributů, filtrování, získání detailů produktu. Pro doporučení: analýza vztahů mezi uživateli a produkty.
    -   *Možné volby:*  **Dokumentová databáze** (MongoDB) pro flexibilní produktový katalog. **Grafová databáze** (Neo4j) pro doporučovací engine. Případně **Multimodelová databáze** (ArangoDB) může pokrýt oba aspekty. Klíč-hodnota store (Redis) pro cachování produktových dat a uživatelských relací.

-   **Scénář 3: Platforma pro monitorování výkonu tisíců IoT zařízení v reálném čase.**
    -   *Data:* Extrémně vysoká rychlost zápisu telemetrických dat (metriky jako teplota, tlak, poloha) s časovým razítkem.
    -   *Dotazy:* Zobrazení aktuálního stavu, historických trendů pro konkrétní zařízení nebo skupiny zařízení, agregace (průměry, maxima za časové okno), alerty.
    -   *Možné volby:*  **Time Series DB** (InfluxDB, TimescaleDB, Prometheus) je zde jasnou volbou.

### 5.5 Závěr

NoSQL databáze hrají klíčovou roli v moderních Big Data architekturách. Jejich schopnost škálovat, flexibilně pracovat s různými datovými modely a optimalizovat pro specifické pracovní zátěže je činí nepostradatelnými pro mnoho aplikací, které by s tradičními RDBMS nebyly realizovatelné nebo efektivní. Výběr správného typu (nebo kombinace typů) NoSQL databáze je však kritickým rozhodnutím, které musí být založeno na důkladné analýze požadavků konkrétního projektu. Často se v komplexních Big Data řešeních setkáváme s tzv. **polyglotní perzistencí**, kde se pro různé části systému a různé typy dat používají různé databázové technologie, aby se co nejlépe využily jejich specifické silné stránky.