# Analýza informačních systémů: Úvodní hodina

## Přehled předmětu

V tomto předmětu se budeme zabývat moderními přístupy k ukládání a zpracování dat, se zvláštním zaměřením na NoSQL databáze a nástroje pro práci s velkými objemy dat (Big Data).  Kurz je navržen tak, aby vám poskytl teoretické základy i praktické dovednosti.

**Cíle předmětu:**

*   Pochopit principy NoSQL databází a jejich rozdíly oproti relačním databázím.
*   Seznámit se s různými typy NoSQL databází (dokumentové, sloupcové, grafové, hashovací).
*   Naučit se pracovat s konkrétními NoSQL systémy (CouchDB, MongoDB, ..).
*   Porozumět konceptům jako MapReduce, replikace a distribuované zpracování.
*   Získat přehled o nástrojích pro práci s Big Data (Apache Spark, Solr).
*   Procvičit si získané znalosti na praktických úkolech a projektu.

## Struktura předmětu

Kurz je rozdělen do tří hlavních tématických bloků:

1.  **Ukládání dat - NoSQL systémy:**
    *   Úvod do NoSQL databází (proč NoSQL, typy, výhody a nevýhody).
    *   Dokumentové databáze.
    *   Sloupcové databáze.
    *   Grafové databáze.
    *   Hashovací (klíč-hodnota) databáze.
    *   MapReduce.
    *   Replikace.
    *   Distribuované zpracování.

2.  **Systémy a nástroje (CouchDB, MongoDB):**
    *   Instalace a konfigurace CouchDB a MongoDB (s využitím Dockeru).
    *   Práce s daty v CouchDB a MongoDB (vkládání, dotazování, aktualizace, mazání).
    *   REST API a JSON formát.

3.  **Ukládání rozsáhlých kolekcí dat (Big Data):**
    *   Úvod do problematiky Big Data.
    *   Apache Spark (základy, RDD, DataFrame, Spark SQL).
    *   Apache Solr (fulltextové vyhledávání).

V předmětu budeme používat nástroje Git a Docke, předpokládá se že těmto nástrojům již rozumíte.

## Hodnocení

Vaše hodnocení v tomto předmětu bude založeno na následujících aktivitách:

*   **Tři malé úkoly (3 x 10% = 30%):**  Tyto úkoly budou zaměřeny na procvičení konkrétních témat probíraných v jednotlivých blocích.  Budete je odevzdávat prostřednictvím GitHubu. Na zpracování úkolu budete mít vždy 14 dní. Neodevzdání úkolu v termínu vás automaticky připravuje o body.
*   **Jeden velký projekt (70%):**  Na konci semestru budete odevzdávat a prezentovat větší projekt, který bude vyžadovat integraci znalostí z celého předmětu.  Projekt bude také odevzdáván prostřednictvím GitHubu. Zadání, které si navrhnete sami, od vás obdržím do 4 týdnů od zahájení předmětu (tzn. 17.4.2025). Projekt je třeba odevzdat nejpozději dva týdny po poslední hodině (tzn. 3.7.2025)

K splnění předmětu a udělení zápočtu musíte získat více jak 60% bodů.

## Motivační příklad: Jednoduchý webový server s MongoDB

Nyní si pomocí Dockeru spustíme jednoduchou aplikaci, která kombinuje webový server (Nginx) a NoSQL databázi (MongoDB). Tato aplikace bude sloužit jako *velmi* zjednodušený příklad ukládání a zobrazování dat.  Nebudeme se zabývat detaily kódu aplikace (to přijde později), ale zaměříme se na to, jak Docker usnadňuje spuštění a propojení těchto dvou komponent.

**Klonování repozitáře:**

Nejprve si naklonujte repozitář s materiály kurzu do svého počítače.  To provedete pomocí příkazu `git clone`.  *Nahraďte `<URL_REPOZITARE>` skutečnou URL adresou repozitáře.*

```bash
git clone <URL_REPOZITARE>
cd <název_repozitáře>  # Obvykle stejný jako název repozitáře na GitHubu
```

**Struktura adresáře (po naklonování)**

Po naklonování byste měli vidět následující strukturu (nebo velmi podobnou - může se v průběhu kurzu měnit):

```
AnalyzaISNoSQL/  <-- Hlavní adresář repozitáře
├── 01_MotivacniPriklad/
│    ├── docker-compose.yml
│    ├── index.html
│    └── README.md <-- Nyní si otevřete tento soubor
├── README.md  <-- Tento soubor
└── ... (další lekce a materiály)
```

Po naklonování si otevřete soubor `README.md`, který je v složce `01_MotivacniPriklad`.

## Příprava na příští hodinu

1.  **Založte si účet na GitHubu** (pokud ho ještě nemáte).
2. **Nainstalujte si Docker**. Doporučuji Docker Desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
3.  **Nahrajte strukturu adresářů** (včetně souborů `docker-compose.yml` a `index.html`) na váš GitHub repozitář.
4. **Vyzkoušejte si spuštění ukázkové aplikace** pomocí `docker-compose up -d`.
5. **První malý úkol:** Nainstalujte si docker a zprovozněte hello-world. Návod naleznete zde [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/). Výsledek v podobě screenshotu nahrajte do vašeho repositáře do složky `ukoly/01`.

---