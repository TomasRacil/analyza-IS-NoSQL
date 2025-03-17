# Zkratky a pojmy:

*   **ACID:** (Atomicity, Consistency, Isolation, Durability) – Sada vlastností databázových transakcí, které zaručují spolehlivost a integritu dat.
    *   **Atomicity (Atomicita):** Transakce se provede *buď celá, nebo vůbec*. Pokud dojde k chybě v průběhu transakce, všechny změny se vrátí zpět (rollback).
    *   **Consistency (Konzistence):** Transakce převede databázi z jednoho konzistentního stavu do jiného konzistentního stavu. Jsou dodržována všechna definovaná pravidla a omezení (constraints).
    *   **Isolation (Izolace):** Transakce probíhají izolovaně od ostatních transakcí. To znamená, že souběžně běžící transakce se navzájem neovlivňují.
    *   **Durability (Trvanlivost):** Jakmile je transakce úspěšně dokončena (committed), změny jsou trvale uloženy, a to i v případě výpadku systému.

*   **API:** (Application Programming Interface) – Rozhraní pro programování aplikací. Umožňuje různým softwarovým komponentám komunikovat mezi sebou. V kontextu databází se API používá pro přístup k datům a provádění operací (vkládání, čtení, aktualizace, mazání).

*   **Apache Spark:** Framework pro distribuované zpracování dat. Používá se pro Big Data aplikace.

*  **Apache Solr:** Open-source platforma pro fulltextové vyhledávání.

*   **Backend:** Část webové aplikace, která běží na serveru. Zodpovídá za zpracování dat, komunikaci s databází a logiku aplikace.

*   **BI:** (Business Intelligence) – Zahrnuje procesy a nástroje pro sběr, analýzu a prezentaci dat, které pomáhají firmám lépe porozumět svému podnikání a dělat lepší rozhodnutí.

*   **Big Data:** Označuje velké a komplexní soubory dat, které je obtížné zpracovávat tradičními databázovými nástroji a technikami. Big Data se vyznačuje třemi (nebo více) "V": Volume (objem), Velocity (rychlost) a Variety (rozmanitost).

*   **BSON:** (Binary JSON) – Binární reprezentace JSON dokumentů. Používá se v MongoDB pro efektivnější ukládání a zpracování dat. Je rychlejší na zpracování než textový JSON.

*   **CAD/CAM:** (Computer-Aided Design/Computer-Aided Manufacturing) – Počítačem podporované navrhování a výroba.  Software pro tvorbu technických výkresů, 3D modelů a řízení výrobních strojů.

* **CMS:** (Content Management System) – Systém pro správu obsahu. Umožňuje vytvářet, upravovat a publikovat digitální obsah (texty, obrázky, videa) na webových stránkách.

*   **CORS:** (Cross-Origin Resource Sharing) – Mechanismus, který umožňuje webovým stránkám z jedné domény (origin) přistupovat k prostředkům na jiné doméně.

*   **CouchDB:** Konkrétní typ NoSQL databáze (dokumentová).

*   **CQL:** (Cassandra Query Language) – Dotazovací jazyk pro Apache Cassandra (sloupcová NoSQL databáze). Podobný SQL.

*   **CRUD:** (Create, Read, Update, Delete) – Čtyři základní operace s daty v databázích: vytvoření, čtení, aktualizace a mazání.

*   **CSS:** (Cascading Style Sheets) – Kaskádové styly. Jazyk pro popis vzhledu webových stránek (barvy, písma, rozložení).

*   **DataFrame:** Datová struktura v Apache Sparku (a dalších systémech). Podobná tabulce v relační databázi – má sloupce a řádky. Umožňuje efektivnější zpracování dat než RDD.

*   **DBA:** (Database Administrator) – Administrátor databáze. Osoba zodpovědná za správu, údržbu a zabezpečení databáze.

*   **DNS:** (Domain Name System) – Systém doménových jmen. Překládá doménová jména (např. `www.example.com`) na IP adresy (např. `192.168.1.1`).

*   **Docker:** Platforma pro vývoj, distribuci a spouštění aplikací v kontejnerech.

*   **ERP:** (Enterprise Resource Planning) – Podnikový informační systém. Integruje různé podnikové procesy (např. finance, účetnictví, výrobu, logistiku, lidské zdroje) do jednoho systému.

*  **Frontend:** Část webové aplikace, která běží v prohlížeči uživatele (HTML, CSS, JavaScript). Zodpovídá za zobrazení a interakci s uživatelem.

*   **Git:** Distribuovaný systém pro správu verzí. Umožňuje sledovat změny v souborech, vracet se k předchozím verzím, spolupracovat s ostatními a řešit konflikty.

*   **GitHub:** Webová služba (a platforma) pro hostování Git repozitářů. Poskytuje nástroje pro spolupráci, správu verzí, sledování chyb, atd.

*   **GIS:** (Geographic Information System) – Geografický informační systém.  Systém pro sběr, správu, analýzu a vizualizaci geografických dat.

*   **HTML:** (HyperText Markup Language) – Značkovací jazyk pro tvorbu webových stránek. Definuje strukturu a obsah stránky.

*   **Host (Hostitelský počítač/Hostitelský OS):**  Fyzický nebo virtuální stroj, na kterém běží Docker Engine a kontejnery.

*   **HTTP:** (Hypertext Transfer Protocol) – Protokol pro přenos hypertextových dokumentů (webových stránek). Používá se pro komunikaci mezi webovým prohlížečem a serverem.

*   **IIFE:** (Immediately Invoked Function Expression) – Funkce v JavaScriptu, která je definována a okamžitě spuštěna. Používá se pro vytvoření lokálního scope (rozsahu platnosti proměnných) a pro zapouzdření kódu.

* **IoT:** (Internet of Things) – Internet věcí. Síť fyzických zařízení (např. senzory, spotřebiče, vozidla) propojených s internetem, která si mohou navzájem vyměňovat data.

* **JavaScript:** Programovací jazyk pro tvorbu interaktivních webových stránek.

*   **JSON:** (JavaScript Object Notation) – Textový formát pro výměnu dat. Založený na podmnožině JavaScriptu. Snadno čitelný pro lidi i stroje. Používá se v mnoha webových aplikacích a NoSQL databázích (např. MongoDB).

*   **LTS:** (Long-Term Support) – Verze softwaru, která má garantovanou dlouhodobou podporu (opravy chyb, bezpečnostní aktualizace).

*   **MapReduce:** Programovací model pro zpracování velkých objemů dat na distribuovaném clusteru. Data se rozdělí na menší části, ty se zpracují paralelně (map) a výsledky se sloučí (reduce).

*  **Middleware:** Software, který zprostředkovává komunikaci mezi různými částmi aplikace nebo mezi různými aplikacemi.

*   **MongoDB:** Konkrétní typ NoSQL databáze (dokumentová).

*   **Nginx:** Webový server a reverzní proxy server.

*   **NoSQL:** (Not Only SQL) – Obecný termín pro databáze, které nepoužívají relační model.

*   **OLAP:** (Online Analytical Processing) – Analytické zpracování dat. Typicky zahrnuje složité dotazy nad velkým objemem dat, často pro účely business intelligence (BI).

*   **OLTP:** (Online Transaction Processing) – Zpracování transakcí v reálném čase. Typicky zahrnuje velké množství krátkých transakcí (např. v bankovnictví, e-commerce).

*  **RAM:** (Random Access Memory) - Operační paměť počítače. Slouží k dočasnému ukládání dat a spuštěných programů.

*   **RDBMS:** (Relational Database Management System) – Systém pro správu relačních databází. Např. MySQL, PostgreSQL, Oracle, SQL Server.

*   **RDD:** (Resilient Distributed Dataset) – Základní datová struktura v Apache Sparku. Reprezentuje neměnnou, distribuovanou kolekci dat, kterou lze zpracovávat paralelně.

*   **REST (RESTful) API:** (Representational State Transfer) – Architektonický styl pro tvorbu webových služeb. REST API používá standardní HTTP metody (GET, POST, PUT, DELETE) pro komunikaci s daty. Data se obvykle přenášejí ve formátu JSON nebo XML.

* **SDK:** (Software Development Kit) - sada nástrojů pro vývojáře. Obvykle obsahuje knihovny, dokumentaci, příklady kódu a další nástroje, které usnadňují vývoj aplikací pro určitou platformu nebo technologii.

* **Sharding**: Technika horizontálního škálování databáze, při které se data rozdělí na menší části (shardy) a uloží na více serverech.

*   **Spark SQL:** Modul v Apache Sparku, který umožňuje dotazovat se na data pomocí SQL (nebo dialektu SQL).

*   **SQL:** (Structured Query Language) – Strukturovaný dotazovací jazyk. Standardní jazyk pro práci s relačními databázemi.

*   **TSDB:** (Time Series Database) – Databáze optimalizovaná pro ukládání a práci s časovými řadami dat (data, která se mění v čase).

* **VCS:** (Version Control System) - systém správy verzí. Umožňuje sledovat změny v souborech, vracet se k předchozím verzím, spolupracovat s ostatními a řešit konflikty. Např. Git, Subversion, Mercurial.

*   **VS Code:** (Visual Studio Code) – Populární, bezplatný a open-source editor kódu od Microsoftu. Má vestavěnou podporu pro Git.

* **URL:** (Uniform Resource Locator) Adresa zdroje na internetu (např. webové stránky, souboru).

* **XML:** (Extensible Markup Language) – Značkovací jazyk pro reprezentaci strukturovaných dat.  Používá se pro výměnu dat mezi různými systémy.

*   **YAML:** (YAML Ain't Markup Language) – Formát pro serializaci dat.  Často se používá pro konfigurační soubory (např. v Docker Compose).  Je navržen tak, aby byl snadno čitelný pro lidi.
Tento slovník by měl studentům pomoci lépe se orientovat v terminologii používané v kurzu. Doporučuji ho umístit do repozitáře, například do hlavního `README.md` nebo do samostatného souboru (např. `SLOVNIK.md`).
