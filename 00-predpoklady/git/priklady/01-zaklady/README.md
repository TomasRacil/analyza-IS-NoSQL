# Příklad 01: Základy Gitu

Tento příklad ukazuje základní workflow Gitu: inicializaci repozitáře, přidání souborů, vytvoření commitu a prohlížení historie.

## Postup

1.  **Vytvořte nový adresář** (nebo použijte existující) pro váš projekt. Například:

    ```bash
    mkdir muj-prvni-git-projekt
    cd muj-prvni-git-projekt
    ```

2.  **Inicializujte Git repozitář:**

    ```bash
    git init
    ```

    Tím se vytvoří skrytý adresář `.git` uvnitř `muj-prvni-git-projekt`.

3.  **Vytvořte soubor `README.md`** s nějakým obsahem (například pomocí textového editoru nebo příkazu `echo`):

    ```bash
    echo "# Můj první Git projekt" > README.md
    ```

4.  **Přidejte soubor `README.md` do staging area:**

    ```bash
    git add README.md
    ```

5.  **Vytvořte commit:**

    ```bash
    git commit -m "Přidán README.md"
    ```

6.  **Upravte soubor `README.md`** (přidejte nějaký další text).

7.  **Přidejte změny do staging area:**

    ```bash
    git add README.md
    ```

8. **Vytvořte druhý commit:**

   ```bash
    git commit -m "Aktualizován README.md"
   ```

9.  **Prohlédněte si historii commitů:**

    ```bash
    git log
    ```

    Měli byste vidět dva commity, každý s unikátním hashem, autorem, datem a zprávou.

    ```bash
    git log --oneline # Zjednodušená verze
    ```

10. **Volitelné: Vytvořte ještě jeden soubor a přidejte ho do repozitáře.**
    ```bash
    echo "print('Hello from git')" > script.py
    git add script.py
    git commit -m "Added a python script"
    ```