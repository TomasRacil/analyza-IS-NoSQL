## CouchDB Cheat Sheet

### 1. Základy

*   **Struktura URL:** `http://[uzivatelske_jmeno:heslo@]hostitel:port/databaze/_design/design-dokument/_view/nazev-view`
*   **Výchozí Port:** 5984
*   **Fauxton (Webové Rozhraní):** Přístup na `http://127.0.0.1:5984/_utils/`
* **Autorizace:** Většina příkazů vyžaduje autorizaci.  Použijte `-u uzivatelske_jmeno:heslo` v `curl` příkazech.

### 2. Databáze

*   **Vytvoření Databáze:**
    ```bash
    curl -X PUT -u admin:password http://127.0.0.1:5984/nazev_databaze
    ```

*   **Smazání Databáze:**
    ```bash
    curl -X DELETE -u admin:password http://127.0.0.1:5984/nazev_databaze
    ```

*   **Výpis Všech Databází:**
    ```bash
    curl -X GET -u admin:password http://127.0.0.1:5984/_all_dbs
    ```

*   **Informace o Databázi:**
    ```bash
    curl -X GET -u admin:password http://127.0.0.1:5984/nazev_databaze
    ```
* **Změny v databázi**
    ```bash
     curl -X GET -u admin:password "http://127.0.0.1:5984/nazev_databaze/_changes"

    ```
*   **Kompaktace databáze**
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/_compact
    ```

### 3. Dokumenty

*   **Vytvoření Dokumentu (s automaticky generovaným ID):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze -d '{"klic1": "hodnota1", "klic2": "hodnota2"}'
    ```

*   **Vytvoření Dokumentu (se specifikovaným ID):**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu -d '{"klic1": "hodnota1"}'
    ```

*   **Získání Dokumentu:**
    ```bash
    curl -X GET -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu
    ```

*   **Aktualizace Dokumentu:**
    1.  **Získejte aktuální revizi (`_rev`) dokumentu:**  To je *velmi důležité* v CouchDB.  Musíte vždy uvést revizi dokumentu, který aktualizujete, aby se zabránilo konfliktům.
        ```bash
        curl -X GET -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu
        ```
        (Výstup bude obsahovat pole `"_rev": "nejaka-revize"`.)

    2.  **Proveďte `PUT` požadavek s *novými daty* a *aktuální revizí*:**
        ```bash
        curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu -d '{"_rev": "aktualni-revize", "klic1": "nova_hodnota1", "klic3": "nova_hodnota3"}'
        ```
        *   `_rev`:  *Povinné*.  Musí odpovídat *aktuální* revizi dokumentu v databázi.
        *   Dokument *musíte* poslat *celý*, i s poli, která se nemění.  `PUT` nahrazuje *celý* dokument.

*   **Smazání Dokumentu:**
    1.  **Získejte aktuální revizi (`_rev`) dokumentu:** (Stejně jako u aktualizace.)
        ```bash
        curl -X GET -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu
        ```

    2.  **Proveďte `DELETE` požadavek s ID a revizí:**
        ```bash
        curl -X DELETE -u admin:password http://127.0.0.1:5984/nazev_databaze/id_dokumentu?rev=aktualni-revize
        ```
        *   `rev`: *Povinné*.

*   **Hromadné Operace (_bulk_docs):**  Efektivní způsob, jak vytvořit, aktualizovat nebo smazat *více dokumentů najednou*.
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/_bulk_docs -d '{
      "docs": [
        {"_id": "doc1", "key": "value1"},
        {"_id": "doc2", "key": "value2"},
        {"_id": "doc3", "_rev": "1-abc", "key": "updated_value"},
        {"_id": "doc4", "_rev": "1-xyz", "_deleted": true}
      ]
    }'
    ```
    *   `docs`: Pole dokumentů.
    *   `_id`:  ID dokumentu (pro vytvoření nebo aktualizaci).
    *   `_rev`:  Revize (pro aktualizaci nebo smazání).
    *   `_deleted`:  `true` pro smazání dokumentu.

* **Přidání přílohy**
   ```bash
   curl -X PUT -u admin:password 'http://127.0.0.1:5984/nazev_databaze/id_dokumentu/nazev_prilohy?rev=aktualni_revize' \
   -H "Content-Type: text/plain" \
   --data-binary @soubor.txt

   ```
* **Získání přílohy**
   ```bash
    curl -X GET -u admin:password 'http://127.0.0.1:5984/nazev_databaze/id_dokumentu/nazev_prilohy' > soubor.txt
   ```
### 4. Views (MapReduce)

*   **Vytvoření/Aktualizace Design Documentu (a View):**  Views se definují uvnitř *design documents*.

    ```bash
    curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/_design/nazev_design_dokumentu -d '{
      "views": {
        "nazev_view": {
          "map": "function (doc) { if (doc.vek) { emit(doc.vek, doc.jmeno); } }",
          "reduce": "_count"
        }
      }
    }'
    ```
    *   `views`: Objekt obsahující definice views.
    *   `nazev_view`: Název vašeho view.
    *   `map`:  *Povinná* JavaScript funkce, která mapuje dokumenty na klíče a hodnoty.
    *   `reduce`:  *Volitelná* JavaScript funkce (nebo vestavěná funkce jako `_count`, `_sum`, `_stats`), která agreguje výsledky.

*   **Dotazování na View:**
    ```bash
    curl -X GET -u admin:password "http://127.0.0.1:5984/nazev_databaze/_design/nazev_design_dokumentu/_view/nazev_view?key=hodnota&include_docs=true&reduce=false"
    ```
    *   `key`: Filtruje podle *přesné shody* klíče.
    *   `startkey` a `endkey`: Filtruje podle rozsahu klíčů.
    *   `include_docs=true`: Zahrne do výsledku *celé dokumenty* (nejen klíč a hodnotu z `emit`).
    *   `reduce=false`: Vypne reduce funkci (pokud je definovaná).  Vrátí výsledky *pouze* z map funkce.
    *  `group=true` Spustí reduce a seskupí výsledky
    *   `limit`: Omezí počet vrácených výsledků.
    *   `skip`: Přeskočí zadaný počet výsledků (pro stránkování).
    *   `descending=true`: Seřadí výsledky sestupně (podle klíče).

### 5. Mango Queries (`_find`)

*   **Dotazování:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/nazev_databaze/_find -d '{
      "selector": {
        "vek": {"$gt": 25},
        "mesto": "Praha"
      },
      "fields": ["jmeno", "email"],
      "sort": [{"vek": "desc"}],
      "limit": 10,
      "skip": 5
    }'
    ```
    *   `selector`:  *Povinný*.  Definuje filtr (podmínky).  Používá operátory jako `$gt` (větší než), `$lt` (menší než), `$eq` (rovná se), `$in` (je v poli), `$regex` (regulární výraz), `$and`, `$or`, `$not`, `$exists`, atd.
    *   `fields`:  *Volitelné*.  Projekce – které pole se mají vrátit.
    *   `sort`:  *Volitelné*.  Řazení.  Pole v poli určují pořadí řazení a směr (`asc` nebo `desc`).
    *   `limit`: *Volitelné*. Maximální počet vrácených dokumentů.
    * `skip`: *Volitelný*. Počet dokumentů, které se mají přeskočit.
*   **Vytvoření Mango Indexu:** CouchDB automaticky vytváří některé indexy, ale pro optimalizaci složitějších dotazů je *nutné* vytvořit vlastní indexy.  To se obvykle dělá přes Fauxton (webové rozhraní).  Zde je příklad, jak vytvořit index pomocí `curl`:
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://localhost:5984/testdb/_index -d '{
          "index": {
            "fields": ["age", "name"]
          },
          "name" : "age_name_index",
          "type" : "json"
        }'
    ```
    * `"ddoc"`: (volitelné) Název Design Documentu kam se má index uložit. Pokud neuvedete, CouchDB vytvoří nový.
    * `"name"`: (volitelné) Jméno indexu.
    * `"type"`: Typ indexu.  Pro Mango queries je to obvykle `"json"`.  Další možnost je `"text"` (pro fulltextové indexy – viz níže).
    * `"index"`: Objekt s polem "fields", které specifikuje indexovaná pole *v pořadí, ve kterém se mají indexovat*.

### 6. Replikace

*   **Jednorázová replikace:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/_replicate -d '{"source": "zdrojova_databaze", "target": "cilova_databaze", "create_target": true}'
     ```
    *   `source`:  Název zdrojové databáze (může být i URL vzdálené databáze).
    *   `target`:  Název cílové databáze (může být i URL vzdálené databáze).
    *   `create_target`:  `true` - vytvoří cílovou databázi, pokud neexistuje.
    *  `"continuous": true` - Spustí kontinuální replikaci.
    * `"user_ctx":{"roles":["_admin"]}` - Spustí replikaci pod administrátorem.

*   **Kontinuální replikace:**  Nastaví replikaci, která běží *neustále* a synchronizuje změny mezi databázemi.  To se obvykle nastavuje pomocí dokumentu v databázi `_replicator`.

    ```bash
    curl -X POST -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/_replicator -d '{
      "_id": "nejake_id_replikace",
      "source": "zdrojova_databaze",
      "target": "cilova_databaze",
      "continuous": true,
      "create_target": true
    }'
    ```
* **Zastavení replikace**. Smazat dokument v _replicator databázi, pomocí curl DELETE.

### 7. Další Užitečné Příkazy

* **Získání UUIDs (Universal Unique Identifiers):** CouchDB generuje UUIDs pro dokumenty (pokud je sami nezadáte).  Pro získání UUID:
    ```bash
    curl -X GET -u admin:password http://127.0.0.1:5984/_uuids
    ```

## 8. Bezpečnost

*   **Heslo:** *Vždy* nastavte silné heslo pro administrátorský účet (a případně další uživatele). To se provádí *po* první instalaci CouchDB. V produkčním prostředí byste *nikdy* neměli používat výchozí přihlašovací údaje (admin/password).

    *   **Změna hesla přes Fauxton:** Nejjednodušší způsob je přes webové rozhraní Fauxton (`http://127.0.0.1:5984/_utils/`). Přejděte do sekce "Setup" (nebo "Configuration" -> "Administrators") a nastavte heslo.

    *   **Změna hesla přes API (curl):**
        ```bash
        curl -X PUT -H "Content-Type: application/json" -u admin:stare_heslo http://127.0.0.1:5984/_node/couchdb@localhost/_config/admins/admin -d '"nove_heslo"'
        ```
        *   Nahraďte `stare_heslo` a `nove_heslo` skutečnými hodnotami.
        *  Tento příkaz mění heslo administrátora.
    *   **Vytvoření uživatele s heslem**
         ```bash
        curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/_users/org.couchdb.user:novy_uzivatel -d '{
          "name": "novy_uzivatel",
          "password": "nove_heslo",
          "roles": [],
          "type": "user"
        }'

         ```

*   **Uživatelé a Role:** CouchDB má systém uživatelů a rolí.  Měli byste vytvořit uživatele s *omezenými* právy pro vaše aplikace a *nepoužívat* administrátorský účet pro běžný provoz.
    *  **_users databáze**: CouchDB používá speciální databázi `_users` pro ukládání informací o uživatelích.
    * **Přidání uživatele** se provádí vytvořením dokumentu v databázi `_users`. Klíčem dokumentu je `org.couchdb.user:` následované jménem uživatele.
    * **Role** se přiřazují uživatelům v poli `roles` v jejich uživatelském dokumentu.
    *   **Příklad (vytvoření uživatele `mujuzivatel` s heslem `mojeheslo`):** Viz výše.

*   **Omezení Přístupu:**

    *   **Databáze:** Vytvářejte samostatné databáze pro různé aplikace nebo typy dat a přidělujte uživatelům přístup *pouze* k databázím, které potřebují.
    *   **Design Documents:**  Můžete omezit přístup k *design documents* (a tedy i k views a dalším funkcím).  To je užitečné, pokud nechcete, aby uživatelé mohli měnit logiku vašich views.
    *   **Validation Functions:** Můžete definovat *validation functions* (v design documents), které kontrolují, zda jsou dokumenty, které se uživatelé pokoušejí vytvořit/upravit/smazat, validní (např. splňují určitá pravidla, mají správný formát).
        ```javascript
        function(newDoc, oldDoc, userCtx, secObj) {
            if (newDoc.type !== "user") {
            throw({forbidden : "Only user documents are allowed"});
            }
        }
        ```
     *   `newDoc`: Nový/aktualizovaný dokument.
     *   `oldDoc`: Předchozí verze dokumentu (při aktualizaci; `null` při vytváření).
     *    `userCtx`: Kontext uživatele (obsahuje informace o přihlášeném uživateli).
    *  `secObj`: Bezpečnostní objekt databáze
    *   **`throw({forbidden: "zprava"})`:**  Pokud validace selže, vyhoďte chybu.  `forbidden` je standardní HTTP status kód (403).
    * **Show Functions**: Umožňují transformovat data před tím než jsou poslána klientovi. Lze je použít pro autorizaci
    * **List Functions**: Umožnují iterovat přes view a zpracovávat data, také je lze použít pro omezení přístupu.
*   **HTTPS (TLS/SSL):** *Vždy* používejte HTTPS pro šifrovanou komunikaci s CouchDB serverem, zejména pokud přenášíte citlivá data.
     *   **Konfigurace HTTPS:** Viz oficiální dokumentace CouchDB.  Budete potřebovat SSL/TLS certifikát a klíč.
     *   **Připojení přes HTTPS:** Použijte `https://` místo `http://` v URL.

*   **CORS (Cross-Origin Resource Sharing):**  Pokud vaše webová aplikace běží na jiné doméně než CouchDB, budete muset povolit CORS.  To se konfiguruje v CouchDB (obvykle přes Fauxton, v sekci "Configuration" -> "CORS").
    ```bash
      curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/_node/couchdb@localhost/_config/cors/enable -d 'true'
      curl -X PUT -H "Content-Type: application/json" -u admin:password http://127.0.0.1:5984/_node/couchdb@localhost/_config/cors/origins -d '"*"'
    ```

*   **Firewall:**  Omezte přístup k CouchDB serveru pomocí firewallu.  Povolte přístup pouze z důvěryhodných IP adres (vaší aplikace, atd.).  *Nikdy* nevystavujte CouchDB přímo na veřejný internet bez firewallu a HTTPS.

*   **Pravidelné Zálohování:**  Pravidelně zálohujte data z CouchDB.  Můžete použít nástroj `couchbackup` (nebo si napsat vlastní skript, který používá replikaci).

* **Aktualizace:** Udržujte CouchDB aktualizovaný na nejnovější verzi, abyste měli nejnovější bezpečnostní záplaty.

* **_security object**: Každá databáze může mít dokument _security, který určuje, kteří uživatelé a role mají k databázi přístup.

    ```bash
    curl -X PUT -u admin:password http://127.0.0.1:5984/mojedatabaze/_security -H "Content-Type: application/json" -d '{
      "admins": {
        "names": [],
        "roles": ["admin-role"]
      },
      "members": {
        "names": ["user1", "user2"],
        "roles": ["member-role"]
      }
    }'
    ```
* **Read-only přístup**: Vytvoření uživatele pouze pro čtení.

### Best Practices

*   **Používejte popisné názvy klíčů a databází:**  Usnadní to orientaci v datech.
*   **Používejte Views a Mango Queries efektivně:**  Vytvářejte indexy pro pole, podle kterých často vyhledáváte.
*   **Zvažte denormalizaci dat:** Ukládejte související data *společně* v jednom dokumentu, abyste se vyhnuli složitým dotazům.
*   **Ošetřujte chyby:** Ve vaší aplikaci ošetřujte chyby, které mohou nastat při komunikaci s CouchDB (např. síťové chyby, chyby autorizace).
*   **Monitorujte výkon:**  Sledujte využití CPU, paměti a disku na CouchDB serveru.
* **Testování**: Důkladně otestujte všechny operace s databází, včetně scénářů selhání (např. co se stane, když dojde k výpadku sítě během replikace).
