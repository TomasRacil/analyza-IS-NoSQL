# Příklad 01: Hello World

Tento příklad demonstruje nejjednodušší použití Dockeru – spuštění oficiálního "hello-world" image.

## Spuštění

1.  Otevřete terminál.
2.  Spusťte příkaz:

    ```bash
    docker run hello-world
    ```

Docker stáhne image `hello-world` z Docker Hubu (pokud ho ještě nemáte lokálně) a spustí kontejner.  Uvidíte uvítací zprávu, která potvrzuje, že Docker je správně nainstalovaný a funguje.

## Co se stalo?

1.  **`docker run`:** Tento příkaz říká Dockeru, aby vytvořil a spustil nový kontejner.
2.  **`hello-world`:** Toto je název image, který se má použít.  Docker ho najde na Docker Hubu.
3.  **Stažení image:** Pokud image nemáte lokálně, Docker ho stáhne z Docker Hubu.
4.  **Vytvoření kontejneru:** Docker vytvoří nový kontejner z image `hello-world`.
5.  **Spuštění kontejneru:** Kontejner se spustí a vypíše uvítací zprávu.
6.  **Ukončení kontejneru:** Po vypsání zprávy se kontejner automaticky ukončí (protože už nemá co dělat).