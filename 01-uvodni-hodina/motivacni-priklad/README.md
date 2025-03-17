# Ukázkový příklad: Nginx + Node.js Backend + MongoDB s Docker Compose

Tento příklad demonstruje, jak pomocí Docker Compose snadno spustit a propojit tři služby:

*   **Webový server Nginx:** Slouží k zobrazení statického obsahu (HTML, CSS, JavaScript).
*   **Node.js Backend:** Jednoduchý server, který poskytuje API pro komunikaci s databází.
*   **Databáze MongoDB:** NoSQL dokumentová databáze.

Cílem tohoto příkladu je ukázat základní principy:

*   **Izolace:** Každá služba běží ve vlastním kontejneru.
*   **Propojení:** Služby spolu komunikují.
*   **Snadné spuštění:** Celou aplikaci (všechny tři služby) lze spustit jediným příkazem.
*   **Perzistence dat:** Data v MongoDB jsou uložena v *Docker volume*, takže zůstanou zachována i po restartování nebo smazání kontejneru.
* **Základní architektura**: Ukázka běžného uspořádání webové aplikace (frontend, backend, databáze)

## Struktura

*   **`docker-compose.yml`:** Definuje služby (Nginx, Node.js backend, MongoDB), jejich konfiguraci a propojení.
*   **`index.html`:** HTML soubor s JavaScriptem, který komunikuje s Node.js backendem.
* **`backend/`**: Adresář obsahující soubory pro Node.js backend
    * **`backend/index.js`**: Kód Node.js serveru.
    * **`backend/Dockerfile`**: Dockerfile pro sestavení image Node.js backendu.
    * **`backend/package.json`**: Soubor popisující Node.js projekt a jeho závislosti.

## Obsah souborů

(Zde by mohly být znovu uvedeny *zkrácené* verze souborů, nebo jen odkazy na ně, abychom se neopakovali.  Pro studenty je lepší mít *celý* kód na jednom místě (v souborech), než ho hledat rozkouskovaný v README.)

*   **`docker-compose.yml`:** (Viz kompletní verze v předchozích odpovědích)
*   **`index.html`:** (Viz kompletní verze v předchozích odpovědích)
*  **`backend/index.js`**: (Viz kompletní verze v předchozích odpovědích)
* **`backend/Dockerfile`**: (Viz kompletní verze v předchozích odpovědích)
* **`backend/package.json`**: (Viz kompletní verze v předchozích odpovědích)

## Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.** (Viz instrukce v hlavním `README.md` souboru kurzu.)
2.  **Otevřete terminál** a přejděte do tohoto adresáře (`01-uvodni-hodina/motivacni-priklad`).
3.  **Spusťte aplikaci** příkazem:

    ```bash
    docker-compose up -d
    ```

    Tento příkaz stáhne potřebné image (pokud je nemáte), vytvoří a spustí kontejnery na pozadí. Poprvé to může trvat déle, protože se musí sestavit image pro Node.js backend.

4.  **Ověřte funkčnost:** Otevřete v prohlížeči adresu `http://localhost:8080`. Měla by se zobrazit stránka, která umožňuje přidávat a zobrazovat data z MongoDB.

5.  **Zkontrolujte běžící kontejnery:**

    ```bash
    docker-ps
    ```
    Měli byste vidět tři běžící kontejnery (pro Nginx, Node.js backend a MongoDB).

6. **Zkontrolujte vytvořený volume:**
     ```bash
      docker volume ls
     ```

## Zastavení

Pro zastavení a odstranění kontejnerů (a sítě) použijte:

```bash
docker-compose down
```

Pro zastavení, smazání kontejnerů, resources a smazání *volumes* spusťte:

```bash
docker-compose down -v
```

## Vysvětlení `docker-compose.yml`

*   **`version: "3.9"`:** Určuje verzi syntaxe souboru Docker Compose.
*   **`services:`:** Definuje jednotlivé služby.
    *   **`web:`:**
        *   **`image: nginx:latest`:** Používá oficiální image Nginx.
        *   **`ports: ["8080:80"]`:** Mapuje port 80 kontejneru na port 8080 hostitele.
        *   **`volumes: [...]`:** Mapuje `index.html` do kontejneru.
        *   **`depends_on: [backend]`:**  Zajistí, že se Nginx spustí až po Node.js backendu.
    *   **`backend:`:**
        *   **`build: ./backend`:** Sestaví image z `Dockerfile` v adresáři `backend`.
        *   **`ports: ["3000:3000"]`:** Mapuje port 3000 kontejneru (kde běží Node.js) na port 3000 hostitele.  *Pozn.:*  K tomuto portu se připojuje JavaScript z `index.html`.
        * **`environment: - MONGO_URL=mongodb://mongo:27017/mydatabase`:** Nastavuje proměnnou prostředí s URL pro připojení k MongoDB.
        *   **`depends_on: [mongo]`:** Zajistí, že se backend spustí až po MongoDB.
    *   **`mongo:`:**
        *   **`image: mongo:latest`:** Používá oficiální image MongoDB.
        *   **`volumes: [mongodb_data:/data/db]`:** Vytvoří volume pro persistenci dat.
*   **`volumes:`:** Definuje pojmenované volumes.
    *   **`mongodb_data:`:** Vytvoří volume `mongodb_data`.

## Vysvětlení `backend/index.js`
* **`const express = require('express');`**: Importuje framework Express
* **`const { MongoClient } = require('mongodb');`**: Importuje MongoClient z MongoDB driveru.
* **`const cors = require('cors');`**: Importuje CORS middleware.
* **`const app = express();`**: Vytvoří instanci Express aplikace.
* **`const port = 3000;`**: Definuje port, na kterém bude server naslouchat.
* **`const mongoUrl = ...;`**: Nastaví URL pro připojení k MongoDB (z proměnné prostředí nebo výchozí).
* **`const dbName = 'mydatabase';`**:  Název databáze.
* **`const collectionName = 'items';`**:  Název kolekce.
* **`app.use(cors());`**: Povolí CORS pro *všechny* origins (pro jednoduchost – v produkci byste to omezili!).
* **`app.use(express.json());`**:  Middleware pro parsování JSON těla requestu (potřebné pro POST requesty).
*   **`connectToMongo()`:** Asynchronní funkce, která se připojí k MongoDB a vrátí objekt databáze.
* **IIFE**: Okamžitě vyvolaná asynchroní funkce, která se postará o spuštění `connectToMongo`
*   **`app.get('/items', ...)`:**  Definuje endpoint pro získání všech položek (GET request na `/items`).
*   **`app.post('/items', ...)`:**  Definuje endpoint pro přidání nové položky (POST request na `/items`).
*   **`app.listen(port, ...)`:**  Spustí server na daném portu.

## Vysvětlení `index.html`

*   **`const apiUrl = 'http://localhost:3000/items';`:**  Definuje URL adresu API backendu.
*   **`loadData()`:**  Funkce, která načte data z backendu (GET `/items`) a zobrazí je na stránce.
*   **`addItem()`:**  Funkce, která odešle data z formuláře na backend (POST `/items`).
*   **Event listener:**  Připojí funkci `addItem()` k tlačítku "Přidat".