# Praktická Ukázka: MapReduce - Počítání Slov v Pythonu s Dockerem

Tento příklad demonstruje základní princip MapReduce na jednoduché úloze počítání výskytu slov v textovém souboru. Použijeme Python pro implementaci Map a Reduce fází a Docker pro spuštění skriptu v izolovaném prostředí.

## Struktura adresáře

```
priklad-map-reduce/
├── README.md (Tento soubor)
├── docker-compose.yml
├── word_count.py  (Python skript s implementací MapReduce)
└── input.txt      (Vstupní textový soubor pro analýzu)
```

## Soubory

### `docker-compose.yml`

Definuje službu `mapreduce_worker`, která spustí náš Python skript. Mapuje aktuální adresář do kontejneru, aby měl skript přístup k `input.txt`.

### `word_count.py`

Python skript, který obsahuje:
* **Mapper funkci:** Načte vstupní text, rozdělí ho na slova a pro každé slovo emituje pár (slovo, 1).
* **Reducer funkci:** Shromáždí všechny hodnoty (jedničky) pro stejné slovo a sečte je.
* Hlavní logiku, která simuluje MapReduce workflow.

### `input.txt`

Jednoduchý textový soubor obsahující věty, na kterých provedeme počítání slov.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.

## Spuštění

1.  Otevřete terminál.
2.  Přejděte do adresáře `analyza-IS-NoSQL/03-nastroje/02_MapReduce/priklad_map_reduce/`.
3.  Spusťte MapReduce úlohu pomocí Docker Compose:
    ```bash
    docker-compose up
    ```
    Docker Compose sestaví (pokud je to nutné, i když zde používáme existující Python image) a spustí kontejner. Python skript se provede a vypíše výsledky (počet jednotlivých slov) do konzole. Kontejner se po dokončení skriptu automaticky zastaví.

    Pokud chcete kontejner po dokončení odstranit, můžete použít:
    ```bash
    docker-compose up --build --remove-orphans && docker-compose down
    ```
    Nebo jednoduše po `docker-compose up`:
    ```bash
    docker-compose down
    ```

## Očekávaný výstup

Skript vypíše slovník, kde klíče jsou slova a hodnoty jsou jejich počty. Například:
```
INFO:root:Výsledky Reduce fáze:
INFO:root:{'toto': 2, 'je': 2, 'prvni': 1, 'radek': 1, 'druhy': 1}
```
(Přesný výstup závisí na obsahu `input.txt`.)

## Jak to funguje (zjednodušeně)

1.  **Map fáze:**
    * Skript načte `input.txt`.
    * Každý řádek je zpracován mapperem.
    * Mapper rozdělí řádek na slova, převede je na malá písmena a odstraní interpunkci (velmi zjednodušeně).
    * Pro každé slovo emituje pár `(slovo, 1)`.

2.  **Shuffle & Sort fáze (simulovaná):**
    * V tomto jednoduchém příkladu je tato fáze simulována seskupením identických klíčů (slov) dohromady. V reálných MapReduce systémech (jako Hadoop) je to komplexní distribuovaný proces.

3.  **Reduce fáze:**
    * Pro každé unikátní slovo vezme reducer seznam všech přiřazených jedniček.
    * Sečte tyto jedničky, čímž získá celkový počet výskytů daného slova.

Tento příklad je zjednodušenou demonstrací a neukazuje distribuovanou povahu skutečných MapReduce systémů, ale ilustruje základní logiku Map a Reduce funkcí.
