# Analýza informačních systémů: NoSQL Databáze - Teorie

## Úvod

V dříve jsme si ukázali praktický příklad s MongoDB, což je *NoSQL* databáze.  Nyní se podíváme podrobněji na to, co NoSQL databáze vlastně jsou, jaké jsou jejich typy, výhody, nevýhody a v čem se liší od tradičních relačních databází.  Půjdeme více do hloubky a probereme i pokročilejší koncepty.

## Co je NoSQL?

NoSQL (Not Only SQL) je obecný termín pro databáze, které nepoužívají tradiční relační model (tabulky, řádky, sloupce, SQL dotazy). Místo toho NoSQL databáze používají různé datové modely, které jsou optimalizované pro specifické typy dat a použití. Termín "Not Only SQL" naznačuje, že tyto databáze mohou (ale nemusí) podporovat i některé prvky SQL – ať už jako primární dotazovací jazyk, nebo jako doplněk. NoSQL systémy vznikly jako reakce na potřeby moderních webových aplikací, které často vyžadují:

*   **Vysokou škálovatelnost:** Schopnost zvládat obrovské množství dat a uživatelů.
*   **Vysokou dostupnost:** Minimalizace výpadků a zajištění rychlé odezvy.
*   **Flexibilitu schématu:** Možnost snadno měnit strukturu dat bez složitých migrací.
    * **Schema-on-write** (Relační Databáze): Schéma (struktura tabulek, datové typy sloupců) je definováno *předem* a data musí tomuto schématu odpovídat. Jakákoli změna schématu vyžaduje migraci dat.
    *   **Schema-on-read** (NoSQL Databáze): Schéma *není* striktně vynucováno databází.  Struktura dat se ověřuje a interpretuje až při *čtení* dat aplikací. To umožňuje velkou flexibilitu.
    * **Schema-less:** Extrémní případ schema-on-read, kde databáze nemá vůbec žádné schéma.
*   **Rychlý vývoj:** Kratší vývojové cykly a agilní přístup.

+ **Příklad flexibilního schématu (dokumentová databáze):**
+ Představte si, že ukládáte informace o uživatelích. V relační databázi byste museli předem definovat tabulku se sloupci jako `id`, `jmeno`, `prijmeni`, `email`. V NoSQL dokumentové databázi můžete mít dokumenty s různou strukturou:

    ```json
    // Uživatel 1
    {
    "_id": 1,
    "jmeno": "Jan",
    "prijmeni": "Novák",
    "email": "[e-mailová adresa byla odstraněna]"
    }

    // Uživatel 2 (má navíc telefon a oblíbené barvy)
    {
    "_id": 2,
    "jmeno": "Anna",
    "prijmeni": "Veselá",
    "telefon": "123456789",
    "oblibeneBarvy": ["modrá", "zelená"]
    }
    ```
Nemusíte provádět žádné změny schématu, abyste mohli uložit uživatele s různými atributy.

## Relační vs. NoSQL databáze (Podrobnější srovnání)

| Vlastnost | Relační databáze (RDBMS) | NoSQL databáze |
| - | - | - |
| **Datový model** | Tabulky s řádky a sloupci, pevně definované schéma (schema-on-write). Vztahy mezi tabulkami jsou definovány pomocí cizích klíčů. Normalizace dat (eliminace redundance). | Různé: dokumentové, klíč-hodnota, sloupcové, grafové, ... Schéma může být flexibilní (schema-on-read) nebo i úplně chybět (schemaless). Data jsou často denormalizovaná (pro optimalizaci výkonu). |
| **Dotazovací jazyk** | SQL (Structured Query Language) - standardizovaný jazyk pro dotazování a manipulaci s daty. | Různé (závisí na typu databáze). Některé mají vlastní dotazovací jazyky (např. MongoDB Query Language), jiné používají API (např. Redis). Některé podporují i podmnožinu SQL nebo dialekty SQL (např. Cassandra Query Language - CQL). |
| **Konzistence** | Silná konzistence (ACID vlastnosti). Zaručuje, že data jsou vždy v konzistentním stavu. | Často "eventual consistency" (konečná konzistence). Data se nakonec stanou konzistentními, ale není zaručeno, že budou konzistentní v každém okamžiku. Některé NoSQL databáze nabízejí i silnou konzistenci (nastavitelnou nebo jako výchozí), ale obvykle za cenu výkonu nebo dostupnosti. |
| **Škálovatelnost** | Obvykle vertikální (přidávání výkonu na jeden server – více RAM, CPU, diskového prostoru). Horizontální škálování (distribuce dat na více serverů) je složitější a dražší, vyžaduje specializované techniky (sharding, replikace). | Obvykle horizontální (snadné přidávání dalších serverů). Navrženy pro distribuované prostředí. Sharding a replikace jsou často vestavěné a snadno konfigurovatelné. |
| **Transakce** | Podpora ACID transakcí (Atomicity, Consistency, Isolation, Durability) na úrovni více operací a tabulek. Zajišťují integritu dat i při složitých operacích. | Omezená nebo žádná podpora transakcí. Některé NoSQL databáze podporují transakce na úrovni jednoho dokumentu nebo klíče (např. MongoDB). Podpora transakcí přes více dokumentů/klíčů je vzácnější a obvykle méně výkonná než u RDBMS. |
| **Vztahy (Relationships)** | Vztahy mezi tabulkami jsou definovány pomocí cizích klíčů (foreign keys). Relační integrita je vynucována databází. | Vztahy se řeší různě (vnořené dokumenty, reference, ...). Neexistuje jednotný způsob, jak definovat vztahy. Aplikace obvykle musí sama zajistit konzistenci vztahů. Některé NoSQL databáze (např. grafové) jsou přímo navrženy pro práci se složitými vztahy a překonávají v této oblasti relační databáze. |
| **Použití** | Aplikace, kde je důležitá integrita dat a konzistence (např. bankovnictví, účetnictví, ERP systémy). OLTP (Online Transaction Processing) - aplikace s velkým množstvím transakcí. | Aplikace, kde je důležitý výkon, škálovatelnost a flexibilita (např. sociální sítě, webové aplikace, IoT, Big Data). OLAP (Online Analytical Processing) - analýza velkého množství dat, a další aplikace, kde není kritická absolutní konzistence dat v každém okamžiku, ale spíše rychlost a dostupnost. |
| **Náročnost na správu** | Vyžaduje zkušené administrátory databází (DBA). Správa schématu, optimalizace dotazů, zálohování a obnova dat jsou složitější. | Často jednodušší na správu, zejména v cloudu (managed services). Flexibilní schéma zjednodušuje vývoj a nasazení. Automatické sharding a replikace zjednodušují škálování. |
| **Náklady** | Licence na komerční RDBMS mohou být velmi drahé. Náklady na hardware (pro vertikální škálování) mohou být také vysoké. | Mnoho NoSQL databází je open source a zdarma k použití. Horizontální škálování umožňuje používat levnější hardware (commodity hardware). Cloudové služby (managed NoSQL databases) nabízejí flexibilní cenové modely (pay-as-you-go). |
| **Maturita** | Relační databáze existují desítky let, jsou velmi dobře prověřené a existuje k nim rozsáhlá dokumentace, nástroje a odborníci. | NoSQL databáze jsou relativně novější, ale rychle se vyvíjejí. Některé NoSQL technologie jsou již velmi vyspělé, jiné jsou stále ve fázi vývoje. |

## Proč NoSQL?

Kromě již zmíněných důvodů (škálovatelnost, výkon, flexibilita, specializace), existují i další:

*   **Data Variety (Různorodost dat):**  Moderní aplikace často pracují s různými typy dat (strukturovaná, polostrukturovaná, nestrukturovaná).  Většina NoSQL databází lépe zvládá ukládání a zpracování těchto různorodých dat.
*   **Data Velocity (Rychlost dat):**  Data se často generují a mění velmi rychle (např. data ze senzorů, sociálních sítí). Existují NoSQL databáze navrženy tak, aby zvládaly vysokou rychlost zápisu a čtení.
*   **Data Volume (Objem dat):**  Objem dat, se kterými aplikace pracují, neustále roste. Některé NoSQL databáze jsou navrženy tak, aby zvládaly obrovské objemy dat (petabajty a více).
*   **Cloud Computing:**  Většina NoSQL databází se dobře hodí pro cloudové prostředí, kde je důležitá elasticita (automatické škálování) a pay-as-you-go model.
*   **Agilní vývoj**: Schopnost přizpůsobovat datový model za běhu bez nutnosti migrace schématu se hodí agilnímu vývoji.

## Typy NoSQL databází

1.  **Dokumentové databáze:**

    *   **Datový model:** Data jsou uložena ve formě dokumentů, obvykle ve formátu JSON (JavaScript Object Notation) nebo BSON (Binary JSON).  Dokumenty jsou v podstatě kolekce párů klíč-hodnota, kde hodnoty mohou být skalární hodnoty (čísla, řetězce, boolean), pole, nebo vnořené dokumenty.  Každý dokument má unikátní identifikátor (obvykle nazývaný `_id`). Dokumenty jsou seskupeny do *kolekcí* (collections), které jsou analogické tabulkám v relačních databázích, ale *nemusí* mít pevně definované schéma.  Různé dokumenty ve stejné kolekci mohou mít různou strukturu.

        ```json
        // Příklad dokumentu v MongoDB
        {
          "_id": ObjectId("5f8f1d7a1d41c81d94f9b9b1"),
          "name": "John Doe",
          "age": 30,
          "address": {
            "street": "123 Main St",
            "city": "Anytown"
          },
          "hobbies": ["reading", "hiking", "coding"]
        }
        ```

    *   **Příklady:** MongoDB, Couchbase, CouchDB, Amazon DocumentDB, Azure Cosmos DB, RethinkDB.

    *   **Použití:**
        *   **Webové aplikace:** Ukládání uživatelských profilů, článků, komentářů, produktů v e-shopech, atd.
        *   **Správa obsahu (CMS):** Ukládání stránek, blogových příspěvků, multimediálního obsahu.
        *   **Mobilní aplikace:** Synchronizace dat mezi mobilními zařízeními a cloudem.
        *   **Internet of Things (IoT):** Ukládání dat ze senzorů a zařízení.
        *   **Katalogy produktů:** Flexibilní schéma umožňuje snadno přidávat nové atributy produktů.

    *   **Výhody:**
        *   **Flexibilní schéma:** Snadné přidávání a změna polí v dokumentech bez nutnosti migrace schématu.
        *   **Snadné škálování:** Horizontální škálování je obvykle dobře podporováno.
        *   **Dobrý výkon pro čtení i zápis:**  Díky denormalizaci dat a optimalizovaným dotazovacím mechanismům.
        *   **Přirozené mapování na objektově orientované programování:**  Dokumenty se snadno mapují na objekty v programovacích jazycích.

    *   **Nevýhody:**
        *   **Omezená podpora transakcí:**  Transakce jsou obvykle omezeny na úroveň jednoho dokumentu.  Transakce přes více dokumentů jsou složitější a méně výkonné (nebo vůbec nepodporované).
        *   **Složitější dotazování na vztahy mezi dokumenty:**  Vztahy se obvykle řeší vnořením dokumentů nebo referencemi (podobně jako cizí klíče, ale bez vynucování integrity).  Dotazování na tyto vztahy může být složitější než v relačních databázích (žádné JOINy).

2.  **Klíč-hodnota (Key-Value) databáze:**

    *   **Datový model:** Data jsou uložena jako páry klíč-hodnota. Klíč je unikátní řetězec a hodnota může být libovolný datový typ (řetězec, číslo, binární data, JSON, XML, ...).  Je to v podstatě distribuovaná hashovací tabulka.
    *   **Příklady:** Redis, Memcached, Amazon DynamoDB, Riak KV, LevelDB.
    *   **Použití:**
        *   **Caching:** Ukládání často používaných dat do paměti pro rychlý přístup (např. výsledky dotazů do databáze, HTML fragmenty).
        *   **Session management:** Ukládání informací o uživatelských relacích (např. přihlašovací údaje, obsah nákupního košíku).
        *   **Ukládání uživatelských profilů (jednoduchých):** TODO
        *   **Nákupní košíky:** TODO
        *   **Fronty zpráv**: TODO
    *   **Výhody:**
        *   **Extrémně rychlé čtení a zápis:**  Přístup k datům je velmi rychlý, protože se používá pouze klíč.
        *   **Jednoduché škálování:**  Snadné rozložení dat na více serverů.
        *   **Jednoduchost:**  Jednoduchý datový model a API.
    *   **Nevýhody:**
        *   **Omezené možnosti dotazování:**  Data lze získat pouze pomocí klíče.  Nelze provádět složitější dotazy (např. filtrování podle hodnoty, rozsahové dotazy).
        * **Žádné vztahy**:

3.  **Sloupcové (Column-Family) databáze:**

    *   **Datový model:** Data jsou uložena po sloupcích, ne po řádcích.  To umožňuje efektivní čtení a zápis velkého množství dat v rámci jednoho sloupce.  Data jsou seskupena do *rodin sloupců* (column families), které jsou definovány předem.  V rámci rodiny sloupců mohou být data uložena řídce (sparse data) – nemusí existovat hodnota pro každý řádek a sloupec. Každý řádek má unikátní klíč (row key).
    *   **Příklady:** Apache Cassandra, HBase, Google Bigtable, ScyllaDB.
    *   **Použití:**
        *   **Analytika:**  Agregace dat z velkého množství zdrojů.
        *   **Logování:**  Ukládání a analýza logů.
        *   **Časové řady:**  Ukládání a analýza dat, která se mění v čase (např. data ze senzorů, finanční data).
        *   **Aplikace s velkým objemem zápisů:**
    *   **Výhody:**
        *   **Vysoký výkon pro zápis:**  Zápis nových dat je velmi rychlý, protože se zapisují pouze nové hodnoty sloupců.
        *   **Škálovatelnost:**  Snadné horizontální škálování.
        *   **Vhodné pro data s mnoha atributy:**  Efektivní ukládání dat, kde každý záznam může mít velké množství atributů (ale ne všechny atributy musí být vyplněny).
    *   **Nevýhody:**
        <!-- *   **Složitější správa:**  Vyžaduje pečlivé plánování datového modelu. -->
        *   **Méně vhodné pro komplexní dotazy a transakce:**  Dotazování je obvykle omezeno na přístup k datům pomocí klíče řádku a rodiny sloupců.
        *   **Méně vhodné pro časté updaty na existujících sloupcích.**

4.  **Grafové databáze:**

    *   **Datový model:** Data jsou uložena ve formě uzlů (nodes) a hran (edges).  Uzly reprezentují entity (např. osoby, produkty, místa) a hrany reprezentují vztahy mezi nimi (např. "zná", "koupil", "navštívil").  Uzly i hrany mohou mít vlastnosti (properties).
    *   **Příklady:** Neo4j, Amazon Neptune, JanusGraph, ArangoDB, OrientDB.
    *   **Použití:**
        *   **Sociální sítě:**  Propojení uživatelů a jejich vztahů (přátelé, sledující, sdílení).
        *   **Doporučovací systémy:**  Doporučování produktů nebo obsahu na základě vztahů mezi uživateli a položkami (např. "Uživatelé, kteří si koupili tento produkt, si také koupili...").
        *   **Správa znalostí:**  Reprezentace a správa složitých vztahů mezi informacemi.
        *   **Detekce podvodů:**  Odhalování podezřelých vzorců chování v sítích transakcí nebo vztahů.
        *   **Analýza sítí:**  Analýza vztahů v různých typech sítí (např. dopravní sítě, telekomunikační sítě).
        *   **Správa oprávnění a rolí:** Reprezentace hierarchických struktur a vztahů mezi uživateli, rolemi a zdroji.

    *   **Výhody:**
        *   **Efektivní práce se složitými vztahy:**  Grafové databáze jsou optimalizovány pro dotazy, které procházejí grafem a zkoumají vztahy mezi uzly.
        *   **Rychlé dotazování na cesty mezi uzly:**  Snadné a rychlé vyhledávání cest mezi uzly (např. nalezení nejkratší cesty, nalezení všech přátel přátel).
        *   **Intuitivní datový model:**  Grafový model je často intuitivnější pro reprezentaci vztahů než relační model.

    *   **Nevýhody:**
        *   **Méně vhodné pro obecné ukládání dat:**  Grafové databáze nejsou ideální pro ukládání dat, která nemají jasné vztahy.
        *   **Složitější škálování než u jiných NoSQL databází:**  Horizontální škálování grafových databází může být náročné.
        * **Menší rozšířenost a méně dostupných nástrojů:** Oproti relačním, a některým NoSQL databázím.

5.  **Hashovací (Hash/Klíč-hodnota s rozšířenými možnostmi):**

    *   **Datový model:** Podobné Key-Value databázím, ale s rozšířenými možnostmi.  Klíč je stále unikátní řetězec, ale hodnota může být nejen jednoduchý datový typ, ale i složitější datové struktury, jako jsou:
        *   **Seznamy (Lists):** Uspořádané kolekce hodnot.
        *   **Množiny (Sets):** Neuspořádané kolekce unikátních hodnot.
        *   **Hashovací tabulky (Hashes):** Kolekce párů klíč-hodnota (v rámci jedné hodnoty).
        *   **Seřazené množiny (Sorted Sets):** Množiny, kde jsou hodnoty seřazeny podle skóre.
    *   **Příklady:** Redis, Amazon MemoryDB for Redis
    *   **Použití:**
        *   **In-memory databáze:**  Ukládání dat v operační paměti pro extrémně rychlý přístup.
        *   **Caching:**  Ukládání často používaných dat (výsledky dotazů, HTML fragmenty).
        *   **Message queues (fronty zpráv):**  Implementace front zpráv pro asynchronní komunikaci mezi aplikacemi.
        *   **Real-time analytics:**  Zpracování dat v reálném čase (např. počítání zobrazení, sledování aktivity uživatelů).
        *   **Leaderboards (žebříčky):**  Ukládání a aktualizace žebříčků v online hrách.
        * **Pub/Sub systémy:**

    *   **Výhody:**
        *   **Extrémní rychlost:**  Díky ukládání dat v paměti.
        *   **Flexibilita:**  Podpora různých datových struktur.
        *   **Široká škála použití:**

    *   **Nevýhody:**
        *   **Data se primárně drží v RAM:**  Omezení velikosti dat velikostí RAM.  (Redis nabízí i perzistenci na disk, ale primárně je to in-memory databáze.)
        *   **Omezené možnosti dotazování:**  Stále se jedná o key-value store, takže složitější dotazy nejsou možné.

6. **Objektové Databáze:**
     * **Datový Model:** Ukládá data jako objekty, podobně jako v objektově orientovaném programování. Objekt může obsahovat atributy (data) a metody (funkce). Podporují dědičnost, polymorfismus a zapouzdření.
     * **Příklady:** db4o, ObjectDB, Realm, ZODB.
     * **Použití:** Aplikace s komplexními datovými strukturami, kde je přirozené mapování na objekty v programovacím jazyce. CAD/CAM systémy, simulace.
     * **Výhody:** Přirozené mapování na objekty v kódu, snadná práce se složitými daty.
     * **Nevýhody:** Menší rozšířenost než jiné typy databází, omezená škálovatelnost.

7. **Time Series Databáze (TSDB):**
     *  **Datový Model:** Specializované databáze optimalizované pro ukládání a dotazování na časové řady dat (data, která se mění v čase). Data jsou obvykle uložena jako páry (časová značka, hodnota).
     * **Příklady:** InfluxDB, Prometheus, TimescaleDB (rozšíření PostgreSQL), OpenTSDB.
     * **Použití**: Monitorování systémů, IoT, finanční data, průmyslová data.
     * **Výhody:** Vysoký výkon pro zápis a čtení časových řad, efektivní ukládání a komprese dat, specializované funkce pro práci s časovými řadami (agregace, interpolace, downsampling).
     * **Nevýhody**: Omezené použití mimo oblast časových řad.

8. **Spatial Databáze:**
   * **Datový Model:** Specializované databáze optimalizované pro ukládání a dotazování na prostorová data (geografické souřadnice, tvary, polygony). Umožňují provádět prostorové dotazy (např. nalezení všech bodů v určité oblasti, nalezení nejbližšího bodu).
    * **Příklady:** PostGIS (rozšíření PostgreSQL), MongoDB (má podporu pro GeoJSON), Elasticsearch (s pluginem).
    * **Použití:** Geografické informační systémy (GIS), mapové aplikace, logistika.
    *  **Výhody:** Efektivní práce s prostorovými daty, podpora prostorových indexů a dotazů.
    * **Nevýhody:** Omezené použití mimo oblast prostorových dat.

9. **Multi-model Databáze:**
     * **Datový Model:** Kombinují více datových modelů (např. dokumentový, grafový, klíč-hodnota) v jedné databázi.
     * **Příklady:** ArangoDB, OrientDB, Cosmos DB, FoundationDB, FaunaDB.
     * **Použití:** Aplikace, které potřebují různé datové modely pro různé části dat.
     * **Výhody:** Flexibilita, možnost použít nejvhodnější datový model pro daný úkol.
     * **Nevýhody:** Složitější správa a učení, potenciální problémy s výkonem při kombinování různých modelů.

## CAP teorém

CAP teorém (Consistency, Availability, Partition Tolerance) je důležitý koncept v distribuovaných systémech, včetně NoSQL databází.  Říká, že distribuovaný systém může splňovat *pouze dvě* ze tří následujících vlastností:

*   **Consistency (Konzistence):**  Všechny uzly vidí stejná data ve stejný okamžik.
*   **Availability (Dostupnost):**  Každý požadavek obdrží odpověď (bez záruky, že obsahuje nejnovější data).
*   **Partition Tolerance (Odolnost vůči rozdělení sítě):**  Systém funguje i v případě, že dojde k výpadku komunikace mezi uzly.

V praxi to znamená, že si musíte vybrat, které dvě vlastnosti jsou pro vaši aplikaci nejdůležitější.  NoSQL databáze často upřednostňují dostupnost a odolnost vůči rozdělení sítě (AP) na úkor konzistence (CP). Relační databáze upřednostňují CP.
**V reálných distribuovaných systémech je *Partition Tolerance* prakticky *nutností*.** Sítě nejsou nikdy 100% spolehlivé, a proto je potřeba, aby systém fungoval i v případě výpadku komunikace mezi uzly.  Volba se tedy obvykle zužuje na:

*   **AP (Availability + Partition Tolerance):** Systém je dostupný a odolný vůči rozdělení sítě, ale nemusí být vždy konzistentní.
*   **CP (Consistency + Partition Tolerance):** Systém je konzistentní a odolný vůči rozdělení sítě, ale může být dočasně nedostupný.

## Shrnutí

  NoSQL databáze představují alternativu k relačním databázím, která je vhodná pro specifické typy aplikací a dat. Nabízejí škálovatelnost, výkon, flexibilitu a specializaci, ale často za cenu omezené konzistence a transakční podpory. Při výběru databáze je důležité zvážit požadavky vaší aplikace a vybrat takovou databázi, která jim nejlépe vyhovuje. V příští lekci se podíváme detailněji na MongoDB, což je zástupce dokumentových databází.