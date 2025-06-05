## Praktický příklad: Základy HDFS s Dockerem

Tento příklad vás provede spuštěním jednoduchého HDFS (Hadoop Distributed File System) clusteru pomocí Docker Compose a ukáže, jak provádět základní souborové operace pomocí příkazové řádky HDFS.

### 1. Cíle příkladu

* Spustit minimální HDFS cluster skládající se z NameNode a jednoho DataNode.
* Porozumět základní interakci s HDFS.
* Nahrát soubor z lokálního systému do HDFS.
* Vytvořit adresář v HDFS.
* Zobrazit obsah adresáře a souboru v HDFS.
* Stáhnout soubor z HDFS na lokální systém.

### 2. Struktura adresáře (pro HDFS příklad)

Pro tento příklad budete potřebovat následující strukturu ve vašem projektu:

```
hdfs_example/
├── docker-compose.yml
└── sample_files/          # Adresář pro ukázkové soubory k nahrání do HDFS
    └── my_test_file.txt
```

### 3. Soubory pro HDFS příklad

#### a) `hdfs_example/docker-compose.yml`

Tento soubor definuje služby pro NameNode a DataNode. Použijeme populární image od `kiwenlau`, které jsou připraveny pro jednoduché Hadoop clustery.

* **`kiwenlau/hadoop-namenode:3.2.1-java8`** a **`kiwenlau/hadoop-datanode:3.2.1-java8`**: Použité Docker image.
* **`ports` u `namenode`**:
    * `9870:9870`: Webové rozhraní NameNodu.
    * `9000:9000`: Port, na kterém HDFS naslouchá pro připojení (FSDefaultName).
* **`volumes` u `namenode`**: Mapuje lokální adresář `sample_files` do kontejneru `namenode` do cesty `/root/sample_files`. To nám usnadní nahrávání souborů do HDFS, protože budeme příkazy spouštět z kontejneru `namenode`.
* **`environment` u `datanode1`**: `CORE_CONF_fs_defaultFS=hdfs://namenode:9000` je klíčové, aby DataNode věděl, kde hledat NameNode.
* **`networks`**: Všechny služby jsou ve stejné síti `hadoop_network`, aby spolu mohly komunikovat pomocí názvů služeb.

#### b) `hdfs_example/sample_files/my_test_file.txt`

### 4. Spuštění HDFS clusteru

1.  **Vytvořte strukturu adresářů** (`hdfs_example`, `hdfs_example/sample_files`) a umístěte do nich výše uvedené soubory.
2.  Otevřete terminál v adresáři `hdfs_example`.
3.  Spusťte HDFS cluster pomocí Docker Compose:
    ```bash
    docker-compose up -d
    ```
    Stažení obrazů a první spuštění může chvíli trvat. NameNode potřebuje nějaký čas na formátování a inicializaci.

4.  **Ověření (volitelné):**
    * Počkejte asi minutu nebo dvě, než systém plně naběhne.
    * Otevřete webový prohlížeč a přejděte na NameNode Web UI: `http://localhost:9870`. Měli byste vidět informace o clusteru, včetně připojeného DataNodu (v sekci "Datanodes"). Pokud DataNode nevidíte, dejte mu ještě chvíli.

### 5. Interakce s HDFS pomocí CLI

Budeme používat příkazovou řádku HDFS (`hdfs dfs ...`) spouštěnou **uvnitř kontejneru `namenode`**.

1.  **Připojte se k běžícímu `namenode` kontejneru:**
    ```bash
    docker exec -it namenode bash
    ```
    Nyní jste v shellu uvnitř kontejneru `namenode`. Všechny následující `hdfs dfs` příkazy spouštějte zde.

2.  **Vytvoření adresáře v HDFS:**
    Vytvoříme adresář `/user/test_data` v HDFS.
    ```bash
    hdfs dfs -mkdir -p /user/test_data
    ```
    * `-mkdir`: Příkaz pro vytvoření adresáře.
    * `-p`: Vytvoří i nadřazené adresáře, pokud neexistují (podobně jako `mkdir -p` v Linuxu).

3.  **Výpis obsahu adresáře v HDFS:**
    ```bash
    hdfs dfs -ls /user
    hdfs dfs -ls /user/test_data
    ```
    * `-ls`: Příkaz pro výpis obsahu adresáře.

4.  **Nahrání lokálního souboru do HDFS:**
    Soubor `my_test_file.txt` jsme namapovali do `/root/sample_files/` uvnitř kontejneru `namenode`.
    ```bash
    hdfs dfs -put /sample_files/my_test_file.txt /user/test_data/
    ```
    * `-put <lokální_cesta_v_kontejneru> <cesta_v_HDFS>`: Nahraje soubor.

5.  **Znovu výpis obsahu adresáře v HDFS:**
    ```bash
    hdfs dfs -ls /user/test_data
    ```
    Nyní byste měli vidět soubor `my_test_file.txt`.

6.  **Zobrazení obsahu souboru v HDFS:**
    ```bash
    hdfs dfs -cat /user/test_data/my_test_file.txt
    ```
    * `-cat`: Vypíše obsah souboru na standardní výstup.

7.  **Stažení souboru z HDFS do "lokálního" systému kontejneru:**
    Stáhneme soubor zpět do adresáře `/tmp/` uvnitř kontejneru `namenode`.
    ```bash
    hdfs dfs -get /user/test_data/my_test_file.txt /tmp/downloaded_from_hdfs.txt
    ```
    * `-get <cesta_v_HDFS> <lokální_cesta_v_kontejneru>`: Stáhne soubor.

8.  **Ověření staženého souboru (uvnitř kontejneru `namenode`):**
    ```bash
    cat /tmp/downloaded_from_hdfs.txt
    ```
    Měli byste vidět stejný obsah jako v původním souboru.

9.  **Ukončení `bash` session v kontejneru:**
    ```bash
    exit
    ```

### 6. Zastavení HDFS clusteru

Po dokončení experimentování můžete HDFS cluster zastavit a odstranit kontejnery:
```bash
docker-compose down
```
Pokud chcete smazat i Docker volumes (kde si Hadoop může ukládat svá data, i když jsme je zde explicitně nedefinovali pro perzistenci dat HDFS samotného):
```bash
docker-compose down -v
```

### 7. Co bylo demonstrováno?

* **Základní architektura HDFS:** Viděli jsme, jak NameNode a DataNode spolupracují.
* **Interakce přes HDFS CLI:** Naučili jsme se základní příkazy pro manipulaci se soubory a adresáři v HDFS.
* **Princip distribuovaného úložiště:** I když jsme měli jen jeden DataNode, data byla spravována systémem navrženým pro distribuci a replikaci (která by se projevila s více DataNody).
* **Web UI NameNodu:** Můžete prozkoumat `http://localhost:9870` a podívat se na stav clusteru, procházet souborový systém atd.

Tento příklad je zjednodušený. Reálné HDFS clustery mají mnoho DataNodů, komplexnější konfiguraci sítě, zabezpečení a často i HDFS High Availability pro NameNode. Nicméně, pro pochopení základních principů a vyzkoušení si práce s HDFS je tento model dostačující.
