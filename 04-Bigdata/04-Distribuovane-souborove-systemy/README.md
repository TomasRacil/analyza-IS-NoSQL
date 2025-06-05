## 4. Distribuované souborové systémy (např. HDFS)

S rostoucími objemy dat (Big Data) se tradiční souborové systémy, navržené pro jeden server, stávají nedostatečnými. Distribuované souborové systémy (DFS) nabízejí řešení pro ukládání a správu obrovských datových sad napříč clustery serverů.

### 4.1 Proč Distribuované souborové systémy?

Tradiční souborové systémy (např. NTFS, ext4, HFS+) jsou navrženy pro běh na jednom stroji. Při práci s Big Data narážejí na několik zásadních omezení:

* **Kapacita úložiště:** Jeden server má omezenou diskovou kapacitu. Ukládání petabajtů dat na jediný systém je nepraktické a drahé.
* **Propustnost I/O (Input/Output):** Rychlost čtení a zápisu dat je limitována výkonem disků a řadičů jednoho serveru. Při zpracování velkých datasetů se I/O stává úzkým hrdlem.
* **Jediný bod selhání (Single Point of Failure - SPOF):** Pokud server selže, všechna data na něm uložená se stanou nedostupnými.
* **Škálovatelnost:** Vertikální škálování (přidávání disků a výkonu jednomu serveru) je nákladné a má své limity.

Distribuované souborové systémy řeší tyto problémy tím, že:

* **Distribuují data:** Soubory jsou rozděleny na menší části (bloky) a uloženy napříč mnoha servery (uzly) v clusteru.
* **Poskytují paralelní přístup:** Aplikace mohou číst a zapisovat data paralelně z/na více uzlů, čímž se zvyšuje celková propustnost.
* **Zajišťují odolnost proti chybám:** Bloky dat jsou typicky replikovány na více serverů, takže selhání jednoho uzlu nevede ke ztrátě dat.
* **Umožňují horizontální škálování:** Kapacitu a výkon lze zvyšovat přidáváním dalších serverů do clusteru, což je často nákladově efektivnější.

### 4.2 HDFS (Hadoop Distributed File System)

HDFS je jedním z nejznámějších a nejrozšířenějších distribuovaných souborových systémů. Je klíčovou komponentou ekosystému Apache Hadoop a je navržen pro ukládání velmi velkých souborů (gigabajty až terabajty) na clusterech z komoditního hardwaru.

#### 4.2.1 Úvod a cíle HDFS

Hlavní cíle a charakteristiky HDFS:

* **Ukládání velmi velkých souborů:** Optimalizováno pro soubory o velikosti stovek megabajtů, gigabajtů nebo i terabajtů.
* **Streaming Data Access:** Navrženo pro aplikace, které čtou data sekvenčně a ve velkých blocích (např. MapReduce úlohy). Není optimalizováno pro náhodný přístup k malým částem souborů s nízkou latencí.
* **Běh na komoditním hardwaru:** HDFS je navrženo tak, aby běželo na běžně dostupném, relativně levném hardwaru. Odolnost proti chybám je zajištěna softwarově (replikací), nikoli spoléháním na drahý, vysoce spolehlivý hardware.
* **Odolnost proti chybám (Fault Tolerance):** Automatická detekce selhání a replikace dat zajišťují, že data zůstanou dostupná i při výpadku některých uzlů.
* **Vysoká propustnost (High Throughput):** Poskytuje vysokou agregovanou propustnost pro čtení a zápis dat díky paralelnímu přístupu.
* **Jednoduchý model koherencest:** HDFS používá model "write-once-read-many" (zapiš jednou, čti mnohokrát). Soubory jsou po zapsání typicky neměnné (i když novější verze umožňují append).

#### 4.2.2 Architektura HDFS

HDFS má architekturu master/slave (nebo spíše leader/follower).

* **NameNode (Jmenný uzel):**
    * Je to **master** server v HDFS clusteru.
    * **Spravuje metadata** souborového systému:
        * Adresářovou strukturu (názvy souborů a adresářů, hierarchii).
        * Mapování souborů na datové bloky (které bloky tvoří který soubor).
        * Umístění replik jednotlivých bloků na DataNodech.
        * Přístupová práva k souborům a adresářům.
    * Všechna metadata drží **v operační paměti** pro rychlý přístup. Změny metadat se také logují do transakčního logu (EditLog) a periodicky se ukládá obraz metadat (FsImage) na disk.
    * **Nezpracovává samotná data souborů.** Klienti komunikují s NameNodem pouze pro získání metadat a poté přistupují k datům přímo na DataNodech.
    * Tradičně byl NameNode **jediným bodem selhání (SPOF)**. Pokud NameNode selhal, celý HDFS cluster se stal nedostupným. Moderní verze Hadoopu podporují **HDFS High Availability (HA)** s aktivním a pasivním NameNodem (a ZooKeeperem pro koordinaci) pro eliminaci tohoto problému.

* **DataNode (Datový uzel):**
    * Jsou to **slave/worker** servery v HDFS clusteru.
    * **Ukládají skutečná data souborů** ve formě **datových bloků (blocks)**.
    * Na jednom clusteru běží typicky mnoho DataNodů (desítky, stovky, tisíce).
    * Pravidelně posílají **heartbeat signály** NameNodu, aby informovaly o svém stavu a o blocích, které spravují (block reports).
    * Provádějí operace vytváření, mazání a replikace bloků na základě instrukcí od NameNodu.
    * Obsluhují požadavky na čtení a zápis dat od klientů.

* **Bloky (Blocks):**
    * Soubory v HDFS jsou rozděleny na bloky pevné velikosti.
    * Výchozí velikost bloku je typicky **128 MB** nebo **256 MB** (v Hadoopu 2.x a novějších). Tato velikost je mnohem větší než u tradičních souborových systémů (např. 4 KB).
    * **Důvody pro velké bloky:** Minimalizace režie metadat (méně bloků na soubor znamená méně metadat pro NameNode) a optimalizace pro sekvenční čtení (efektivnější přenos velkých kusů dat).
    * Každý blok je **replikován** na více DataNodů pro zajištění odolnosti proti chybám. Výchozí replikační faktor je **3** (každý blok má 3 kopie na různých DataNodech).

* **Rack Awareness (Povědomí o racku):**
    * HDFS se snaží umisťovat repliky bloků na různé racky (skříně se servery v datovém centru).
    * Cílem je zajistit, že data zůstanou dostupná i v případě selhání celého racku (např. kvůli výpadku napájení nebo síťového switche).
    * Typická strategie umístění replik (při replikačním faktoru 3):
        1.  První replika na DataNodu, kde probíhá zápis (pokud je to DataNode).
        2.  Druhá replika na jiném DataNodu ve stejném racku.
        3.  Třetí replika na DataNodu v jiném racku.

![Obrázek: Zjednodušené schéma architektury HDFS s NameNodem, DataNody a klientem](https://www.databricks.com/sites/default/files/inline-images/hdfs-architecture.png?v=1722875303)

#### 4.2.3 Zápis souboru do HDFS

1.  **Klient** kontaktuje **NameNode** s požadavkem na vytvoření/zápis souboru a jeho cestou.
2.  **NameNode** zkontroluje přístupová práva a zda soubor již neexistuje (nebo zda je povoleno přepsání).
3.  Pokud je vše v pořádku, **NameNode** vytvoří záznam o novém souboru ve své metadata struktuře a vrátí klientovi seznam **DataNodů**, na které má klient zapsat první blok dat (typicky 3 DataNody pro replikaci). NameNode také určí, který z těchto DataNodů bude primární pro daný blok.
4.  **Klient** začne zapisovat data prvního bloku **přímo na první (primární) DataNode** ze seznamu.
5.  Tento **první DataNode** ukládá data a zároveň je **přeposílá (pipelining)** na **druhý DataNode** v seznamu.
6.  **Druhý DataNode** ukládá data a přeposílá je na **třetí DataNode**.
7.  Jakmile je blok zapsán na všech replikách, DataNody posílají potvrzení zpět v řetězci (třetí -> druhý -> první). První DataNode pak pošle potvrzení klientovi.
8.  Klient informuje NameNode o úspěšném zápisu bloku.
9.  Pro další bloky souboru se kroky 3-8 opakují. NameNode poskytne seznam DataNodů pro každý nový blok.
10. Po zapsání všech bloků klient zavolá `complete()` na NameNodu, čímž se soubor uzavře.

#### 4.2.4 Čtení souboru z HDFS

1.  **Klient** kontaktuje **NameNode** s požadavkem na čtení souboru a jeho cestou.
2.  **NameNode** vrátí klientovi seznam bloků, které tvoří daný soubor, a pro každý blok seznam **DataNodů**, na kterých se nacházejí jeho repliky. NameNode se snaží vrátit DataNody, které jsou klientovi "nejblíže" (např. ve stejném racku).
3.  **Klient** kontaktuje **přímo nejbližší DataNode** pro první blok a začne číst data.
4.  Pokud DataNode selže nebo je pomalý, klient se pokusí číst blok z jiného DataNodu, který má repliku daného bloku.
5.  Pro další bloky se kroky 3-4 opakují, dokud není přečten celý soubor.

#### 4.2.5 Replikace a odolnost proti chybám

* **Replikace:** Jak bylo zmíněno, každý blok je replikován (standardně 3x). NameNode udržuje přehled o umístění všech replik.
* **Heartbeat signály:** DataNody pravidelně (každé 3 sekundy) posílají NameNodu heartbeat signály. Pokud NameNode neobdrží heartbeat od DataNodu po určitou dobu (standardně 10 minut), považuje tento DataNode za mrtvý.
* **Re-replikace:** Pokud NameNode zjistí, že některý blok má méně replik, než je požadovaný replikační faktor (např. kvůli selhání DataNodu), naplánuje vytvoření nových replik tohoto bloku na jiných dostupných DataNodech.
* **Block reports:** DataNody periodicky (standardně každých 6 hodin) posílají NameNodu kompletní seznam bloků, které spravují. To umožňuje NameNodu ověřit konzistenci metadat.
* **Checksumy:** Pro každý blok dat se počítá checksum. Při čtení dat klient ověřuje checksum, aby detekoval případné poškození dat během přenosu nebo uložení. Pokud je detekováno poškození, klient se pokusí číst blok z jiné repliky.

#### 4.2.6 Výhody HDFS

* **Obrovská škálovatelnost:** Může ukládat petabajty dat na tisících serverů.
* **Vysoká propustnost pro sekvenční čtení:** Ideální pro dávkové zpracování.
* **Odolnost proti chybám:** Replikace zajišťuje dostupnost dat i při selhání hardwaru.
* **Nákladová efektivita:** Běží na komoditním hardwaru.
* **Flexibilita:** Může ukládat různé typy dat (strukturovaná, polostrukturovaná, nestrukturovaná).
* **Součást ekosystému Hadoop:** Dobře se integruje s nástroji jako MapReduce, Spark, Hive, Pig atd.

#### 4.2.7 Nevýhody a omezení HDFS

* **Vysoká latence pro náhodný přístup:** Není vhodný pro aplikace vyžadující rychlý přístup k malým částem souborů s nízkou latencí (např. OLTP databáze).
* **Problém s malými soubory (Small Files Problem):** Ukládání velkého množství malých souborů (menších než velikost bloku HDFS) je neefektivní, protože každý soubor (i velmi malý) zabírá metadata v NameNodu a může vést k zahlcení NameNodu.
* **Single NameNode Bottleneck (historicky):** I když HA řešení existují, NameNode stále představuje centralizovaný bod pro správu metadat.
* **Write-Once-Read-Many (WORM) model:** Tradičně byly soubory po zapsání neměnné. Novější verze podporují `append` (přidávání na konec souboru), ale plnohodnotné úpravy souborů na místě (in-place modifications) nejsou efektivní.
* **Není POSIX kompatibilní:** HDFS nemá plnou POSIX kompatibilitu, což znamená, že některé standardní operace souborového systému se mohou chovat jinak nebo nejsou podporovány.

### 4.3 Další Distribuované Souborové Systémy (přehled)

Kromě HDFS existuje řada dalších distribuovaných souborových systémů a objektových úložišť, které se používají v kontextu Big Data:

* **Cloudová Objektová Úložiště:**
    * **Amazon S3 (Simple Storage Service):** Velmi populární, vysoce škálovatelné a odolné objektové úložiště od AWS. Není to tradiční souborový systém (nemá hierarchickou adresářovou strukturu ve stejném smyslu), ale objekty (soubory) jsou uloženy v "bucketech" a adresovány pomocí klíčů. Často se používá jako zdroj dat nebo cíl pro Spark a další Big Data nástroje.
    * **Azure Blob Storage:** Obdoba S3 od Microsoft Azure.
    * **Google Cloud Storage (GCS):** Obdoba S3 od Google Cloud Platform.
    * **Výhody cloudových úložišť:** Vysoká dostupnost, odolnost, škálovatelnost, pay-as-you-go model, integrace s dalšími cloudovými službami.
    * **Rozdíly oproti HDFS:** Typicky "eventual consistency" model (změny se nemusí projevit okamžitě všem klientům), optimalizováno pro ukládání objektů, nikoli pro POSIX-like souborové operace.

* **GlusterFS:**
    * Open-source, škálovatelný síťový souborový systém.
    * Může běžet na komoditním hardwaru.
    * Poskytuje různé typy volumed (distribuované, replikované, stripované).
    * Vhodný pro ukládání velkých souborů, virtuálních strojů, záloh.

* **CephFS:**
    * Open-source, distribuovaný souborový systém, který je součástí širší platformy Ceph (která poskytuje i blokové a objektové úložiště).
    * Navržen pro vysokou škálovatelnost, výkon a odolnost.
    * POSIX kompatibilní.

### 4.4 Kdy použít Distribuovaný Souborový Systém?

* **Velké objemy dat:** Když data přesahují kapacitu jednoho serveru.
* **Požadavky na vysokou propustnost:** Pro aplikace, které potřebují rychle číst a zapisovat velké množství dat.
* **Odolnost proti chybám:** Když je kritická dostupnost dat i při selhání hardwaru.
* **Dávkové zpracování:** Pro frameworky jako Hadoop MapReduce nebo Apache Spark, které jsou navrženy pro práci s daty uloženými v DFS.
* **Centralizované úložiště pro analytiku (Data Lake):** DFS často tvoří základ datových jezer, kde se ukládají surová data z různých zdrojů pro pozdější analýzu.
<!-- 
### 4.5 Praktická ukázka (Konceptuální)

Nastavení plnohodnotného HDFS clusteru (i pomocí Dockeru) je poměrně komplexní a přesahuje rámec jednoduché ukázky v tomto úvodním textu. Typicky by to zahrnovalo konfiguraci více kontejnerů pro NameNode, DataNody a případně JournalNody a ZooKeeper pro HA.

Pro interakci s HDFS se obvykle používá příkazová řádka Hadoopu:

* **Výpis obsahu adresáře:**
    ```bash
    hdfs dfs -ls /user/data
    ```
* **Vytvoření adresáře:**
    ```bash
    hdfs dfs -mkdir /user/new_data
    ```
* **Nahrání souboru z lokálního systému do HDFS:**
    ```bash
    hdfs dfs -put local_file.txt /user/data/hdfs_file.txt
    ```
* **Stažení souboru z HDFS do lokálního systému:**
    ```bash
    hdfs dfs -get /user/data/hdfs_file.txt local_copy.txt
    ```
* **Zobrazení obsahu souboru v HDFS:**
    ```bash
    hdfs dfs -cat /user/data/hdfs_file.txt
    ```

Tyto příkazy by se spouštěly na stroji, který má nakonfigurovaný přístup k HDFS clusteru. Big Data frameworky jako Spark pak přistupují k HDFS transparentně pomocí URI jako `hdfs://namenode_host:port/user/data/file.txt`. -->
