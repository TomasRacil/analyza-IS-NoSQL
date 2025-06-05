## Praktický příklad: Apache Spark vs. Standardní Python pro Word Count

Tento příklad demonstruje základní úlohu počítání slov (Word Count) pomocí Apache Sparku (PySpark) a porovnává ji s implementací ve standardním Pythonu. Cílem je ukázat rozdílný přístup a zdůraznit výhody Sparku pro zpracování dat, zejména v kontextu větších datasetů a distribuovaného prostředí.

### Scénář úlohy

Máme textový soubor a chceme spočítat frekvenci každého slova v tomto souboru.

**Vstupní data (`data/input.txt`)**


### Řešení 1: Apache Spark (PySpark)

Toto řešení využívá Apache Spark spuštěný v clusteru (simulovaném pomocí Docker Compose) s jedním master uzlem a jedním worker uzlem.

#### Struktura adresáře (pro Spark řešení)

```
spark_example/
├── docker-compose.yml
├── app/
│   ├── word_count.py  # Náš PySpark skript
│   └── data/
│       └── input.txt    # Vstupní textový soubor
└── Dockerfile         # Dockerfile pro Spark aplikaci (Python prostředí)
```

#### Soubory pro Spark řešení

**1. `spark_word_count/Dockerfile`**

Tento Dockerfile připraví prostředí pro naši PySpark aplikaci.

**2. `spark_word_count/app/word_count.py`**

PySpark skript pro počítání slov.

**3. `spark_word_count/app/data/input.txt`**

Soubor se vstupními daty.


**4. `spark_word_count/docker-compose.yml`**

Docker-compose starající se o nasazení dvou workerů a master služby.

#### Spuštění Spark řešení

1.  Ujistěte se, že jste v adresáři `spark_word_count`.
2.  Sestavte a spusťte kontejnery:
    ```bash
    docker-compose up --build
    ```
    Při prvním spuštění může stažení Spark image a sestavení `spark-app` image chvíli trvat.
3.  V adresáři `data/spark_output` by jste měli vidět výstupní soubor.

#### Sledování distribuovaného zpracování ve Spark UI

Po spuštění můžete otevřít následující webová rozhraní ve vašem prohlížeči:

* **Spark Master UI:** [`http://localhost:8080`](http://localhost:8080)
    * Zde uvidíte **připojené workery** (měli byste vidět `spark-worker-1` a `spark-worker-2`).
    * V sekci "Running Applications" nebo "Completed Applications" najdete vaši aplikaci `PythonWordCountDistributed`.
* **Spark Application UI:** Kliknutím na ID vaší aplikace v Master UI se dostanete na detailní rozhraní aplikace.
    <!-- * **Jobs:** Úloha Word Count bude pravděpodobně reprezentována jedním nebo více "joby".
    * **Stages:** Každý job je rozdělen na "stages" (fáze). Stage představuje sadu úloh (tasks), které mohou být provedeny paralelně bez nutnosti přesunu dat (shuffle). Operace jako `reduceByKey` typicky způsobí vznik nové stage kvůli potřebě shufflování dat.
    * **Tasks:** Každá stage je dále rozdělena na "tasks". Každá task zpracovává jednu partici dat. **Zde uvidíte, jak jsou jednotlivé tasky distribuovány mezi dostupné workery (`spark-worker-1` a `spark-worker-2`).** Můžete sledovat, které tasky běžely na kterém workeru a jak dlouho trvaly.
    * **Storage:** Můžete vidět, které RDD jsou cachované a jak jsou jejich partice distribuovány. -->
    * **Executors:** Zobrazuje seznam aktivních executorů (našich workerů) a jejich využití.

**Co sledovat pro demonstraci distribuce:**

* V Master UI ověřte, že jsou oba workery (`spark-worker-1`, `spark-worker-2`) připojeny a aktivní.
* V Application UI (po kliknutí na vaši aplikaci):
    <!-- * Podívejte se na záložku "Stages". Uvidíte, kolik stages vaše aplikace má.
    * Pro každou stage klikněte na její popis. Zobrazí se DAG (Directed Acyclic Graph) této stage a seznam tasks.
    * V seznamu tasks pro danou stage sledujte sloupec "Executor ID" nebo "Host". Měli byste vidět, že tasky jsou přiřazovány různým workerům. Pokud je dat málo nebo je počet particí nízký, může se stát, že všechny tasky skončí na jednom workeru, ale Spark má mechanismus, jak je distribuovat. -->
    * V PySpark skriptu jsme přidali výpis `lines.getNumPartitions()` a `word_counts.getNumPartitions()`. Spark se snaží určit optimální počet particí na základě velikosti dat a počtu dostupných jader. Pro náš malý soubor to může být stále nízké číslo (např. 2, pokud má každý worker 1 jádro a máme 2 workery). Při zpracování velkých souborů z HDFS by počet particí typicky odpovídal počtu bloků HDFS.


#### Očekávaný výstup (Spark)

Výstup z kontejneru `spark-app-wordcount` bude obsahovat logy Sparku a na konci něco jako:
```
... (Spark logy) ...
...
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
25/06/05 09:27:11 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Načítání souboru: /opt/spark-data/input.txt
Počet particí RDD 'lines' po načtení: 2
Počet particí RDD 'word_counts' před jakoukoliv akcí: 2
Počet unikátních slov (ověření akcí .count()): 200                              
Ukládání výsledků do adresáře: /opt/spark-data/spark_output
Mažu existující adresář na workeru: /opt/spark-data/spark_output pomocí Hadoop FS API
Výsledky úspěšně uloženy do /opt/spark-data/spark_output
Doba zpracování (Spark): X.Y sekund
...
```

### Řešení 2: Standardní Python

Toto řešení provede stejnou úlohu pomocí jednoduchého Python skriptu bez využití Sparku.

#### Soubor pro Python řešení

**`python_word_count/word_count_basic.py`**

**`python_word_count/data/input.txt`** (stejný jako pro Spark)


#### Spuštění Python řešení

1.  Ujistěte se, že jste v adresáři `python_word_count`.
2.  Spusťte skript z adresáře `python_word_count`:
    ```bash
    python word_count_basic.py
    ```

#### Očekávaný výstup (Python)

```
Výsledky úspěšně uloženy do data/result.txt
Doba zpracování (Python): X.Y sekund
```

### Srovnání a výhody Sparku

1.  **Distribuované zpracování a škálovatelnost:**
    * **Spark:** S dvěma workery Spark **distribuuje** zpracování particí dat mezi tyto workery. To je viditelné ve Spark UI, kde uvidíte tasky běžící na `spark-worker-1` i `spark-worker-2`. Pokud bychom přidali další workery a data, Spark by automaticky škáloval a využíval dostupné zdroje. Každý worker zpracovává pouze část dat, což vede k paralelnímu provádění.
    * **Python:** Stále běží na jednom jádře jednoho stroje.

2.  **Abstrakce pro distribuovaná data (RDD):**
    * **Spark:** RDD `lines` je nyní rozděleno na více particí (pravděpodobně minimálně 2, pokud Spark detekuje 2 jádra workerů jako výchozí paralelizmus pro `textFile`). Každá partice může být zpracována nezávisle na jiném workeru.
    * **Python:** Bez změny.

3.  **Odolnost proti chybám (Fault Tolerance):**
    * **Spark:** Pokud by jeden z našich dvou workerů selhal během zpracování, Spark Master by detekoval selhání a přeplánoval by tasky, které na něm běžely, na zbývajícího funkčního workera (nebo na nového, pokud by byl dostupný). Lineage RDD umožňuje rekonstrukci ztracených dat.
    * **Python:** Bez změny.

4.  **Optimalizace provádění (DAG Scheduler):**
    * **Spark:** DAG scheduler stále optimalizuje plán. Ve Spark UI můžete vidět, jak je job rozdělen na stages (např. jedna stage pro `flatMap`, `filter`, `map` a další stage pro `reduceByKey` kvůli shuffle). Tasky v rámci jedné stage běží paralelně.
    * **Python:** Bez změny.

5.  **Sledování a ladění:**
    * **Spark UI (`http://localhost:8080` a `http://localhost:4040`) poskytuje detailní vhled do toho, jak Spark provádí výpočty:**
        * Kolik particí bylo vytvořeno.
        * Jak jsou tasky distribuovány mezi workery.
        * Které operace způsobují shuffle (přesun dat mezi workery).
        * Doba trvání jednotlivých tasks, stages a jobs.
        * Případné chyby a úzká hrdla.
    * Toto je neocenitelné pro ladění a optimalizaci výkonu na reálných, velkých datasetech.
    * **Python:** Možnosti ladění a monitorování jsou omezeny na standardní Python nástroje, které neposkytují vhled do distribuovaného provádění.

**Důležitá poznámka k tomuto lokálnímu demo:**
I s více workery v Docker Compose na jednom fyzickém stroji sdílejí všechny kontejnery zdroje tohoto jednoho stroje (CPU, RAM, I/O). Skutečný přínos distribuovaného zpracování se naplno projeví až na reálném clusteru více fyzických nebo virtuálních strojů. Nicméně, toto nastavení nám umožňuje **demonstrovat a pochopit mechanismy distribuce, paralelizace a odolnosti proti chybám, které Spark nabízí.**

Na našem (stále relativně malém) datasetu nemusí být rozdíl v *celkové době zpracování* mezi Sparkem a Pythonem dramatický, protože režie Spark clusteru (komunikace mezi masterem, workery, odesílání úloh) může stále převážit nad přínosem paralelizace pro takto malá data. Ale principy jsou klíčové. Představte si zpracování terabajtů dat – tam by byl rozdíl propastný.
