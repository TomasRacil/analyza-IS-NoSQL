# Analýza IS: NoSQL, BigDAta

Toto úložiště obsahuje materiály k předmětu zaměřenému na NoSQL databáze a BigData.  Pokryjeme teoretické základy, ale hlavně se zaměříme na *praktické* použití různých typů NoSQL databází.  Budeme pracovat s reálnými příklady a úlohami, abyste si osvojili dovednosti potřebné pro práci s těmito moderními databázovými systémy.

## Struktura Repozitáře

Výukové materiály jsou rozděleny do jednotlivých adresářů, které reprezentují jednotlivé lekce/témata:

*   **`00-predpoklady/`**:  Obsahuje informace a instrukce k instalaci potřebného softwaru (Git, Docker, Docker Compose) a základní seznámení s těmito nástroji.  *Toto je nutné projít před začátkem předmětu.*
*   **`01-uvodni-hodina/`**:  Úvodní materíál k předmětu - jak bude předmět hodnoce, obsah předmětu.
*   **`02-NoSQL/`**:  Obecný úvod do problematiky, typy NoSQL databází. Praktické příklady tohoto tématu.
...

## Jak začít?

1.  **Naklonujte si repozitář:**

    ```bash
    git clone <URL_repozitare>
    cd <název_repozitáře>
    ```

2.  **Projděte si adresář `00-predpoklady/` a nainstalujte potřebný software.**
3.  **Vyuka bude strukralizovaná podle jednotlivých adresářů**  Každý adresář obsahuje:
    *   `README.md`:  Detailní popis tématu, instrukce, příklady kódu, úkoly.
    *   Další soubory (např. `docker-compose.yml`, skripty, ukázková data).

4.  **Experimentujte!**  Nebojte se zkoušet si příklady a měnit je.To je nejlepší způsob, jak se učit.

## Doporučené nástroje (kromě Dockeru a Docker Compose)

*   **Textový editor/IDE:**  Doporučuji VS Code (s rozšířeními pro Docker, JavaScript, JSON, atd.), ale můžete použít libovolný editor, který vám vyhovuje.
*   **`curl`:**  Nástroj pro posílání HTTP požadavků (často se používá pro interakci s REST API).  Je obvykle součástí Linuxových distribucí a macOS.  Pro Windows jej můžete získat např. s Git for Windows.

## Cíle kurzu

*   Rozumět základním principům NoSQL databází.
*   Umět si vybrat vhodný typ NoSQL databáze pro daný problém.
*   Mít praktické zkušenosti s několika nejpoužívanějšími NoSQL databázemi (CouchDB, Redis, MongoDB, Neo4j, Cassandra, ..).
*   Umět modelovat data v NoSQL databázích.
*   Umět dotazovat se na data v NoSQL databázích.
*   Být připraveni používat NoSQL databáze ve svých vlastních projektech.
*   Rozumět základním nástrojům pro práci s daty
*   Získat základní znalosti z oblasti BigData
*   ...