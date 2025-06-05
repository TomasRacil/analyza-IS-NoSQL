## Praktický příklad: Apache Solr - Základy vyhledávání

Tento příklad vás provede základním nastavením Apache Solr pomocí Dockeru, vytvořením "core" (jádra/indexu), definicí jednoduchého schématu, indexací ukázkových dat a provedením základních vyhledávacích dotazů včetně fasetování.

### 1. Cíle příkladu

* Spustit instanci Apache Solr pomocí Docker Compose.
* Porozumět konceptu Solr "core".
* Vytvořit a nakonfigurovat základní schéma pro indexovaná data.
* Naindexovat ukázkové dokumenty (např. ve formátu JSON).
* Provádět fulltextové vyhledávací dotazy.
* Vyzkoušet si fasetování pro filtrování výsledků.

### 2. Struktura adresáře (pro Solr příklad)

Pro tento příklad budeme potřebovat následující strukturu:

```
solr_example/
├── docker-compose.yml
├── solr_home/
│   └── mycore/            # Adresář pro naše Solr jádro ("mycore")
│       └── conf/
│           ├── managed-schema   # Definice schématu (místo schema.xml)
│           └── solrconfig.xml   # Základní konfigurace jádra
└── sample_data.json       # Ukázková data pro indexaci
```

### 3. Soubory pro Solr příklad

#### a) `solr_example/docker-compose.yml`

Tento soubor definuje službu Solr.

*Poznámka k `volumes`*: Mapování `./solr_home:/var/solr/data` způsobí, že konfigurace **a také data indexu** pro jádro `mycore` budou uložena ve vašem lokálním adresáři `./solr_home/mycore/data`. To je pro jednoduchost dema. V produkci by se data indexu typicky ukládala do dedikovaného Docker volume nebo jiného perzistentního úložiště.

#### b) `solr_example/solr_home/mycore/conf/solrconfig.xml`

Toto je základní konfigurační soubor pro Solr core. Pro náš jednoduchý příklad můžeme použít minimalistickou verzi nebo zkopírovat výchozí z nově vytvořeného jádra (viz postup níže). Pro začátek ho můžeme nechat prázdný nebo jen s minimálním obsahem, Solr si ho doplní.

Pro jednoduchost začneme s téměř prázdným souborem, který Solr naplní výchozími hodnotami, nebo si vezmeme základní z dokumentace.

*Důležité:* `luceneMatchVersion` by měla odpovídat verzi Lucene použité ve vaší verzi Solru. Pro Solr 9.5 je to typicky Lucene 9.5.

#### c) `solr_example/solr_home/mycore/conf/managed-schema`

Toto je nejdůležitější konfigurační soubor, který definuje strukturu našich dat. Používá se formát XML (i když se jmenuje `managed-schema`, interně je to XML).


**Vysvětlení souboru `managed-schema`:**
* `<field name="id" type="string" ... />`: Definuje unikátní ID dokumentu.
* `<fieldType name="text_general" ...>`: Definuje typ pole pro fulltextové vyhledávání.
    * `analyzer type="index"`: Jak se text zpracuje při indexaci.
    * `analyzer type="query"`: Jak se text zpracuje při dotazování.
    * `tokenizer class="solr.StandardTokenizerFactory"`: Rozdělí text na slova (tokeny).
    * `filter class="solr.LowerCaseFilterFactory"`: Převede text na malá písmena.
    * Ostatní filtry (StopFilter, SynonymGraphFilter) jsou pro pokročilejší zpracování.
* `title`, `description`, `category`, `author`, `year`: Naše konkrétní pole.
    * `indexed="true"`: Pole bude indexováno pro vyhledávání.
    * `stored="true"`: Hodnota pole bude uložena a může být vrácena ve výsledcích.
    * `multiValued="false"` (nebo `true`): Určuje, zda pole může mít více hodnot.
    * `docValues="true"`: Optimalizuje pole pro řazení, fasetování a groupování.
* `<copyField source="title" dest="text"/>`: Kopíruje obsah pole `title` do pole `text`. To umožňuje vytvořit jedno "catch-all" pole `text` pro vyhledávání napříč více poli.
* `<uniqueKey>id</uniqueKey>`: Určuje, které pole je unikátním identifikátorem dokumentu.

**Poznámka:** Pro jednoduchost zde neuvádíme soubory `stopwords.txt` a `synonyms.txt`. Pokud byste je chtěli použít, musely by být také v adresáři `conf`.

#### d) `solr_example/sample_data.json`

Ukázková data, která budeme indexovat.

### 4. Spuštění a příprava Solru

1.  Otevřete terminál v adresáři `solr_example`.
2.  Spusťte Solr pomocí Docker Compose:
    ```bash
    docker-compose up -d
    ```
    Počkejte, než Solr kontejner nastartuje.

3.  **Ověření a vytvoření jádra (pokud se nevytvořilo automaticky):**
    * Otevřete webový prohlížeč a přejděte na Solr Admin UI: `http://localhost:8983/solr/`
    * Pokud v levém menu v sekci "Core Admin" (nebo přes "Core Selector") vidíte jádro `mycore`, je vše v pořádku. Solr detekoval konfiguraci z namapovaného adresáře.
    * **Pokud `mycore` nevidíte:**
        1.  V Solr Admin UI klikněte na "Core Admin".
        2.  Klikněte na tlačítko "Add Core".
        3.  Do pole `name` zadejte `mycore`.
        4.  Do pole `instanceDir` zadejte `mycore` (Solr bude hledat konfiguraci v `/var/solr/data/mycore/conf`, což je náš namapovaný adresář).
        5.  Ostatní pole můžete nechat prázdná nebo s výchozími hodnotami.
        6.  Klikněte na "Add Core".

### 5. Indexace dat

Data můžeme do Solru nahrát několika způsoby. Pro tento příklad použijeme Solr Admin UI.

1.  V Solr Admin UI vyberte z "Core Selectoru" (vlevo nahoře) vaše jádro `mycore`.
2.  V levém menu klikněte na "Documents".
3.  **Request-Handler:** Nechte `/update`.
4.  **Document Type:** Zvolte `JSON`.
5.  **Document(s):** Zkopírujte a vložte obsah souboru `sample_data.json` do textového pole.
6.  **Commit Within:** Můžete nastavit, za jak dlouho se mají změny projevit v indexu (např. 1000 ms). Pro okamžité projevení můžete nechat prázdné a provést commit manuálně, nebo nastavit nízkou hodnotu.
7.  Klikněte na "Submit Document".

Měli byste vidět zprávu o úspěchu. Pokud chcete, aby se změny okamžitě projevily ve vyhledávání (pokud jste nenastavili nízký `Commit Within`), můžete provést "Commit":
* V Solr Admin UI (stále v sekci `mycore` -> "Documents") najděte tlačítko "Commit" (obvykle pod formulářem pro nahrání dokumentů) a klikněte na něj.

**Alternativní indexace pomocí `curl`:**
```bash
curl -X POST -H 'Content-type:application/json' 'http://localhost:8983/solr/mycore/update/json/docs?commit=true' --data-binary @sample_data.json
```
* `commit=true` v URL zajistí, že se změny ihned projeví.

### 6. Základní vyhledávací dotazy

1.  V Solr Admin UI vyberte jádro `mycore`.
2.  V levém menu klikněte na "Query".
3.  Zde můžete zadávat dotazy.

**Příklady dotazů (zadávejte do pole `q`):**

* **Najít všechny dokumenty:**
    `*:*`

* **Najít dokumenty obsahující slovo "Solr" (v libovolném poli, které je typu `text_general` a je zahrnuto v defaultním vyhledávacím poli, nebo v poli `text` díky `copyField`):**
    `Solr`
    nebo explicitněji (prohledá výchozí pole `text`):
    `text:Solr`

* **Najít dokumenty obsahující slovo "Apache" v poli `title`:**
    `title:Apache`

* **Najít dokumenty obsahující frázi "Apache Solr" v poli `description`:**
    `description:"Apache Solr"` (uvozovky pro frázi)

* **Najít dokumenty z kategorie "Technologie":**
    `category:Technologie` (protože `category` je `string`, hledá se přesná shoda)

* **Najít dokumenty od autora "Jan Novák":**
    `author:"Jan Novák"`

* **Kombinace (AND je výchozí operátor):** Najít dokumenty obsahující "Solr" A z kategorie "Technologie":
    `Solr AND category:Technologie`
    nebo
    `q=Solr&fq=category:Technologie` (`fq` znamená "filter query", je často efektivnější pro filtrování)

* **OR operátor:** Najít dokumenty obsahující "Solr" NEBO "Spark":
    `Solr OR Spark`

* **NOT operátor (nebo mínus):** Najít dokumenty obsahující "Apache", ale NE "Spark":
    `Apache NOT Spark`
    nebo
    `Apache -Spark`

* **Vyhledávání podle roku:**
    `year:2023`

* **Rozsahové vyhledávání pro rok:** Najít dokumenty z let 2022 až 2023:
    `year:[2022 TO 2023]`

Můžete experimentovat s různými parametry v Query UI, např.:
* `fl`: Seznam polí, která se mají vrátit (např. `id,title,score` – `score` je skóre relevance).
* `rows`: Počet výsledků na stránku.
* `sort`: Řazení (např. `year desc` pro řazení podle roku sestupně).

### 7. Fasetování (Faceting)

Fasetování umožňuje dynamicky generovat kategorie a počty dokumentů v těchto kategoriích na základě výsledků vyhledávání. Je to klíčová funkce pro navigaci a filtrování.

1.  V Solr Admin UI (v sekci "Query" pro jádro `mycore`):
2.  Zadejte základní dotaz, např. `q=*:*` (všechny dokumenty) nebo `q=Apache`.
3.  Zaškrtněte políčko `facet` (obvykle vpravo nebo níže).
4.  **`facet.field`**: Zadejte název pole, podle kterého chcete fasetovat. Můžete zadat více polí.
    * Zkuste: `category`
    * Zkuste přidat další: `author`
    * Zkuste přidat další: `year`
5.  Ostatní parametry fasetování (jako `facet.limit`, `facet.mincount`) můžete nechat na výchozích hodnotách.
6.  Spusťte dotaz.

Ve výsledcích (obvykle ve formátu JSON nebo XML, podle toho, co máte nastaveno jako `wt` – writer type) uvidíte kromě samotných dokumentů i sekci `facet_counts`, která bude obsahovat fasety:
```json
// ... část odpovědi ...
"facet_counts": {
  "facet_queries": {},
  "facet_fields": {
    "category": [
      "Technologie", 3,  // Kategorie "Technologie" má 3 dokumenty ve výsledcích
      "Kuchařky", 2     // Kategorie "Kuchařky" má 2 dokumenty
    ],
    "author": [
      "Eva Svobodová", 1,
      "Jan Novák", 1,
      "Marie Veselá", 1,
      "Petr Dvořák", 1,
      "Tomáš Procházka", 1
    ],
    "year": [
      2023, 2,
      2022, 1,
      2021, 1,
      2024, 1
    ]
  },
  // ... další typy faset ...
}
```
Tato informace se pak na frontendu používá k zobrazení filtrů, kde uživatel vidí např. "Kategorie: Technologie (3), Kuchařky (2)". Kliknutím na fasety může uživatel dále zužovat výsledky vyhledávání.

### 8. Další kroky a co prozkoumat

* **Pokročilejší schéma:** Prozkoumejte další typy polí, analyzátory (stemming pro češtinu, n-gramy), filtry.
* **Různé request handlery:** Solr má mnoho request handlerů pro různé účely (DisMax, eDisMax pro robustnější fulltextové vyhledávání, MoreLikeThis pro hledání podobných dokumentů).
* **SolrCloud:** Pokud máte zájem, můžete si zkusit nastavit jednoduchý SolrCloud cluster (vyžaduje ZooKeeper).
* **Integrace s aplikací:** Zkuste se připojit k Solru z vaší oblíbené programovací platformy (Python má knihovnu `pysolr`, Java má SolrJ atd.).
* **Optimalizace relevance:** Zjistěte, jak Solr počítá skóre relevance (TF-IDF, BM25) a jak ho lze ovlivnit (boostování polí atd.).

Tento příklad poskytuje pouze základní úvod. Apache Solr je velmi mocný nástroj s mnoha funkcemi a možnostmi konfigurace.
