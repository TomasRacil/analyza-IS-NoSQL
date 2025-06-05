from pyspark.sql import SparkSession
import time
import os

if __name__ == "__main__":
    start_time = time.time()

    # Vytvoření SparkSession
    # .master("spark://spark-master:7077") určuje adresu Spark masteru v Docker síti
    # .appName definuje název aplikace
    spark = (
        SparkSession.builder.appName("PythonWordCount")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )

    # Získání SparkContextu ze SparkSession
    sc = spark.sparkContext

    # Nastavení úrovně logování pro menší množství výpisů od Sparku
    sc.setLogLevel("WARN")

    # Cesta k vstupnímu souboru uvnitř kontejneru workeru
    # Předpokládáme, že data jsou dostupná na sdíleném volume nebo zkopírována
    # V našem docker-compose.yml mapujeme lokální adresář `app/data` na `/opt/spark-data` v kontejnerech
    input_file_path = "/opt/spark-data/input.txt"

    output_dir_path = "/opt/spark-data/spark_output"  # Cesta pro uložení výsledků

    print(f"Načítání souboru: {input_file_path}")

    try:
        # Načtení textového souboru jako RDD (Resilient Distributed Dataset)
        # Každý řádek souboru bude prvkem RDD
        lines = sc.textFile(input_file_path)

        # Zjištění a výpis počtu particí po načtení
        num_partitions_after_load = lines.getNumPartitions()
        print(f"Počet particí RDD 'lines' po načtení: {num_partitions_after_load}")

        # Transformace RDD:
        # 1. flatMap: Rozdělí každý řádek na slova (tokeny) a "zploští" seznamy slov do jednoho RDD slov
        #    lambda line: line.split(" ") -> pro každý řádek zavolá split(" ")
        words = lines.flatMap(lambda line: line.lower().split(" "))

        # 2. filter: Odstraní prázdné řetězce, které mohly vzniknout po splitu
        words = words.filter(lambda word: len(word) > 0)

        # 3. map: Pro každé slovo vytvoří pár (slovo, 1)
        #    lambda word: (word, 1) -> pro každé slovo vrátí tuple (slovo, 1)
        word_counts_intermediate = words.map(lambda word: (word, 1))

        # 4. reduceByKey: Sečte hodnoty (jedničky) pro každý unikátní klíč (slovo)
        #    lambda a, b: a + b -> pro stejný klíč sečte jeho hodnoty
        word_counts = word_counts_intermediate.reduceByKey(lambda a, b: a + b)

        # Zjištění a výpis počtu particí finálního RDD
        num_partitions_final = word_counts.getNumPartitions()
        print(
            f"Počet particí RDD 'word_counts' před jakoukoliv akcí: {num_partitions_final}"
        )

        # Diagnostická akce .count()
        try:
            count_of_word_counts = word_counts.count()
            print(
                f"Počet unikátních slov (ověření akcí .count()): {count_of_word_counts}",
                flush=True,
            )
        except Exception as e_count:
            print(f"Chyba při word_counts.count(): {e_count}", flush=True)
            # Pokud .count() selže, nemá smysl pokračovat k .saveAsTextFile()
            raise e_count  # Znovu vyvoláme chybu, aby se zachytila v hlavním except bloku

        # Místo collect() použijeme saveAsTextFile()
        # To uloží každou partici RDD 'word_counts' jako samostatný soubor do zadaného adresáře
        print(f"Ukládání výsledků do adresáře: {output_dir_path}", flush=True)

        # Před zápisem zkusíme smazat adresář pomocí Hadoop FileSystem API, pokud existuje
        # To je robustnější způsob pro Spark
        fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(sc._jsc.hadoopConfiguration())
        path_to_delete = sc._jvm.org.apache.hadoop.fs.Path(output_dir_path)
        if fs.exists(path_to_delete):
            print(
                f"Mažu existující adresář na workeru: {output_dir_path} pomocí Hadoop FS API",
                flush=True,
            )
            fs.delete(path_to_delete, True)  # True pro rekurzivní smazání

        # Snížení počtu particí na 1 pro získání jednoho výstupního souboru
        # Toto může být náročné na paměť pro driver, pokud je výsledné RDD velké
        final_sorted_rdd = word_counts.coalesce(1)

        # Seřazení výsledků: nejprve podle počtu sestupně, pak podle slova vzestupně
        # Použijeme sortBy, které bere lambda funkci vracející klíč pro řazení
        # (-x[1], x[0]) -> -x[1] pro sestupné řazení podle počtu, x[0] pro vzestupné podle slova
        sorted_word_counts = final_sorted_rdd.sortBy(lambda x: (-x[1], x[0]))

        sorted_word_counts.saveAsTextFile(output_dir_path)
        print(f"Výsledky úspěšně uloženy do {output_dir_path}", flush=True)

    except Exception as e:
        print(f"Nastala chyba při zpracování Spark úlohy: {e}")

    finally:
        # Ukončení SparkSession
        spark.stop()

    end_time = time.time()
    print(f"Doba zpracování (Spark): {end_time - start_time:.4f} sekund")
