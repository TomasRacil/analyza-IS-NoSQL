# Docker: Teorie a základy

Tento dokument poskytuje úvod do Dockeru, jeho základních konceptů a principů. Obsahuje také praktické příklady, které vám pomohou s prvními kroky.

## Co je Docker?

Docker je platforma pro vývoj, distribuci a spouštění aplikací v *kontejnerech*. Kontejnerizace je způsob, jak zabalit aplikaci a všechny její závislosti (knihovny, konfigurace, runtime prostředí) do jednoho izolovaného balíčku.  Tento balíček (kontejner) lze pak snadno spustit na jakémkoli systému, který má nainstalovaný Docker, bez ohledu na to, jaký operační systém nebo konfiguraci má daný systém.

**Výhody Dockeru:**

*   **Izolace:** Kontejnery jsou izolované od hostitelského operačního systému a od ostatních kontejnerů. To zajišťuje, že aplikace neběží v konfliktu s jinými aplikacemi nebo systémovými nastaveními.
*   **Přenositelnost:** Kontejnery lze snadno přesouvat mezi různými prostředími (vývoj, testování, produkce) a různými počítači.
*   **Konzistence:**  Všichni (vývojáři, testeři, provozní tým) pracují se stejným prostředím, což eliminuje problémy typu "u mě to funguje".
*   **Opakovatelnost:**  Kontejnery lze snadno vytvářet, spouštět, zastavovat a mazat. To usnadňuje automatizaci a testování.
*   **Efektivita:**  Kontejnery sdílejí jádro operačního systému, což je činí menšími a rychlejšími než virtuální stroje.
*   **Škálovatelnost:**  Docker umožňuje snadno škálovat aplikace spuštěním více instancí kontejneru.

## Instalace Dockeru

Předtím, než začnete s Dockerem, je potřeba ho nainstalovat. Doporučený způsob instalace je pomocí **Docker Desktop**, který je dostupný pro Windows, macOS a Linux.

**Docker Desktop:**

*   **Stáhněte si Docker Desktop** z oficiálních stránek: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
*   **Spusťte instalační program** a postupujte podle instrukcí.
*   **Po instalaci spusťte Docker Desktop.**  (Na Windows a macOS se obvykle objeví ikona velryby v oznamovací oblasti/menu baru.)
*   **Ověřte instalaci:** Otevřete terminál (nebo příkazový řádek) a zadejte příkaz `docker --version`. Měla by se vypsat verze Dockeru.

**Alternativní instalace (Linux):**

Pokud nechcete používat Docker Desktop, můžete Docker Engine nainstalovat přímo. Postup se liší podle distribuce Linuxu.  Instrukce naleznete v oficiální dokumentaci Dockeru: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

**Důležité:**

*   Po instalaci Dockeru *může být* nutné restartovat počítač.
*   Na Linuxu budete možná muset přidat svého uživatele do skupiny `docker`, abyste mohli spouštět Docker příkazy bez `sudo`.  (Viz dokumentace k vaší distribuci.)
* Pro Docker Compose, pokud jste instalovali Docker Desktop, je už v instalaci, pokud ne, instrukce naleznete zde [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Základní pojmy

*   **Image:**  Image je *read-only* šablona pro vytvoření kontejneru. Obsahuje vše potřebné pro běh aplikace: kód, knihovny, konfiguraci, runtime prostředí.  Image je jako "plán" nebo "otisk" kontejneru.
*   **Kontejner:** Kontejner je *běžící instance* image.  Je to izolované prostředí, ve kterém běží aplikace.  Kontejner má vlastní souborový systém, síťové rozhraní a procesy.
*   **Dockerfile:**  Dockerfile je textový soubor, který obsahuje instrukce pro vytvoření image.  Definuje, jaké základní image se má použít, jaké příkazy se mají spustit uvnitř kontejneru, jaké soubory se mají zkopírovat, atd.
*   **Docker Hub:**  Docker Hub je veřejný registr Docker imagí.  Je to obrovská knihovna předpřipravených imagí, které můžete použít pro své aplikace (např. image pro Nginx, MongoDB, Python, Node.js, atd.).
*   **Volume:**  Volume je způsob, jak data v Dockeru *persistují* (přežívají) i po smazání kontejneru.  Kontejnery jsou obvykle dočasné – když je smažete, data uvnitř se ztratí.  Volumes umožňují data ukládat mimo kontejner, takže je můžete sdílet mezi kontejnery nebo je zachovat i po restartu.
*   **Síť (Network):**  Docker sítě umožňují komunikaci mezi kontejnery. Kontejnery ve stejné síti se mohou navzájem "vidět" a komunikovat spolu pomocí jmen služeb (např. `web` a `mongo` v našem příkladu s Nginx a MongoDB).
*   **Docker Compose:**  Docker Compose je nástroj pro definování a spouštění *vícekontejnerových* aplikací.  Používá soubor `docker-compose.yml`, ve kterém definujete služby (kontejnery), jejich konfiguraci a vzájemné propojení.  Je to mnohem pohodlnější než spouštět každý kontejner zvlášť.

## Základní příkazy

Zde jsou některé základní příkazy Dockeru, které budete často používat:

*   **`docker pull <image_name>:<tag>`:** Stáhne image z registru (např. Docker Hubu).  `tag` je nepovinný a určuje verzi image (např. `latest`, `1.23`, atd.).  Pokud `tag` nezadáte, použije se `latest`.
    *   Příklad: `docker pull nginx:latest` (stáhne nejnovější verzi Nginx)
    *   Příklad: `docker pull ubuntu:20.04` (stáhne Ubuntu 20.04)

*   **`docker images`:** Zobrazí seznam lokálně stažených imagí.

*   **`docker run <options> <image_name>:<tag> <command>`:** Vytvoří a spustí kontejner z daného image.
    *   `-d`: Spustí kontejner na pozadí (detached mode).
    *   `-p <host_port>:<container_port>`: Mapuje port kontejneru na port hostitelského počítače.
    *   `-v <host_path>:<container_path>`: Připojí volume (adresář na hostiteli do adresáře v kontejneru).
    *   `--name <container_name>`: Pojmenuje kontejner.
    *   `<command>`: Příkaz, který se má spustit uvnitř kontejneru (nepovinný, pokud je definován v image).

    *   Příklad: `docker run -d -p 8080:80 --name my-nginx nginx:latest` (spustí Nginx na pozadí, mapuje port 80 kontejneru na port 8080 hostitele a pojmenuje kontejner `my-nginx`)

*   **`docker ps`:** Zobrazí seznam *běžících* kontejnerů.
*   **`docker ps -a`:** Zobrazí seznam *všech* kontejnerů (i zastavených).

*   **`docker stop <container_id_or_name>`:** Zastaví běžící kontejner.
*   **`docker start <container_id_or_name>`:** Spustí zastavený kontejner.
*   **`docker rm <container_id_or_name>`:** Smaže kontejner (musí být zastavený).
*   **`docker rmi <image_id_or_name>`:** Smaže image (nesmí být používán žádným kontejnerem).

*   **`docker exec -it <container_id_or_name> <command>`:** Spustí příkaz *uvnitř* běžícího kontejneru.  `-it` umožňuje interaktivní přístup (typicky shell).
    *   Příklad: `docker exec -it my-nginx bash` (spustí Bash shell uvnitř kontejneru `my-nginx`)

*   **`docker build -t <image_name>:<tag> <path_to_dockerfile>`:** Vytvoří image z Dockerfile.
    *   `-t <image_name>:<tag>`: Pojmenuje image a (volitelně) přidá tag.
    *   `<path_to_dockerfile>`: Cesta k adresáři, kde se nachází Dockerfile (obvykle `.`, tedy aktuální adresář).
    *   Příklad: `docker build -t my-app:1.0 .`

*   **`docker-compose up -d`:** Spustí aplikaci definovanou v souboru `docker-compose.yml` (v aktuálním adresáři). `-d` spustí kontejnery na pozadí.
*   **`docker-compose down`:** Zastaví a smaže kontejnery, sítě a (volitelně) volumes definované v `docker-compose.yml`.

## Praktické příklady

V adresáři `priklady` naleznete několik jednoduchých příkladů, které ilustrují základní použití Dockeru:

1.  **`01-hello-world`:** Nejjednodušší možný příklad – spuštění oficiálního "hello-world" image z Docker Hubu.
2.  **`02-vlastni-image`:** Vytvoření vlastního image pomocí Dockerfile.
3.  **`03-docker-compose`:** Spuštění jednoduché aplikace s více kontejnery pomocí Docker Compose.

Projděte si tyto příklady a vyzkoušejte si je.  Každý příklad má vlastní `README.md` soubor s podrobnými instrukcemi.
