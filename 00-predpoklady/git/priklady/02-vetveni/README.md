# Příklad 02: Větvení v Gitu

Tento příklad ukazuje, jak vytvořit novou větev, přepínat mezi větvemi a slučovat změny.

## Postup

1.  **Ujistěte se, že jste v repozitáři z předchozího příkladu** (`muj-prvni-git-projekt`).  Pokud ne, vytvořte si nový repozitář a přidejte do něj nějaké soubory (viz příklad 01).  Měli byste mít alespoň soubor `README.md` a ideálně i `script.py`.

2.  **Vytvořte novou větev s názvem `nova-funkce`:**

    ```bash
    git checkout -b nova-funkce
    ```

    Tento příkaz vytvoří novou větev a rovnou do ní přepne.  (`git branch nova-funkce` by větev jen vytvořilo, ale nepřepnulo by do ní.)

3.  **Vytvořte nový soubor (nebo upravte existující) ve větvi `nova-funkce`:**

    ```bash
    echo "Toto je nová funkce." > funkce.txt
    git add funkce.txt
    git commit -m "Přidána funkce.txt"
    ```

4.  **Přepněte zpět do hlavní větve (např. `main` nebo `master`):**

    ```bash
    git checkout main
    ```

    Všimněte si, že soubor `funkce.txt` v pracovním adresáři zmizí – je součástí větve `nova-funkce`, ne `main`.

5.  **Zobrazte seznam větví:**

    ```bash
    git branch
    ```

    Měla by se zobrazit hvězdička u `main` a v seznamu i `nova-funkce`

6.  **Sloučte změny z větve `nova-funkce` do `main`:**

    ```bash
    git merge nova-funkce
    ```

    Tento příkaz sloučí změny z `nova-funkce` do aktuální větve (`main`).  Soubor `funkce.txt` se nyní objeví i v `main`.

7.  **(Volitelné) Smažte větev `nova-funkce` (pokud už ji nepotřebujete):**

    ```bash
    git branch -d nova-funkce
    ```

    `-d` smaže větev *pouze*, pokud už byla sloučena.  Pokud by v ní byly nějaké nesloučené změny, Git by vás upozornil.  Pro *nucené* smazání (i s nesloučenými změnami) použijte `-D`.

8. **Vytvořte konflikt a vyřešte ho.**
    * Přepněte se do `nova-funkce`: `git checkout -b nova-funkce-2`
    * Upravte `script.py`, přidejte na konec souboru: `print("Hello from branch")`
    * Commit: `git add script.py && git commit -m "Added greeting from branch"`
    * Přepněte zpět do `main`: `git checkout main`
    * Upravte *stejný* řádek v `script.py`, ale jinak: `print("Hello from main branch!")`
    * Commit: `git add script.py && git commit -m "Added greeting from main"`
    * Zkuste merge: `git merge nova-funkce-2`
        * Dostanete hlášku o konfliktu (CONFLICT). Git automaticky upraví soubor `script.py` a označí v něm konfliktní místa. Bude vypadat nějak takto:
            ```
            print('Hello from git')
            <<<<<<< HEAD
            print("Hello from main branch!")
            =======
            print("Hello from branch")
            >>>>>>> nova-funkce-2
            ```
        * Vyberte jednu z variant, nebo upravte soubor tak, aby obsahoval to, co chcete. Odstraňte značky `<<<<<<<`, `=======`, `>>>>>>>`.
        * Po úpravě souboru ho přidejte do staging area a commitněte:
          ```bash
          git add script.py
          git commit -m "Vyřešen konflikt"
          ```
    * Nyní je konflikt vyřešen.
