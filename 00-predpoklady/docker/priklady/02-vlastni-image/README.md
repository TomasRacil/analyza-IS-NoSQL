# Příklad 02: Vlastní Image

V tomto příkladu si vytvoříme vlastní Docker image pomocí `Dockerfile`.

## Struktura

*   **`Dockerfile`:** Obsahuje instrukce pro vytvoření image.
*   **`app.py`:** Jednoduchý Python skript, který bude spuštěn uvnitř kontejneru.

## Obsah souborů

*   **`Dockerfile`:**

    ```dockerfile
    # Použijeme oficiální Python image jako základ
    FROM python:3.9-slim-buster

    # Nastavíme pracovní adresář uvnitř kontejneru
    WORKDIR /app

    # Zkopírujeme soubor app.py do kontejneru
    COPY app.py .

    # Spustíme app.py při startu kontejneru
    CMD ["python", "app.py"]
    ```

*   **`app.py`:**

    ```python
    print("Ahoj z mého vlastního Docker image!")

    ```

## Vytvoření a spuštění

1.  **Otevřete terminál** a přejděte do tohoto adresáře (`00-predpoklady/docker/priklady/02-vlastni-image/`).
2.  **Vytvořte image** pomocí příkazu:

    ```bash
    docker build -t my-python-app:1.0 .
    ```

    *   `-t my-python-app:1.0`:  Pojmenuje image `my-python-app` a přidá tag `1.0`.
    *   `.`:  Říká Dockeru, aby hledal `Dockerfile` v aktuálním adresáři.

3.  **Spusťte kontejner** z nově vytvořeného image:

    ```bash
    docker run my-python-app:1.0
    ```

    Měli byste vidět výstup "Ahoj z mého vlastního Docker image!".

## Vysvětlení `Dockerfile`

*   **`FROM python:3.9-slim-buster`:**  Říká Dockeru, aby použil oficiální Python 3.9 image jako *základní image*.  `slim-buster` je menší verze image, která obsahuje jen nezbytné součásti.
*   **`WORKDIR /app`:**  Nastaví `/app` jako *pracovní adresář* uvnitř kontejneru.  Všechny následující příkazy se budou provádět v tomto adresáři.
*   **`COPY app.py .`:**  Zkopíruje soubor `app.py` z vašeho počítače do pracovního adresáře (`/app`) uvnitř kontejneru.
*   **`CMD ["python", "app.py"]`:**  Určuje, jaký příkaz se má spustit při *startu* kontejneru.  V tomto případě se spustí Python skript `app.py`.