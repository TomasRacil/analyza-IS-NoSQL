
# Analýza informačních systémů: Ukládání rozsáhlých kolekcí dat (Big Data)

## Úvod do problematiky Big Data

Předchozí bloky kurzu se zaměřily na databáze a technologie vhodné pro běžné aplikace a středně velké objemy dat. V dnešním světě však exponenciálně roste množství dat generovaných a sbíraných z nejrůznějších zdrojů: webové logy, sociální sítě, IoT zařízení, vědecké experimenty, finanční transakce a mnoho dalších. Tato data, často označovaná jako *Big Data*, představují *nové výzvy* a *příležitosti*.

**Co jsou Big Data?**

Big Data se obvykle definuje pomocí "tří V" (někdy se uvádí i více):

*   **Volume (Objem):** Obrovské množství dat (terabajty, petabajty, exabajty).
*   **Velocity (Rychlost):** Vysoká rychlost, jakou jsou data generována a zpracovávána (často v reálném čase).
*   **Variety (Rozmanitost):** Různé typy dat (strukturovaná, polostrukturovaná, nestrukturovaná).

Kromě těchto tří V se někdy přidávají i:

*   **Veracity (Věrohodnost):** Kvalita a spolehlivost dat.
*   **Value (Hodnota):** Schopnost získat z dat užitečné informace a znalosti.
* **Variability**: Proměnlivost dat a jejich významu v kontextu.

Tradiční databázové systémy a nástroje nejsou navrženy pro efektivní zpracování Big Data. Proto vznikly *specializované technologie a frameworky*, které umožňují ukládat, zpracovávat a analyzovat obrovské objemy různorodých dat.

## Klíčové oblasti a technologie

Tento blok kurzu se zaměří na následující klíčové oblasti a technologie pro práci s Big Data:

1.  **Úvod do problematiky Big Data:**

    Tato úvodní lekce poskytuje hlubší vhled do problematiky Big Data. Definuje klíčové pojmy, charakteristiky a výzvy. Vysvětluje, proč jsou tradiční technologie nedostatečné a představuje základní principy distribuovaného zpracování dat pro Big Data.

2.  **Apache Spark:**

    Apache Spark je *rychlý*, *univerzální* a *škálovatelný* framework pro distribuované zpracování dat. Stal se *de facto standardem* pro zpracování Big Data. Spark nabízí intuitivní API pro různé programovací jazyky (Scala, Java, Python, R) a podporuje širokou škálu úloh, od dávkového zpracování po streamování, strojové učení a grafové algoritmy.

    *   **Základy Sparku:** Lekce představuje základní koncepty Sparku, jako jsou RDD (Resilient Distributed Datasets), DataFrame a Dataset. Vysvětluje architekturu Sparku (driver, executory, cluster manager) a principy fungování.
    *   **RDD (Resilient Distributed Datasets):** Podrobný pohled na RDD, základní datovou abstrakci Sparku. Lekce vysvětluje, jak RDD fungují, jaké operace s nimi lze provádět (transformace a akce) a jak Spark optimalizuje provádění těchto operací.
    *   **DataFrame a Spark SQL:** Lekce se zaměřuje na DataFrame, strukturovanější datovou abstrakci nad RDD, která umožňuje pracovat s daty podobně jako s tabulkami v relačních databázích. Spark SQL umožňuje provádět SQL dotazy nad DataFrame.
    *  **Spark Streaming** Práce s reálným tokem dat.
    * **MLib**: Knihovna pro strojové učení, která je součástí Sparku.
    * **GraphX**: Knihovna pro práci s grafy.

3.  **Apache Solr (fulltextové vyhledávání):**

    Apache Solr je *výkonný* a *škálovatelný* open-source *fulltextový vyhledávač*. Je postaven na knihovně Apache Lucene a umožňuje rychlé a efektivní vyhledávání v *obrovských kolekcích textových dokumentů*. Solr je vhodný pro aplikace, jako jsou webové vyhledávače, e-commerce platformy, systémy pro správu obsahu (CMS) a další.

    *   **Základy Solr:** Lekce představuje základní koncepty Solr (index, dokument, pole, schéma). Vysvětluje architekturu Solr a principy fungování.
    *   **Indexování dat:** Lekce se zaměřuje na proces indexování dat v Solr. Ukazuje, jak definovat schéma indexu, jak importovat data z různých zdrojů (databáze, soubory, webové stránky) a jak konfigurovat analyzátory a filtry pro zpracování textu.
    *   **Dotazování:** Lekce se věnuje dotazování v Solr. Ukazuje, jak používat různé typy dotazů (boolean, range, fuzzy, proximity), jak řadit výsledky, jak používat faceting (filtrování podle kategorií) a jak provádět pokročilé operace, jako je zvýrazňování (highlighting) a suggestions (našeptávání).
    * **Pokročilé funkce Solr** Replikace, Sharding, Clustering.

4. **Distribuované souborové systémy (např. HDFS):**
    * **Proč Distribuované souborové systémy?** Běžné souborové systémy nejsou vhodné pro ukládání obřích souborů.
    * **HDFS (Hadoop Distributed File System):** Detailní prozkoumání jednoho z nejpoužívánějších DFS. Architektura, principy fungování, replikace, správa.
    * **Další DFS (přehled):** Cloudové varianty jako S3, Azure Blob Storage.

5. **NoSQL databáze pro Big Data (přehled a srovnání):**
    * Připomenutí typů NoSQL databází, které se hodí pro velké objemy dat.
    * Detailnější rozbor použití jednotlivých typů, a srovnání. (Cassandra, HBase, MongoDB, atd.)

6. **Data Warehousing a Data Lakes:**

    * **Data Warehouse (Datový sklad):** Centralizované úložiště strukturovaných dat, optimalizované pro analytické dotazy a reporting.
    * **Data Lake (Datové jezero):** Centralizované úložiště *surových* dat v *různých formátech* (strukturovaná, polostrukturovaná, nestrukturovaná). Data Lake umožňuje ukládat data *bez nutnosti předem definovat schéma*.
    *  **Rozdíly a použití:** Srovnání Data Warehouse a Data Lake. Kdy použít kterou variantu.

7. **Stream Processing (Zpracování dat v reálném čase):**

    *   **Proč stream processing?** Mnoho aplikací vyžaduje zpracování dat *v reálném čase* (např. detekce podvodů, monitorování systémů, personalizovaná doporučení).
    *   **Základní koncepty:**  Pojmy jako stream, windowing, state management.
    * **Frameworky pro stream processing (přehled):**  Apache Kafka Streams, Apache Flink, Apache Samza, Spark Streaming (i když je to spíše micro-batching).

## Propojení s předchozími bloky

Tento blok navazuje na předchozí znalosti o databázích (zejména NoSQL) a systémech pro komunikaci a distribuované zpracování. Technologie pro Big Data často využívají koncepty jako MapReduce, replikace, sharding a distribuované zpracování, které byly představeny v předchozích blocích. Znalost REST API a JSON je užitečná pro interakci s mnoha Big Data nástroji.

## Cíl bloku

Cílem tohoto bloku je poskytnout *ucelený přehled* o technologiích a konceptech pro práci s Big Data. Naučíme se, jak ukládat, zpracovávat a analyzovat obrovské objemy dat a jak z těchto dat získávat užitečné informace. Budeme se věnovat jak teoretickým základům, tak praktickým příkladům použití jednotlivých nástrojů. Po absolvování tohoto bloku budete mít solidní základ pro budování Big Data řešení.
