## 2. Apache Spark

Apache Spark je výkonný, open-source framework pro distribuované zpracování velkých objemů dat (Big Data). Byl vyvinut na Kalifornské univerzitě v Berkeley a později darován Apache Software Foundation. Spark se stal jedním z nejpopulárnějších nástrojů pro Big Data analýzy díky své rychlosti, snadnému použití a univerzálnosti.

### 2.1 Co je Apache Spark a proč je důležitý?

Na rozdíl od tradičního MapReduce (např. v Hadoopu), který provádí většinu operací na disku, Spark se snaží co nejvíce výpočtů provádět **v operační paměti (in-memory)**. To vede k výrazně vyššímu výkonu, zejména pro iterativní algoritmy (jako jsou ty používané ve strojovém učení) a interaktivní analýzu dat.

**Klíčové vlastnosti a výhody Apache Sparku:**

* **Rychlost:** Díky in-memory zpracování a optimalizovanému prováděcímu enginu (DAG scheduler) může být Spark až 100x rychlejší než Hadoop MapReduce pro určité úlohy.
* **Univerzálnost:** Spark není omezen pouze na MapReduce paradigma. Poskytuje bohaté API a podporuje různé typy úloh:
    * **Dávkové zpracování (Batch Processing):** Zpracování velkých, statických datasetů.
    * **Streamování dat (Stream Processing):** Zpracování dat v reálném čase nebo téměř v reálném čase (pomocí Spark Streaming nebo novějšího Structured Streaming).
    * **Strojové učení (Machine Learning):** Knihovna MLlib poskytuje širokou škálu algoritmů pro klasifikaci, regresi, clustering, doporučování atd.
    * **Zpracování grafů (Graph Processing):** Knihovna GraphX (a novější GraphFrames) umožňuje analyzovat grafové struktury.
    * **SQL dotazy:** Spark SQL umožňuje spouštět SQL dotazy nad strukturovanými daty a integrovat se s různými datovými zdroji.
* **Snadné použití:** Spark nabízí API v populárních programovacích jazycích jako **Scala** (primární jazyk Sparku), **Java**, **Python** (PySpark) a **R**. Python API (PySpark) je obzvláště populární díky své jednoduchosti a širokému ekosystému datově-vědných knihoven.
* **Odolnost proti chybám (Fault Tolerance):** Spark je navržen pro běh na distribuovaných clusterech a dokáže se automaticky zotavit ze selhání jednotlivých uzlů.
* **Integrace:** Snadno se integruje s různými systémy pro ukládání dat (HDFS, Amazon S3, Apache Cassandra, HBase, Hive, relační databáze přes JDBC) a správci clusterů (Standalone, Apache Mesos, Hadoop YARN, Kubernetes).
* **Aktivní komunita:** Spark má velkou a aktivní komunitu vývojářů a uživatelů, což zajišťuje neustálý vývoj, podporu a množství dostupných zdrojů.

**Kdy použít Apache Spark?**

Spark je vhodný pro širokou škálu scénářů, kde je potřeba zpracovávat velké objemy dat, například:

* Analýza logů a clickstream dat.
* Doporučovací systémy.
* Detekce podvodů.
* Zpracování genomických dat.
* Analýza sentimentu.
* ETL (Extract, Transform, Load) procesy pro datové sklady a data lakes.
* Interaktivní datová analýza a explorace.

### 2.2 Základní architektura Apache Sparku

Spark aplikace běží jako sada nezávislých procesů na clusteru, koordinovaných hlavním programem nazývaným **Driver Program**.

* **Driver Program (Řídící program):**
    * Je to proces, ve kterém běží `main()` funkce vaší Spark aplikace.
    * Je zodpovědný za vytvoření **SparkContextu** (nebo **SparkSession** v novějších verzích), což je hlavní vstupní bod pro Spark funkcionalitu.
    * Analyzuje uživatelský kód, transformuje ho na logický a fyzický plán provádění (DAG – Directed Acyclic Graph úloh).
    * Komunikuje s **Cluster Managerem** pro získání zdrojů na clusteru.
    * Distribuuje úlohy (tasks) na **Executory**.
    * Sleduje průběh provádění úloh a shromažďuje výsledky.

* **Cluster Manager (Správce clusteru):**
    * Zodpovídá za přidělování výpočetních zdrojů (CPU, paměť) na clusteru Spark aplikacím.
    * Spark podporuje několik typů cluster managerů:
        * **Standalone Cluster Manager:** Jednoduchý správce clusteru dodávaný se Sparkem.
        * **Apache Hadoop YARN (Yet Another Resource Negotiator):** Běžně používaný v Hadoop ekosystému.
        * **Apache Mesos:** Univerzální správce clusteru.
        * **Kubernetes:** Populární platforma pro orchestraci kontejnerů, kterou Spark také podporuje.

* **Executor (Vykonavatel):**
    * Jsou to pracovní procesy běžící na jednotlivých uzlech (worker nodes) clusteru.
    * Jsou spouštěny na začátku Spark aplikace a běží po celou dobu jejího života.
    * Jsou zodpovědné za **provádění úloh (tasks)**, které jim přidělí Driver Program.
    * Ukládají data (RDD/DataFrame partitions) v paměti nebo na disku.
    * Vrací výsledky zpracování zpět Driver Programu.

**Schéma komunikace:**

1.  Uživatel spustí Spark aplikaci (Driver Program).
2.  Driver Program požádá Cluster Managera o zdroje (Executory).
3.  Cluster Manager alokuje zdroje a spustí Executory na worker nodech.
4.  Executory se zaregistrují u Driver Programu.
5.  Driver Program transformuje kód na úlohy a posílá je Executorům.
6.  Executory provádějí úlohy na datech (která mohou být načtena z distribuovaného úložiště jako HDFS nebo cachována v paměti Executorů).
7.  Výsledky jsou posílány zpět Driver Programu nebo ukládány do externího úložiště.


![Obrázek: Zjednodušené schéma architektury Apache Sparku s Driverem, Cluster Managerem a Executory](https://miro.medium.com/v2/resize:fit:828/format:webp/1*oP13RtCYqYJS74NoqonTpA.png)


Tato architektura umožňuje Sparku efektivně škálovat a paralelně zpracovávat data napříč velkými clustery.
