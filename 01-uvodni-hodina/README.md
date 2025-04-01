# Analýza informačních systémů: Úvodní hodina

## Přehled předmětu

V tomto předmětu se budeme zabývat moderními přístupy k ukládání a zpracování dat, se zvláštním zaměřením na NoSQL databáze a nástroje pro práci s velkými objemy dat (Big Data).  Kurz je navržen tak, aby vám poskytl teoretické základy i praktické dovednosti.

**Cíle předmětu:**

*   Pochopit principy NoSQL databází a jejich rozdíly oproti relačním databázím.
*   Seznámit se s různými typy NoSQL databází (dokumentové, sloupcové, grafové, hashovací, ...).
*   Naučit se pracovat s konkrétními NoSQL systémy (CouchDB, Neo4j, ...).
*   Porozumět konceptům jako MapReduce, replikace a distribuované zpracování.
*   Získat přehled o nástrojích pro práci s Big Data (Apache Spark, Solr).
*   Procvičit si získané znalosti na praktických úkolech.

## Struktura předmětu

Kurz je rozdělen do tří hlavních tématických bloků:

1.  **Ukládání dat - NoSQL systémy:**
    *   Úvod do NoSQL databází (proč NoSQL, typy, výhody a nevýhody).
    *   Dokumentové databáze.
    *   Sloupcové databáze.
    *   Grafové databáze.
    *   Hashovací (klíč-hodnota) databáze.
    *   Objektové databáze.
    *   Time series databáze.
    *   Spatial databáze.

2.  **Systémy a nástroje:**
    *   REST API a JSON formát.
    *   MapReduce.
    *   Replikace.
    *   Distribuované zpracování.
    *   ...

3.  **Ukládání rozsáhlých kolekcí dat (Big Data):**
    *   Úvod do problematiky Big Data.
    *   Apache Spark (základy, RDD, DataFrame, Spark SQL).
    *   Apache Solr (fulltextové vyhledávání).
    *   ...

V předmětu budeme používat nástroje Git a Docker, předpokládá se, že těmto nástrojům již rozumíte. Pokud ne projděte se materiály ve složce `00-predpoklady`.

## Hodnocení

Vaše hodnocení v tomto předmětu bude založeno na následujících aktivitách:

*   **Dvě prezentační vystoupení (2 x 25% = 50%):**  V průběhu semestru bude každý student dvakrát prezentovat na hodině vybraný koncept, který byl probírán v rámci kurzu. Cílem je ukázat reálné a praktické využití tohoto konceptu. Prezentace v délce 10-15 minut. Student si vybere koncept z probírané látky (např. "Implementace REST API pro správu uživatelů", "Caching s Redisem", atd.).
*   **Výstupní test (50%):**  Na konci semestru budete psát výstupní test, který prověří vaše znalosti z celého předmětu. Test bude pokrývat témata ze všech tří bloků kurzu (NoSQL systémy, Systémy a nástroje, Ukládání rozsáhlých kolekcí dat). Na termínu testu se domlluvíme ke konci předmětu.

K splnění předmětu a udělení zápočtu musíte získat více jak *60% bodů*.

## Motivační příklad: Jednoduchý webový server s MongoDB

Nyní si pomocí Dockeru spustíme jednoduchou aplikaci, která kombinuje webový server (Nginx) a NoSQL databázi (MongoDB). Tato aplikace bude sloužit jako *velmi* zjednodušený příklad ukládání a zobrazování dat.  Nebudeme se zabývat detaily kódu aplikace.

**Klonování repozitáře:**

Nejprve si naklonujte repozitář s materiály kurzu do svého počítače.  To provedete pomocí příkazu `git clone`.  *Nahraďte `<URL_REPOZITARE>` skutečnou URL adresou repozitáře.*

```bash
git clone <URL_REPOZITARE>
cd <název_repozitáře>  # Obvykle stejný jako název repozitáře na GitHubu
```

**Struktura adresáře (po naklonování)**

Po naklonování byste měli vidět následující strukturu (nebo velmi podobnou - může se v průběhu kurzu měnit):

```
analyza-IS-NoSQL/  <-- Hlavní adresář repozitáře
├── 01-uvodni-hodina/
│    ├── README.md  <-- Dokument, který právě čtete.
│    └── motivacni-priklad
│        ├── docker-compose.yml
│        ├── index.html
│        └── README.md <-- Nyní si otevřete tento soubor
├── README.md  <-- Tento soubor
└── ... (další lekce a materiály)
```

Po naklonování si otevřete soubor `README.md`, který je v složce `01-uvodni-hodina/motivacni-priklad`.

## Příprava na příští hodinu

<!-- 1.  **Založte si účet na GitHubu** (pokud ho ještě nemáte). -->
1. **Nainstalujte si Docker**. Doporučuji Docker Desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
2.  **Stahněte si repozitář** na váš počítač.
3. **Vyzkoušejte si spuštění ukázkové aplikace** pomocí `docker-compose up -d`.

---