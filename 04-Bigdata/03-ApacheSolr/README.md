## 3. Apache Solr (Fulltextové vyhledávání)

Apache Solr je open-source, vysoce výkonná a škálovatelná platforma pro **fulltextové vyhledávání**. Je postavena na knihovně **Apache Lucene**, což je Java knihovna poskytující nízkoúrovňové funkce pro indexování a vyhledávání. Solr rozšiřuje Lucene o řadu funkcí, které z něj dělají robustní vyhledávací server připravený pro produkční nasazení.

### 3.1 Co je Apache Solr a k čemu se používá?

Solr umožňuje indexovat velké objemy textových (i jiných) dat a následně v nich rychle a efektivně vyhledávat. Nejde jen o prosté hledání přesné shody, ale Solr podporuje pokročilé techniky jako:

* **Relevance skóre:** Výsledky jsou řazeny podle toho, jak dobře odpovídají dotazu.
* **Fasetové vyhledávání (Faceting):** Umožňuje uživatelům filtrovat a procházet výsledky podle různých kategorií (faset), např. podle výrobce, ceny, barvy u produktů v e-shopu.
* **Zvýrazňování (Highlighting):** Ve výsledcích jsou zvýrazněna slova odpovídající dotazu.
* **Našeptávání (Suggestions/Autocomplete):** Pomáhá uživatelům formulovat dotazy nabídkou relevantních termínů.
* **Kontrola pravopisu (Spell Checking):** Navrhuje opravy pro překlepy v dotazech.
* **Geoprostorové vyhledávání:** Vyhledávání na základě geografické polohy.
* **Podpora různých formátů dokumentů:** Solr dokáže indexovat data z různých zdrojů a formátů (JSON, XML, CSV, PDF, Microsoft Word atd.) pomocí nástrojů jako Apache Tika.
* **Škálovatelnost a odolnost proti chybám:** Solr může běžet v distribuovaném režimu (SolrCloud) pro zvládnutí velkých indexů a vysoké zátěže.

**Typické případy použití Apache Solr:**

* **Vyhledávání na webových stránkách a portálech:** Interní vyhledávání obsahu.
* **E-commerce:** Vyhledávání produktů, filtrování, doporučování.
* **Systémy pro správu dokumentů (DMS):** Prohledávání velkého množství dokumentů.
* **Logovací a analytické platformy:** Prohledávání a analýza logů.
* **Podnikové vyhledávání (Enterprise Search):** Prohledávání dat napříč různými interními systémy.
* **Vyhledávání v databázích:** Poskytnutí fulltextového vyhledávání nad daty uloženými v relačních nebo NoSQL databázích.

### 3.2 Základní koncepty Apache Solr

Pro pochopení fungování Solru je důležité znát několik klíčových termínů:

* **Index:**
    * Srdcem Solru (a Lucene) je **invertovaný index**. Místo toho, aby se prohledávaly dokumenty jeden po druhém, invertovaný index mapuje termíny (slova) na seznam dokumentů, které tyto termíny obsahují. To umožňuje velmi rychlé vyhledávání.
    * Představte si to jako rejstřík na konci knihy: pro každé klíčové slovo máte seznam stránek, kde se vyskytuje.
    * Solr index se skládá z jednoho nebo více **segmentů**.

* **Dokument (Document):**
    * Základní jednotka informací v Solru. Dokument je sada **polí (fields)**.
    * Například dokument reprezentující produkt může mít pole jako `id`, `name`, `description`, `price`, `category`, `manufacturer`.
    * Dokumenty se přidávají do indexu během procesu **indexování**.

* **Pole (Field):**
    * Část dokumentu, která obsahuje konkrétní informaci (např. `name`, `price`).
    * Každé pole má **název** a **hodnotu**.
    * Pole mají také **typ (field type)**, který určuje, jak se data v poli ukládají a analyzují (viz níže).

* **Schéma (Schema):**
    * Definuje strukturu dokumentů a polí v Solr indexu.
    * Specifikuje názvy polí, jejich typy a jak mají být indexována a analyzována.
    * V Solru je schéma obvykle definováno v souboru `managed-schema` (dříve `schema.xml`).
    * **Typy polí (Field Types):** Definují, jak se data daného pole zpracovávají. Například:
        * `string`: Pro přesné shody řetězců (neoanalyzované).
        * `text_general` (a další textové typy): Pro fulltextové vyhledávání. Text je během indexování **analyzován** (rozdělen na slova, převeden na malá písmena, odstraněna diakritika, odstraněna stop-slova, aplikováno kmenování – stemming).
        * `int`, `float`, `long`, `double`, `date`: Pro číselné hodnoty a datumy.
        * `boolean`: Pro pravdivostní hodnoty.
    * **Analyzátory (Analyzers):** Řetězec operací, které se aplikují na textové pole během indexování a dotazování (např. tokenizace, převod na malá písmena, stemming).

* **Core (Jádro) / Collection (Kolekce):**
    * **Core:** V režimu Standalone (jeden Solr server) je **core** jeden Solr index spolu s jeho konfigurací (včetně schématu). Můžete mít více cores na jednom Solr serveru, každý s vlastním indexem a konfigurací.
    * **Collection:** V distribuovaném režimu **SolrCloud** je **collection** logický index, který může být rozdělen na více **shardů (shards)** a replikován na více **replik (replicas)** napříč clusterem Solr serverů. Collection poskytuje škálovatelnost a odolnost proti chybám.

* **Dotaz (Query):**
    * Požadavek na Solr server pro vyhledání dokumentů, které odpovídají zadaným kritériím.
    * Solr podporuje různé parsery dotazů (např. standardní Lucene parser, DisMax, eDisMax) a bohatou syntaxi pro specifikaci dotazů.

* **Handler (Request Handler):**
    * Komponenta v Solru, která zpracovává příchozí požadavky (např. dotazy, indexační příkazy).
    * Existují různé request handlery pro různé účely (např. `/select` pro vyhledávání, `/update` pro indexaci, `/admin` pro administrativní úkony).

### 3.3 Architektura Apache Solr

Solr může běžet v několika režimech:

* **Standalone Mode (Samostatný režim):**
    * Jeden Solr server spravuje jeden nebo více **cores**.
    * Vhodné pro menší aplikace nebo pro vývoj a testování.
    * Neposkytuje vysokou dostupnost ani automatickou škálovatelnost.

* **SolrCloud Mode (Distribuovaný režim):**
    * Solr běží jako cluster více serverů (uzlů).
    * Logické indexy se nazývají **collections**.
    * Každá collection je rozdělena na jeden nebo více **shardů (shards)**. Shard je část indexu. Rozdělení na shardy umožňuje horizontální škálování (data jsou distribuována).
    * Každý shard má jednoho **vůdce (leader)** a nula nebo více **replik (replicas)**. Repliky jsou kopie shardu a zajišťují odolnost proti chybám a škálovatelnost čtení.
    * Koordinaci v SolrCloud clusteru zajišťuje **Apache ZooKeeper**. ZooKeeper spravuje konfiguraci clusteru, volbu leaderů shardů a detekci selhání uzlů.
    * SolrCloud poskytuje vysokou dostupnost, automatické failover a distribuované indexování a vyhledávání.

<!-- ```
[Obrázek: Zjednodušené schéma architektury SolrCloud s ZooKeeperem, Shardy a Replikami]
``` -->

V adresáři `solr_example` je praktická ukázka instalace Solru pomocí Dockeru, indexování dat a provádění základních dotazů.
