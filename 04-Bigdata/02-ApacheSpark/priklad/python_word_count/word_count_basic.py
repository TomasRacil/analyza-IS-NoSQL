import time
from collections import Counter
import os


def count_words_python(file_path):
    word_counts = Counter()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                # Odstranění bílých znaků (včetně \n) z kraje a konce řádku
                cleaned_line = line.strip()
                if not cleaned_line:  # Přeskočení prázdných řádků
                    continue
                words = cleaned_line.lower().split(" ")
                # Odstranění prázdných řetězců
                words = [word for word in words if len(word) > 0]
                word_counts.update(words)
    except Exception as e:
        print(f"Chyba při čtení souboru nebo zpracování: {e}")
        return None
    return word_counts


def save_results(results, output_file_path):
    # Seřazení výsledků: nejprve podle počtu sestupně, pak podle slova vzestupně
    # Counter.most_common() vrací seznam (slovo, počet) seřazený podle počtu sestupně.
    # Pro sekundární řazení podle slova (pokud jsou počty stejné) můžeme použít sorted.
    # Nicméně, pro jednoduchost a konzistenci s tím, jak Counter.most_common() funguje,
    # ponecháme primární řazení podle počtu. Pokud by bylo potřeba přesnější řazení
    # jako v Sparku (sestupně podle počtu, pak vzestupně podle slova), museli bychom to implementovat explicitně.
    # Pro tento příklad postačí výchozí chování most_common().
    sorted_results = (
        results.most_common()
    )  # Vrací list [(slovo, pocet), ...] seřazený podle počtu

    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, "w", encoding="utf-8") as f:
            for word, count in sorted_results:
                f.write(f"{word}: {count}\n")
        print(f"Výsledky úspěšně uloženy do {output_file_path}")
    except Exception as e:
        print(f"Chyba při ukládání výsledků: {e}")


if __name__ == "__main__":
    start_time = time.time()

    input_file = "data/input.txt"
    output_file = "data/result.txt"

    results = count_words_python(input_file)

    if results:
        save_results(results, output_file)

    end_time = time.time()
    print(f"Doba zpracování (Python): {end_time - start_time:.4f} sekund")
