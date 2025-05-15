# Praktická Ukázka: Jednoduché REST API s Node.js a Express v Dockeru

Tento příklad demonstruje vytvoření a spuštění jednoduchého REST API serveru pomocí Node.js, frameworku Express a Dockeru. API bude poskytovat základní CRUD operace pro správu seznamu úkolů.

## Struktura adresáře

```

priklad-rest/
├── README.md (Tento soubor)
├── requests.http (Soubor s HTTP požadavky pro VS Code REST Client)
├── docker-compose.yml
└── backend/
    ├── Dockerfile
    ├── index.js
```

## Soubory

### `docker-compose.yml`

Definuje službu `api_server`, která sestaví a spustí naši Node.js aplikaci.

### `backend/Dockerfile`

Obsahuje instrukce pro sestavení Docker image pro Node.js aplikaci.

### `backend/index.js`

Obsahuje kód samotného Express serveru s definovanými API endpointy.

### `requests.http`

Obsahuje sadu HTTP požadavků pro testování API pomocí rozšíření **REST Client (humao.rest-client)** ve Visual Studio Code.

## Předpoklady

* Nainstalovaný Docker a Docker Compose.
* Visual Studio Code s nainstalovaným rozšířením **REST Client** od Huachao Mao (identifikátor: `humao.rest-client`).

## Spuštění

1.  Otevřete terminál.
2.  Přejděte do adresáře `analyza-IS-NoSQL/03-nastroje/01_Komunikace_se_serverem/priklad-rest/`.
3.  Spusťte aplikaci pomocí Docker Compose:
    ```bash
    docker-compose up -d --build
    ```
    * `--build` zajistí sestavení Docker image, pokud ještě neexistuje nebo pokud byly provedeny změny v `backend/Dockerfile` nebo souvisejících souborech.
    * `-d` spustí kontejnery na pozadí.

Aplikace by nyní měla běžet na `http://localhost:3000`.

## Testování API

API můžete testovat několika způsoby:

### 1. Pomocí `curl` (příkazová řádka)

Příklady `curl` požadavků jsou uvedeny níže a také v tomto `README.md`.

* **Získání všech úkolů (GET /tasks):**
    ```bash
    curl http://localhost:3000/tasks
    ```
* **Vytvoření nového úkolu (POST /tasks):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"title": "Nakoupit mléko"}' http://localhost:3000/tasks
    ```
* **Získání konkrétního úkolu (GET /tasks/:id):**
    ```bash
    curl http://localhost:3000/tasks/1
    ```
* **Aktualizace úkolu (PUT /tasks/:id):**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"title": "Nakoupit mléko a chleba", "completed": true}' http://localhost:3000/tasks/1
    ```
* **Smazání úkolu (DELETE /tasks/:id):**
    ```bash
    curl -X DELETE http://localhost:3000/tasks/1
    ```

### 2. Pomocí VS Code REST Client Extension

1.  Otevřete soubor `api_requests.http` ve Visual Studio Code.
2.  Nad každým HTTP požadavkem (odděleným `###`) se objeví odkaz "Send Request".
3.  Kliknutím na "Send Request" se požadavek odešle a odpověď se zobrazí v novém panelu.

Můžete postupně procházet požadavky v souboru `requests.http` a sledovat, jak API reaguje.

### 3. Pomocí jiných API klientů

Můžete také použít nástroje jako Postman nebo Insomnia.

## Zastavení aplikace

Pro zastavení a odstranění kontejnerů definovaných v `docker-compose.yml` použijte:
```bash
docker-compose down
```

Tento příklad poskytuje základní kostru pro pochopení, jak lze API server kontejnerizovat a spravovat pomocí Dockeru. Studenti si mohou kód dále upravovat a rozšiřovat.
