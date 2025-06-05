## 6. Data Warehousing, Data Lakes a Datové Kostky

Při práci s velkými objemy dat pro analytické účely a reporting se setkáváme s různými architektonickými přístupy k ukládání a organizaci dat. Mezi nejvýznamnější patří datové sklady (Data Warehouses), datová jezera (Data Lakes) a v kontextu multidimenzionální analýzy také datové kostky (OLAP Cubes).

### 6.1 Data Warehouse (Datový sklad)

*   **Definice:** Datový sklad je centralizované úložiště, které integruje data z jednoho nebo více různých zdrojů. Je navržen a optimalizován primárně pro **analytické dotazy a reporting (Business Intelligence - BI)**, nikoli pro transakční zpracování (OLTP). Data v datovém skladu jsou typicky **strukturovaná, vyčištěná, transformovaná a historická**.
    
*   **Klíčové charakteristiky:**
    *   **Předmětově orientovaný (Subject-Oriented):** Data jsou organizována podle hlavních obchodních témat nebo subjektů (např. zákazník, produkt, prodej, finance), nikoli podle operačních aplikací.
    *   **Integrovaný (Integrated):** Data z různých zdrojových systémů jsou sjednocena a konzistentně uložena. Řeší se nekonzistence v názvosloví, formátech, kódech atd.
    *   **Časově variantní (Time-Variant):** Data v datovém skladu obsahují časovou dimenzi, což umožňuje analýzu trendů a změn v čase. Záznamy jsou typicky opatřeny časovým razítkem.
    *   **Nestálý (Non-Volatile):** Data v datovém skladu jsou primárně pro čtení. Po nahrání se obvykle nemění ani nemažou (s výjimkou archivace nebo oprav chyb). Nová data se přidávají, ale existující historická data zůstávají zachována.
        
*   **Architektura:**
    *   **ETL (Extract, Transform, Load) proces:** Data jsou extrahována z různých operačních systémů (databáze, CRM, ERP, ploché soubory), transformována (čištění, agregace, sjednocení formátů) a nahrána do datového skladu.
    *   **Datové tržiště (Data Marts):** Menší, specializované podmnožiny datového skladu zaměřené na konkrétní oddělení nebo obchodní oblast (např. marketingové datové tržiště, prodejní datové tržiště). Mohou být závislé (postavené nad centrálním datovým skladem) nebo nezávislé.
    *   **Schéma:** Typicky se používá **hvězdicové schéma (star schema)** nebo **schéma sněhové vločky (snowflake schema)**, které jsou optimalizovány pro analytické dotazy.
        *   **Faktové tabulky (Fact Tables):** Obsahují měřitelné údaje (fakta, metriky), např. částka prodeje, počet prodaných kusů. Mají odkazy (cizí klíče) na dimenzionální tabulky.
        *   **Dimenzionální tabulky (Dimension Tables):** Obsahují popisné atributy (dimenze), které poskytují kontext k faktům, např. čas, produkt, zákazník, geografická poloha.
            
*   **Výhody:**
    *   Poskytuje "jedinou verzi pravdy" pro analytické účely.
    *   Optimalizováno pro komplexní dotazy a reporting.
    *   Zlepšuje kvalitu a konzistenci dat.
    *   Umožňuje historickou analýzu.
        
*   **Nevýhody:**
    *   Náročné na návrh a implementaci (ETL procesy mohou být složité).
    *   Méně flexibilní vůči změnám ve zdrojových systémech nebo nových typech dat.
    *   Primárně pro strukturovaná data.
        
*   **Technologie:** Tradiční relační databáze (Oracle, SQL Server, Teradata), specializované databázové systémy pro datové sklady (Snowflake, Google BigQuery, Amazon Redshift).
    

### 6.2 Data Lake (Datové jezero)

*   **Definice:** Datové jezero je centralizované úložiště, které umožňuje ukládat **obrovské objemy surových dat v jejich nativním formátu** z různých zdrojů. Na rozdíl od datového skladu, data v jezeře nejsou předem strukturována ani transformována. Schéma se aplikuje až při čtení dat (schema-on-read).
    
*   **Klíčové charakteristiky:**
    *   **Ukládání všech typů dat:** Strukturovaná, polostrukturovaná (JSON, XML, CSV) i nestrukturovaná (text, obrázky, video, audio, logy).
    *   **Schema-on-Read:** Struktura dat je definována a aplikována až v momentě, kdy jsou data čtena a analyzována, nikoli při jejich ukládání. To poskytuje velkou flexibilitu.
    *   **Surová data:** Data jsou ukládána v původní, nezměněné podobě. To umožňuje různé typy analýz a zabraňuje ztrátě informací, která by mohla nastat při předběžné transformaci.
    *   **Škálovatelnost:** Navrženo pro ukládání petabajtů a exabajtů dat, typicky s využitím distribuovaných souborových systémů.
    *   **Různé nástroje pro analýzu:** Umožňuje použití široké škály analytických nástrojů a frameworků (SQL, Python, R, Spark, strojové učení).
        
*   **Architektura:**
    *   **Vrstva úložiště:** Typicky distribuovaný souborový systém (HDFS) nebo cloudové objektové úložiště (Amazon S3, Azure Blob Storage, Google Cloud Storage).
    *   **Vrstva zpracování a analýzy:** Nástroje jako Apache Spark, Hadoop MapReduce, Presto, Hive pro zpracování a dotazování dat.
    *   **Katalog metadat:** Systémy pro správu metadat o datech v jezeře (např. Apache Atlas, AWS Glue Data Catalog), které pomáhají s objevováním a pochopením dat.
        
*   **Výhody:**
    *   **Flexibilita:** Schopnost ukládat jakákoli data bez předchozí transformace.
    *   **Škálovatelnost:** Navrženo pro extrémní objemy dat.
    *   **Nákladová efektivita:** Často využívá levnější komoditní hardware nebo cloudové úložiště.
    *   **Podpora pro pokročilou analýzu:** Ideální pro explorativní analýzu, datovou vědu a strojové učení nad surovými daty.
    *   **Data nejsou ztracena transformací:** Všechna původní data jsou zachována.
        
*   **Nevýhody:**
    *   **Riziko "datového močálu" (Data Swamp):** Pokud data nejsou řádně spravována, katalogizována a zabezpečena, může se jezero stát nepřehledným a nepoužitelným.
    *   **Kvalita a konzistence dat:** Protože data jsou surová, mohou obsahovat chyby a nekonzistence.
    *   **Bezpečnost a správa přístupu:** Zajištění bezpečnosti a správného přístupu k různým typům dat může být náročné.
    *   **Schema-on-Read může být náročnější pro některé uživatele:** Vyžaduje pochopení struktury dat při analýze.
        

### 6.3 Data Cubes (Datové Kostky / OLAP kostky)

*   **Definice:** Datová kostka (OLAP kostka) je **multidimenzionální datová struktura** používaná v OLAP (Online Analytical Processing) systémech. Umožňuje rychlou analýzu dat z více perspektiv (dimenzí). Představte si ji jako rozšíření dvourozměrné tabulky (spreadsheetu) do více dimenzí.
    
*   **Klíčové koncepty:**
    *   **Dimenze (Dimensions):** Kategorie, podle kterých jsou data analyzována. Představují kontext pro fakta. Příklady dimenzí: Čas (rok, kvartál, měsíc), Produkt (kategorie, značka, název), Geografie (země, region, město), Zákazník (segment, věková skupina). Dimenze mohou mít hierarchickou strukturu (např. Rok -> Kvartál -> Měsíc).
    *   **Míry (Measures):** Numerické hodnoty (fakta), které jsou analyzovány. Příklady měr: Prodej (částka), Počet prodaných kusů, Zisk, Náklady.
    *   **Buňky (Cells):** Průsečíky dimenzí, které obsahují hodnoty měr. Každá buňka v kostce reprezentuje agregovanou hodnotu pro specifickou kombinaci členů dimenzí.¨

*   **Operace s OLAP kostkami:**
    *   **Slice (Řez):** Výběr podmnožiny kostky fixací jedné nebo více hodnot v jedné nebo více dimenzích (např. prodeje pro konkrétní produkt v roce 2023).
    *   **Dice (Podkostka):** Výběr podmnožiny kostky definováním rozsahů hodnot ve více dimenzích.
    *   **Drill-down (Ponoření):** Procházení z agregovanějších dat na detailnější úroveň v hierarchii dimenze (např. z ročních prodejů na kvartální, pak měsíční).
    *   **Roll-up (Konsolidace/Shrnutí):** Agregace dat na vyšší úroveň v hierarchii dimenze (opak drill-down, např. z měsíčních prodejů na roční).
    *   **Pivot (Otočení):** Změna orientace os (dimenzí) v zobrazení dat.
        
*   **Typy OLAP:**
    *   **MOLAP (Multidimensional OLAP):** Data jsou uložena v optimalizované multidimenzionální databázi. Poskytuje rychlý výkon dotazů díky předpočítaným agregacím.
    *   **ROLAP (Relational OLAP):** Data zůstávají v relační databázi (často v datovém skladu s hvězdicovým nebo vločkovým schématem). OLAP nástroj generuje SQL dotazy pro získání dat.
    *   **HOLAP (Hybrid OLAP):** Kombinuje přístupy MOLAP a ROLAP. Detailní data mohou být v RDBMS, zatímco agregace jsou v MOLAP úložišti.
        
*   **Výhody:**
    *   **Rychlá analýza a reporting:** Díky předpočítaným agregacím a optimalizované struktuře.
    *   **Intuitivní pro business uživatele:** Multidimenzionální pohled na data je často přirozenější pro analýzu.
    *   **Podpora komplexních analytických dotazů.**
        
*   **Nevýhody:**
    *   **Méně flexibilní než Data Lake:** Struktura kostky a dimenze musí být definovány předem.
    *   **Omezení na numerická data a agregace:** Primárně pro kvantitativní analýzu.
    *   **Proces vytváření a aktualizace kostky (build/refresh) může být časově náročný.**
        
*   **Technologie:** Microsoft SQL Server Analysis Services (SSAS), Oracle Essbase, IBM Cognos TM1, Apache Kylin, Druid (často se používá pro real-time OLAP).
    

### 6.4 Srovnání: Data Warehouse vs. Data Lake vs. Data Cube

| Aspekt | Data Warehouse (DWH) | Data Lake (DL) | Data Cube (OLAP) |
| :-------------------------- | :------------------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------------------------------- |
| **Primární účel** | Business Intelligence, reporting, strukturovaná analýza | Explorativní analýza, datová věda, strojové učení, ukládání všech dat | Multidimenzionální analýza, rychlé agregace, BI |
| **Typ dat** | Strukturovaná, vyčištěná, transformovaná | Surová: strukturovaná, polostrukturovaná, nestrukturovaná | Primárně numerická (míry), kategorická (dimenze) |
| **Schéma** | Schema-on-Write (předem definované) | Schema-on-Read (flexibilní, definováno při analýze) | Pevně definované dimenze a míry |
| **Zpracování dat** | ETL (Extract, Transform, Load) před uložením | ELT (Extract, Load, Transform) nebo žádná transformace před uložením | Agregace a výpočty při tvorbě/aktualizaci kostky |
| **Uživatelé** | Business analytici, manažeři | Datoví vědci, datoví inženýři, business analytici | Business analytici, manažeři |
| **Flexibilita** | Nízká | Vysoká | Střední (v rámci definovaných dimenzí) |
| **Rychlost dotazů (BI)** | Vysoká (pro optimalizované dotazy) | Může být nižší (vyžaduje zpracování surových dat) | Velmi vysoká (pro předpočítané pohledy) |
| **Náklady** | Potenciálně vysoké (návrh, ETL, specializovaný HW/SW) | Potenciálně nižší (komoditní HW, cloudové úložiště) | Závisí na technologii, může být náročné na zdroje |
| **Správa** | Náročná (ETL, správa schématu) | Náročná (governance, metadata, bezpečnost "datového močálu") | Náročná (návrh kostky, proces build/refresh) |


### 6.5 Kdy použít kterou variantu? A jak spolu souvisí?

Často se tyto koncepty nevylučují, ale doplňují v rámci moderní datové architektury (někdy označované jako **Lakehouse Architecture**, která kombinuje výhody Data Lakes a Data Warehouses):

*   **Data Lake jako základ:** Mnoho organizací začíná s Data Lake pro ukládání všech svých surových dat. Slouží jako centrální repozitář.
*   **Data Warehouse nad Data Lake:** Z vybraných (vyčištěných a transformovaných) dat v Data Lake může být postaven Data Warehouse (nebo jeho části, tzv. Data Marts) pro specifické BI a reportingové potřeby, kde je vyžadován výkon a strukturovaný přístup.
*   **Data Cubes pro specifickou analýzu:** Datové kostky mohou být vytvářeny nad daty z Data Warehouse (nebo přímo z Data Lake pomocí nástrojů jako Apache Kylin) pro poskytnutí rychlého a interaktivního multidimenzionálního pohledu pro business uživatele.

**Kdy použít:**

*   **Data Warehouse:**
    *   Potřebujete spolehlivé, konzistentní a historické reporty pro business rozhodování.
    *   Uživatelé jsou primárně business analytici a manažeři, kteří potřebují předdefinované pohledy a dashboardy.
    *   Pracujete hlavně se strukturovanými daty.
        
*   **Data Lake:**
    *   Chcete ukládat všechny typy dat (strukturovaná, polostrukturovaná, nestrukturovaná) pro budoucí, možná zatím nedefinované, analýzy.
    *   Potřebujete flexibilitu pro explorativní analýzu, datovou vědu a strojové učení nad surovými daty.
    *   Očekáváte velké objemy a vysokou rychlost příchozích dat.
        
*   **Data Cubes (OLAP):**
    *   Vaši uživatelé potřebují provádět rychlou, interaktivní, multidimenzionální analýzu (slice, dice, drill-down, roll-up).
    *   Potřebujete optimalizovat výkon pro specifické analytické dotazy a agregace.
    *   Chcete poskytnout business uživatelům snadno použitelný nástroj pro prozkoumávání dat bez nutnosti psát složité SQL dotazy.
        
Moderní datové platformy se snaží kombinovat výhody těchto přístupů. Například koncept "Lakehouse" (např. Databricks Delta Lake, Apache Hudi, Apache Iceberg) se snaží přinést ACID transakce, správu schématu a výkon datových skladů přímo nad data uložená v Data Lake.