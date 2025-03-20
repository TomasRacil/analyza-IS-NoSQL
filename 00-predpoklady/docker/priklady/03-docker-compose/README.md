# Příklad 03: Docker Compose

Tento příklad ukazuje, jak použít Docker Compose pro spuštění jednoduché aplikace s webovým serverem (Nginx) a jednoduchou "databází" (JSON soubor).

## Struktura

*   **`docker-compose.yml`:** Definuje služby (Nginx a "databáze").
*   **`index.html`:** HTML soubor, který bude zobrazován Nginxem.
*   **`data.txt`:** Textový soubor, který bude simulovat databázi.

## Obsah souborů

*   **`docker-compose.yml`:**

    ```yaml
    version: "3.9"
    services:
      web:
        image: nginx:latest
        ports:
          - "8080:80"
        volumes:
          - ./index.html:/usr/share/nginx/html/index.html
          - ./data.txt:/usr/share/nginx/html/data.txt
    ```

*   **`index.html`:**

    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ukázka Docker Compose</title>
    </head>
    <body>
        <h1>Data:</h1>
        <pre id="data"></pre>
        <script>
            fetch('data.txt')
                .then(response => response.text())
                .then(text => {
                    document.getElementById('data').textContent = text;
                });
        </script>
    </body>
    </html>
    ```

* **`data.json`:**
    ```json
    {
    "message": "Toto jsou data z mé 'databáze'."
    }
    ```

## Spuštění

1.  **Otevřete terminál** a přejděte do tohoto adresáře (`00-predpoklady/docker/priklady/03-docker-compose/`).
2.  **Spusťte aplikaci** pomocí příkazu:

 ```bash
 docker-compose up -d
 ```

3.  **Ověřte funkčnost:** Otevřete v prohlížeči adresu `http://localhost:8080`. Měla by se zobrazit stránka s textem z `data.txt`.

## Zastavení
```bash
 docker-compose down
```

## Vysvětlení
`docker-compose.yml`: Definuje pouze jednu službu (web), která používá Nginx.

`volumes::` Mapujeme dva soubory: index.html (pro zobrazení stránky) a data.txt (pro simulaci databáze).

`index.html:` Obsahuje jednoduchý