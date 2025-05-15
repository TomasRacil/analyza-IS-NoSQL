import re
from collections import defaultdict
import logging

# Nastavení základního logování
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


# --- Map Fáze ---
def mapper(text_line):
    """
    Zpracuje jeden řádek textu a emituje páry (slovo, 1) pro každé slovo.
    Slova jsou převedena na malá písmena a je odstraněna základní interpunkce.
    """
    logger.debug(f"Mapper zpracovává řádek: '{text_line}'")
    # Odstranění interpunkce a převedení na malá písmena
    # Toto je velmi zjednodušené, v praxi by se použily robustnější metody.
    text_line = re.sub(r"[^\w\s]", "", text_line).lower()
    words = text_line.split()
    map_output = []
    for word in words:
        if word:  # Přeskočíme prázdné řetězce po splitu
            map_output.append((word, 1))
            logger.debug(f"Mapper emituje: ({word}, 1)")
    return map_output


# --- Reduce Fáze ---
def reducer(word, counts):
    """
    Sečte všechny výskyty (counts) pro dané slovo.
    """
    logger.debug(f"Reducer zpracovává slovo: '{word}' s počty: {counts}")
    total_count = sum(counts)
    logger.debug(f"Reducer emituje: ({word}, {total_count})")
    return (word, total_count)


# --- Hlavní Logika Simulující MapReduce ---
if __name__ == "__main__":
    logger.info("Spouštění MapReduce úlohy (Word Count)...")

    input_file_path = "input.txt"
    intermediate_data = defaultdict(
        list
    )  # Pro ukládání výstupů z mapperů (simulace Shuffle & Sort)
    final_results = {}

    # 1. Čtení vstupního souboru a Map fáze
    logger.info(f"Čtení vstupního souboru: {input_file_path}")
    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            # Každý řádek je zpracován samostatným "mapperem"
            # V reálném distribuovaném systému by se řádky/části souboru
            # distribuovaly mezi více mapper uzlů.
            all_map_outputs = []
            for line in f:
                line = line.strip()
                if line:  # Zpracováváme pouze neprázdné řádky
                    all_map_outputs.extend(mapper(line))

        logger.info("Map fáze dokončena.")
        logger.debug(f"Celkový výstup Map fáze (před shuffle): {all_map_outputs}")

    except FileNotFoundError:
        logger.error(f"Chyba: Vstupní soubor '{input_file_path}' nebyl nalezen.")
        exit(1)
    except Exception as e:
        logger.error(f"Nastala chyba při čtení souboru nebo v Map fázi: {e}")
        exit(1)

    # 2. Shuffle & Sort fáze (simulovaná)
    # Seskupení hodnot podle klíčů (slov)
    # V reálném MapReduce by toto byla komplexní distribuovaná operace.
    logger.info("Simulace Shuffle & Sort fáze...")
    for key, value in all_map_outputs:
        intermediate_data[key].append(value)

    logger.info("Shuffle & Sort fáze dokončena.")
    logger.debug(f"Data po Shuffle & Sort (před Reduce): {dict(intermediate_data)}")

    # 3. Reduce fáze
    # Pro každý unikátní klíč (slovo) zavoláme reducer.
    # V reálném distribuovaném systému by se klíče distribuovaly
    # mezi více reducer uzlů.
    logger.info("Spouštění Reduce fáze...")
    for word, counts in intermediate_data.items():
        word_count_pair = reducer(word, counts)
        final_results[word_count_pair[0]] = word_count_pair[1]

    logger.info("Reduce fáze dokončena.")

    # 4. Výpis výsledků
    logger.info("Výsledky Reduce fáze:")
    # Seřazení výsledků pro konzistentní výstup (volitelné)
    sorted_results = dict(
        sorted(final_results.items(), key=lambda x: x[1], reverse=True)
    )
    logger.info(sorted_results)

    logger.info("MapReduce úloha (Word Count) dokončena.")
