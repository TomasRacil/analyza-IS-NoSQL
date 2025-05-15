# MapReduce: Princip Distribuovaného Zpracování

MapReduce je **programovací model** a s ním spojená **implementace** pro zpracování a generování velkých datových sad pomocí paralelního, distribuovaného algoritmu na clusteru počítačů. Původně byl vyvinut společností Google a stal se základem pro mnoho technologií zpracování Big Data, včetně Apache Hadoop.

I když dnes existují modernější a často efektivnější frameworky (jako Apache Spark), pochopení principů MapReduce je stále klíčové pro porozumění základům distribuovaného zpracování dat.

## 1. Motivace: Proč MapReduce?

Představte si, že máte obrovský soubor dat (např. terabajty logů z webového serveru) a chcete provést relativně jednoduchou operaci, jako je spočítání výskytu každého slova. Zpracování takového objemu dat na jednom počítači by trvalo neúměrně dlouho nebo by bylo zcela nemožné kvůli omezením paměti a výpočetního výkonu.

MapReduce řeší tento problém tím, že:

1.  **Rozdělí data:** Vstupní datová sada je rozdělena na menší, nezávislé části (chunks, splits).
2.  **Rozdělí práci:** Zpracování těchto částí je distribuováno mezi mnoho počítačů (uzlů) v clusteru.
3.  **Paralelizuje zpracování:** Každý uzel zpracovává svou část dat paralelně s ostatními.
4.  **Agreguje výsledky:** Dílčí výsledky z jednotlivých uzlů jsou shromážděny a zkombinovány do finálního výsledku.

## 2. Základní Fáze MapReduce

MapReduce proces se skládá ze tří hlavních fází:

**a) Fáze Map:**

* **Vstup:** Část vstupních dat (split).
* **Operace:** Uživatel definuje **Map funkci**. Tato funkce je aplikována na *každý* záznam ve vstupním splitu. Jejím úkolem je transformovat vstupní záznamy na **mezilehlé páry klíč-hodnota `(key, value)`**. Klíčem je zde slovo a hodnotou číslo 1, reprezentující jeden výskyt. Často se zde provádí i normalizace (např. převod na malá písmena, odstranění interpunkce).
* **Výstup:** Proud mezilehlých párů klíč-hodnota.
* **Příklad (počítání slov):**
    * Vstupní řádek: `"Ahoj světe, ahoj"`
    * Výstup Map (po normalizaci na malá písmena): `("ahoj", 1)`, `("světe", 1)`, `("ahoj", 1)`

**b) Fáze Shuffle & Sort (Řazení a Míchání):**

* **Vstup:** Mezilehlé páry klíč-hodnota ze všech Map úloh.
* **Operace:** Framework (např. Hadoop) automaticky **shromáždí** všechny hodnoty patřící ke **stejnému klíči** (zde ke stejnému slovu po normalizaci) ze všech Map výstupů a **seřadí** je. Data jsou přerozdělena mezi Reduce uzly tak, aby všechny hodnoty pro daný klíč skončily na stejném Reduce uzlu.
* **Výstup:** Pro každý unikátní klíč je vytvořen seznam všech jeho asociovaných hodnot: `(key, [value1, value2, ...])`.
* **Příklad (počítání slov):**
    * Vstupy z různých Map úloh (již normalizované): `("ahoj", 1)`, `("světe", 1)`, `("ahoj", 1)`, `("světe", 1)`, `("ahoj", 1)`
    * Výstup Shuffle & Sort (pro dva Reduce uzly):
        * Uzel 1: `("ahoj", [1, 1, 1])`
        * Uzel 2: `("světe", [1, 1])`

**c) Fáze Reduce:**

* **Vstup:** Klíč a seznam jeho asociovaných hodnot `(key, [value1, value2, ...])`.
* **Operace:** Uživatel definuje **Reduce funkci**. Tato funkce je aplikována na *každý* unikátní klíč a jeho seznam hodnot. Jejím úkolem je **agregovat** hodnoty (v tomto případě sečíst jedničky) a vyprodukovat finální výsledek.
* **Výstup:** Finální páry klíč-hodnota (nebo jiné výsledky).
* **Příklad (počítání slov):** Reduce funkce by pro každý klíč (slovo) sečetla všechny hodnoty (jedničky) v seznamu.
    * Vstup pro Uzel 1: `("ahoj", [1, 1, 1])` -> Výstup Reduce 1: `("ahoj", 3)`
    * Vstup pro Uzel 2: `("světe", [1, 1])` -> Výstup Reduce 2: `("světe", 2)`

**Celkový výsledek:** Kombinací výstupů ze všech Reduce úloh získáme finální počet výskytů každého slova.

## 3. Klíčové Koncepty a Vlastnosti

* **Paralelizace:** Map a Reduce funkce běží paralelně na více uzlech.
* **Odolnost vůči chybám (Fault Tolerance):** Framework (např. Hadoop) automaticky detekuje selhání uzlů a znovu spustí neúspěšné úlohy na jiných uzlech.
* **Lokalita dat (Data Locality):** Framework se snaží spouštět Map úlohy na uzlech, kde jsou data fyzicky uložena, aby se minimalizoval síťový přenos.
* **Jednoduchost modelu:** Vývojář se soustředí pouze na logiku funkcí Map a Reduce, o složitost distribuovaného provedení, paralelizaci, odolnost vůči chybám a přenos dat se stará framework.
* **Škálovatelnost:** Přidáním dalších uzlů do clusteru lze snadno zvýšit výpočetní kapacitu.

## 4. Analogie: Inventura v Knihovně

Představte si, že potřebujete spočítat počet knih pro každý žánr ve velké knihovně s mnoha regály.

1.  **Rozdělení dat:** Každý regál je "split" dat.
2.  **Fáze Map:** Každý knihovník (Map úloha) dostane jeden regál. Pro každou knihu v regálu napíše na lísteček `(žánr, 1)`.
3.  **Fáze Shuffle & Sort:** Všechny lístečky se shromáždí a roztřídí podle žánru. Všechny lístečky pro "Detektivky" jdou na jednu hromádku, všechny pro "Sci-Fi" na druhou atd. Tyto hromádky se rozdělí mezi několik stolů (Reduce uzly).
4.  **Fáze Reduce:** U každého stolu sedí knihovník (Reduce úloha). Vezme hromádku pro jeden žánr (např. "Detektivky") a spočítá počet lístečků (jedniček). Výsledkem je finální počet knih pro daný žánr, např. `("Detektivky", 542)`.

## 5. Apache Hadoop

Apache Hadoop je open-source framework, který poskytuje implementaci MapReduce modelu a další komponenty pro distribuované ukládání a zpracování dat:

* **HDFS (Hadoop Distributed File System):** Distribuovaný souborový systém pro ukládání velkých datových sad napříč clusterem.
* **YARN (Yet Another Resource Negotiator):** Správce zdrojů clusteru, který plánuje a přiděluje zdroje (CPU, paměť) pro MapReduce úlohy a další aplikace.
* **MapReduce Engine:** Implementace MapReduce programovacího modelu.

Hadoop byl průkopníkem v oblasti Big Data, ale jeho MapReduce implementace má některé nevýhody (např. vysoká latence kvůli častému zápisu mezivýsledků na disk).

## 6. Výhody a Nevýhody MapReduce

**Výhody:**

* **Škálovatelnost:** Velmi dobře škáluje na velké clustery.
* **Odolnost vůči chybám:** Automatické zotavení po selhání uzlů.
* **Flexibilita:** Lze použít pro širokou škálu úloh zpracování dat.
* **Ekonomičnost:** Umožňuje využívat běžný hardware (commodity hardware).
* **Jednoduchý programovací model (pro vývojáře Map/Reduce funkcí).**

**Nevýhody:**

* **Latence:** Může mít vysokou latenci, nevhodné pro interaktivní dotazy nebo zpracování v reálném čase (zejména Hadoop MapReduce v1).
* **Složitost pro některé úlohy:** Některé algoritmy (např. iterativní) se obtížněji vyjadřují pomocí MapReduce.
* **Nutnost psát kód (Java, Python, ...):** Není tak deklarativní jako SQL.
* **Výkon:** Modernější frameworky jako Spark jsou často výrazně rychlejší díky zpracování v paměti.

## 7. MapReduce Dnes a Alternativy

MapReduce jako koncept je stále relevantní, ale jeho původní implementace v Hadoopu je často nahrazována modernějšími frameworky:

* **Apache Spark:** Nabízí podobné API inspirované MapReduce, ale provádí výpočty převážně v paměti, což vede k výrazně vyššímu výkonu. Podporuje širší škálu operací a je vhodnější pro iterativní algoritmy a interaktivní analýzu. Spark je dnes často preferovanou volbou pro zpracování Big Data.
* **Apache Flink:** Další framework zaměřený na stream processing i batch processing s nízkou latencí.
* **SQL-on-Hadoop Engines (Hive, Impala, Presto):** Umožňují používat SQL dotazy nad daty uloženými v HDFS nebo jiných úložištích, často interně využívají principy podobné MapReduce nebo modernější execution engines.

Pochopení MapReduce vám však poskytne pevný základ pro pochopení toho, jak tyto modernější systémy fungují na pozadí při distribuovaném zpracování velkých dat.

## 8. Praktická Ukázka: Počítání Slov

Pro praktické vyzkoušení základních principů Map a Reduce najdete v adresáři jednoduchý příklad "word count" (počítání slov) implementovaný v Pythonu a spuštěný pomocí Dockeru.

**Kde příklad najdete:**

* Adresář: `priklad-map-reduce/` (v rámci této sekce `02_MapReduce`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a vysvětlení kódu naleznete v souboru `priklad_map_reduce/README.md`.

**Co příklad ukazuje:**

* Jak implementovat jednoduchou Map funkci pro rozdělení textu na slova a emitování párů (slovo, 1).
* Jak implementovat jednoduchou Reduce funkci pro sečtení výskytů každého slova.
* Jak simulovat základní MapReduce workflow v jednom Python skriptu.
* Jak spustit Python skript v Docker kontejneru pomocí `docker-compose.yml` a zpracovat vstupní textový soubor.

Tento příklad slouží jako názorná ilustrace základních fází MapReduce a pomůže vám lépe uchopit teoretické koncepty.
