# Dokumentové Databáze

## 1. Dokumentové Databáze: Teorie

### 1.1 Datový Model

Dokumentové databáze ukládají data v *dokumentech*.  Tyto dokumenty jsou typicky ve formátu **JSON** (JavaScript Object Notation) nebo jeho binární variantě **BSON** (Binary JSON).  Dokumenty si můžeme představit jako *samo-popisné* struktury, které obsahují data ve formátu *klíč-hodnota*.

*   **Klíč (Key):**  Řetězec, který identifikuje danou hodnotu (např. `"name"`, `"age"`, `"address"`).
*   **Hodnota (Value):**  Může být:
    *   **Skalární hodnota:**  Číslo (integer, float), řetězec (string), boolean (true/false), datum.
    *   **Pole (Array):**  Uspořádaný seznam hodnot (např. seznam koníčků: `["reading", "hiking"]`).
    *   **Vnořený dokument (Embedded Document/Object):**  Další dokument, který umožňuje vytvářet hierarchické struktury (např. adresa jako vnořený dokument uvnitř dokumentu uživatele).

**Příklad JSON dokumentu:**

```json
{
  "_id": "john_doe",   // Unikátní identifikátor dokumentu (povinný)
  "name": "John Doe",
  "age": 30,
  "email": "[e-mailová adresa byla odstraněna]",
  "address": {         // Vnořený dokument (adresa)
    "street": "123 Main St",
    "city": "Anytown"
  },
  "hobbies": ["reading", "hiking", "coding"], // Pole řetězců
  "active": true
}
```

**Klíčové vlastnosti dokumentového modelu:**

*   **Schéma-less (Schemaless) nebo Schéma-flexible:**  Na rozdíl od relačních databází, kde musíte předem definovat strukturu tabulek (sloupce a datové typy), dokumentové databáze *nemají* pevně dané schéma.  To znamená, že:
    *   Různé dokumenty ve stejné *kolekci* (viz níže) mohou mít *různou strukturu*.  Můžete mít dokument uživatele s polem `email` a jiný dokument uživatele bez tohoto pole.
    *   Můžete *snadno* přidávat a odebírat pole v dokumentech bez nutnosti migrace schématu (žádné `ALTER TABLE`).
*   **Denormalizace:** V relačních databázích se data obvykle *normalizují* (rozdělují do více tabulek), aby se minimalizovala redundance. V dokumentových databázích se data často *denormalizují* – související data se ukládají *společně* v jednom dokumentu.  To zvyšuje výkon při čtení, protože nemusíte provádět JOINy přes více tabulek.  V příkladu výše je adresa *součástí* dokumentu uživatele (vnořený dokument).
*   **Hierarchická data:**  Díky vnořeným dokumentům a polím je dokumentový model *přirozeně* vhodný pro reprezentaci hierarchických dat.
*   **Kolekce (Collections):** Dokumenty jsou seskupeny do *kolekcí*.  Kolekce je analogická tabulce v relační databázi, ale s tím rozdílem, že *nemusí* mít pevně dané schéma.

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Flexibilita:**  Snadná změna struktury dat bez složitých migrací.  Ideální pro agilní vývoj a rychle se měnící požadavky.
*   **Výkon:**  Denormalizace a optimalizované dotazovací mechanismy (indexy) často vedou k *vysokému výkonu* pro čtení i zápis, zejména pokud data, která potřebujete, jsou uložena v *jednom* dokumentu.
*   **Škálovatelnost:**  Dokumentové databáze jsou obvykle navrženy pro *horizontální škálování* (distribuce dat na více serverů).  To umožňuje zvládat velké objemy dat a vysokou zátěž.
*   **Přirozené mapování:**  JSON (a BSON) se velmi dobře mapuje na objekty v objektově orientovaných programovacích jazycích, což zjednodušuje vývoj aplikací.

**Nevýhody:**

*   **Omezené transakce (ACID):**  Toto je *největší nevýhoda* oproti relačním databázím.  Zatímco relační databáze poskytují silné záruky *ACID* (Atomicity, Consistency, Isolation, Durability) pro transakce přes *více* tabulek, dokumentové databáze obvykle poskytují ACID záruky *pouze* na úrovni *jednoho dokumentu*.  Transakce přes více dokumentů jsou buď *nepodporované*, nebo *složité a méně výkonné*.  To znamená, že pokud potřebujete provést operaci, která zahrnuje konzistentní změnu *více* dokumentů, musíte si logiku transakce zajistit *sami* v kódu aplikace. CouchDB podporuje ACID vlastnosti pouze na úrovni jednoho dokumentu. MongoDB od verze 4.0 přidala podporu multi-document ACID transakcí, ale s určitými omezeními a potenciálním dopadem na výkon.
*   **Složitější dotazování na vztahy:**  Vztahy mezi dokumenty (např. uživatel a jeho příspěvky) se typicky řeší:
    *   **Vnořením:**  Vnořené dokumenty (jako adresa v našem příkladu).  Vhodné pro vztahy "má" (has-a), kde vnořený dokument nemá smysl sám o sobě.
    *   **Referencemi:**  Ukládáním ID jiného dokumentu (podobně jako cizí klíče v relačních databázích).  Vhodné pro vztahy "má mnoho" (has-many) a "patří do" (belongs-to).
    *   **Problém:**  Neexistuje zde koncept *JOIN* operace jako v SQL.  Pokud potřebujete získat data z více dokumentů propojených referencemi, musíte provést *více dotazů* a "spojit" data *v kódu aplikace*.  To je méně efektivní a složitější než JOIN.
*   **Relační Integrita:** Relační databáze umožňují definovat cizí klíče, které *vynucují* integritu vztahů (např. nemůžete smazat kategorii, pokud na ni odkazují nějaké produkty). Dokumentové databáze toto *obecně* nenabízejí (musíte si to ošetřit v aplikaci).

### 1.3 Příklady Dokumentových Databází

*   **MongoDB:**  Jedna z nejpopulárnějších dokumentových databází.  Používá BSON, má bohatý dotazovací jazyk, podporuje indexy, sharding (horizontální škálování), replikaci a (od verze 4.0) multi-document transakce.
*   **Couchbase:**  Kombinuje vlastnosti key-value a dokumentových databází.  Zaměřuje se na výkon a škálovatelnost.
*   **CouchDB:**  Zaměřuje se na spolehlivost, snadné použití a offline synchronizaci.  Používá JSON a HTTP API.  Vhodná pro mobilní aplikace.
*   **Amazon DocumentDB:**  Dokumentová databáze kompatibilní s MongoDB API, nabízená jako služba na AWS.
*   **Azure Cosmos DB:**  Multi-model databáze od Microsoftu, která podporuje různé datové modely, včetně dokumentového.

### 1.4 Kdy je dokumentová databáze lepší volbou než relační?

Dokumentové databáze, jako je CouchDB, jsou výhodnější než relační databáze v těchto situacích:

1.  **Flexibilní schéma (nebo žádné schéma):**  Pokud se struktura vašich dat často mění, nebo pokud máte data s různou strukturou, dokumentová databáze je *mnohem* flexibilnější.  Nemusíte provádět složité migrace schématu (jako `ALTER TABLE` v SQL).  Proste přidáte nové pole do dokumentu.
2.  **Denormalizovaná data:**  Pokud máte data, která by v relační databázi vyžadovala složité JOINy přes mnoho tabulek, v dokumentové databázi je můžete uložit *denormalizovaně* do jednoho dokumentu.  To zjednodušuje a zrychluje dotazování.  Příklad:  Uživatel a jeho adresa.  V relační databázi by to byly dvě tabulky.  V dokumentové databázi může být adresa *vnořený dokument* uvnitř dokumentu uživatele.
3.  **Hierarchická data:**  Dokumentové databáze přirozeně reprezentují hierarchická data (např. stromové struktury, JSON data).
4.  **Rychlý vývoj:**  Díky flexibilnímu schématu je vývoj aplikací s dokumentovými databázemi často rychlejší, zejména v agilním prostředí.
5.  **Velký objem dat a vysoká zátěž:**  Dokumentové databáze jsou obvykle *velmi dobře škálovatelné* horizontálně (přidáváním dalších serverů).
6. **Mobilní a offline aplikace:** CouchDB má excelentní support pro synchronizaci, a offline first přístup.

**Příklady, kdy je CouchDB (nebo jiná dokumentová DB) *dobrá* volba:**

*   **Správa obsahu (CMS):**  Stránky, blogové příspěvky, články – každý může mít jinou strukturu.
*   **Katalogy produktů:**  Různé produkty mají různé atributy.
*   **Uživatelské profily:**  Různí uživatelé mohou mít různé informace.
*   **IoT (Internet of Things):**  Data ze senzorů mohou mít různou strukturu.
* **Mobilní aplikace s offline synchronizací**

**Příklady, kdy je CouchDB (nebo jiná dokumentová DB) *špatná* volba:**

*   **Aplikace, které vyžadují silné transakce přes více dokumentů (ACID):**  Např. bankovní aplikace.  Relační databáze jsou v tomto případě lepší.
*   **Aplikace, kde je důležitá relační integrita:**  Pokud potřebujete *vynucovat* integritu vztahů mezi daty (např. že každý produkt musí mít existující kategorii), relační databáze jsou lepší.
* **Aplikace s velmi komplexními relacemi, kde je potřeba joinovat velké množství tabulek**: v takovém případě je lepší použít grafovou DB.


## 2. CouchDB: Praktický Příklad

Tento příklad ukazuje, jak naplnit CouchDB databázi, a detailně se věnuje dotazování pomocí *views* (MapReduce) a *Mango queries* (CouchDB's `_find` API).  Také probereme, kdy je dokumentová databáze *lepší volbou* než relační databáze.

### Struktura

*   **`docker-compose.yml`:** Definuje službu CouchDB.
*   **`data/users.json`:** JSON soubor s ukázkovými daty.

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**
2.  **Otevřete terminál** a přejděte do tohoto adresáře (`02-NoSQL/01-dokumentova-db`).
3.  **Spusťte CouchDB kontejner:**

    ```bash
    docker-compose up -d
    ```

4.  **Otevřete Fauxton:** Otevřete `http://localhost:5984/_utils/` v prohlížeči.
5.  **Přihlaste se:** Použijte `admin` a `password`.
6.  **Vytvořte databázi:** Klikněte na "Create Database", zadejte `mydb`, zvolte "non-partitioned", a klikněte na "Create".

### Import dat

**Spusťte tento příkaz v terminálu (z kořenového adresáře projektu):**

```bash
curl -X POST -H "Content-Type: application/json" -u admin:password http://localhost:5984/mydb/_bulk_docs --data-binary @data.json
```

### Dotazování v CouchDB: Views (MapReduce) a Mango Queries

CouchDB nabízí dva hlavní způsoby dotazování:

*   **Views (MapReduce):**  Tradiční a velmi flexibilní způsob.  Definujete *map* funkci (která vybírá a transformuje data) a volitelně *reduce* funkci (která agreguje výsledky). Views jsou psané v JavaScriptu.  Jsou *předkompilované* a uložené v *design documents*.  Jsou *velmi efektivní* pro předem definované dotazy.
*   **Mango Queries (`_find` API):**  Modernější a deklarativnější způsob dotazování.  Používáte JSON strukturu pro specifikaci filtru, projekce a řazení.  Podobné dotazovacímu jazyku MongoDB.  Mango je často *jednodušší* pro běžné dotazy, ale *méně flexibilní* než views pro složité transformace a agregace.  Mango může používat *buď* existující views, *nebo* si dočasně vytvořit ad-hoc indexy.

#### Views (MapReduce)

**1. Vytvoření View:**

*   V levém menu Fauxtonu, klikněte na `mydb`.
*   Klikněte na `+ New View`.
*   **Design Document:** Nechte `_design/mydesign` (nebo si zvolte jiný název). Design documents jsou speciální dokumenty, které obsahují definice views.
*   **Index Name:** Zadejte jméno view, např. `by_age`.
*   **Map Function:**  Zde napíšete JavaScriptový kód.

    ```javascript
    function (doc) {
      if (doc.age && doc.name) { // Kontrola, že pole existují
        emit(doc.age, doc.name); // Klíč = věk, hodnota = jméno
      }
    }
    ```

    *   `doc`:  Reprezentuje každý dokument v databázi.
    *   `emit(key, value)`:  Tato funkce je *klíčová*.  Pro každý dokument, který splňuje podmínky v `if`, se zavolá `emit`.
        *   První argument (`doc.age`) je *klíč*, podle kterého se bude indexovat.
        *   Druhý argument (`doc.name`) je *hodnota*, která se uloží spolu s klíčem.  Může to být cokoli (nebo `null`, pokud vás hodnota nezajímá).
    *   Tato map funkce vytvoří index, kde klíčem je věk uživatele a hodnotou je jeho jméno.

*   **Reduce Function:**  Nechte prázdné (pro tento příklad).  Reduce funkce se používají pro agregace (např. `_count`, `_sum`, `_stats`).

*   Klikněte na "Create Document and Build Index".

**2. Použití View (Dotazování):**

Jakmile máte view vytvořený, můžete ho použít pro dotazování.  Existují dva hlavní způsoby:

*   **Přes webové rozhraní Fauxton:** Toto je nejjednodušší způsob pro interaktivní zkoumání.
*   **Přes HTTP API (pomocí `curl`):** Toto je způsob, který byste použili ve své *aplikaci*.

**a) Použití View přes Fauxton:**

1.  V levém menu klikněte na název vaší databáze (`mydb`).
2.  V rozevíracím seznamu, kde je standardně "All Documents", vyberte váš view (např. `mydesign/by_age`).  Tím se přepnete z pohledu na všechny dokumenty na pohled definovaný vaším view.
3.  *Ve výchozím stavu* se zobrazí *všechny* záznamy z indexu, které vytvořila vaše `map` funkce (tedy všechny věky a jména).


**b) Použití View přes HTTP API (pomocí `curl`):**

*   **Základní URL:** URL adresa pro přístup k view má tento formát:

    ```
    http://<server>:<port>/<database>/_design/<design_doc>/_view/<view_name>
    ```

    Pro náš příklad (`by_age` view):

    ```
    http://localhost:5984/mydb/_design/mydesign/_view/by_age
    ```

*   **Parametry dotazu:** Parametry se přidávají do URL jako query string (za otazník `?`).

*   **Příklady (pomocí `curl`):**

    *   **Všichni uživatelé (bez filtru, včetně dokumentů):**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true"
        ```

    *   **Uživatelé s věkem *přesně* 25:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&key=25"
        ```

    *   **Uživatelé ve věku 25 až 30 (včetně):**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&startkey=25&endkey=30"
        ```

    *   **Uživatelé starší nebo rovni 25 letům:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&startkey=25"
        ```

    *   **Uživatelé mladší nebo rovni 25 letům:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&endkey=25"
        ```

    *   **Uživatelé starší než 25 let, seřazení sestupně podle věku:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&startkey=26&descending=true"
        ```

    *   **Omezit na prvních 5 výsledků:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&limit=5"
        ```
     * **Vypnout reduce funkci**
       ```bash
       curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/by_age?include_docs=true&reduce=false"
       ```

**3. Příklad: Počet uživatelů v jednotlivých městech (MapReduce s `_count`):**

*   **Map Function:**

    ```javascript
    function (doc) {
      if (doc.address && doc.address.city) {
        emit(doc.address.city, 1); // Klíč = město, hodnota = 1 (pro počítání)
      }
    }
    ```

    *   Tato funkce prochází všechny dokumenty. Pokud dokument obsahuje pole `address` a `address.city`, zavolá `emit` s městem jako klíčem a hodnotou `1`.  Tedy pro každého uživatele z "Anytown" se zavolá `emit("Anytown", 1)`.

*   **Reduce Function:** Zvolte *vestavěnou* funkci `_count`.

*   **Použití (DŮLEŽITÉ - `group=true`):**

    *   **Ve Fauxtonu:**
        1.  Vytvořte view (jak je popsáno výše) s map funkcí a reduce funkcí `_count`.  Pojmenujte ho např. `count_by_city`.
        2.  Přejděte na zobrazení tohoto view (`mydb` -> "All Documents" -> `mydesign/count_by_city`).
        3.  *Musíte zaškrtnout "Reduce"* v "Query Options".  Pokud to neuděláte, uvidíte pouze výsledky `map` funkce, *ne* agregovaný výsledek.

    *   **Pomocí `curl`:**

        ```bash
        curl -X GET -u admin:password "http://localhost:5984/mydb/_design/mydesign/_view/count_by_city?group=true"
        ```

        (Předpokládá se, že jste view pojmenovali `count_by_city` a design document `mydesign`.)

        *   **`group=true`:** Toto je *klíčové*.  Říká CouchDB, aby seskupil výsledky podle klíče (města) a aplikoval reduce funkci (`_count`) na každou skupinu.

    *   **Výsledek (s `group=true`):**

        ```json
        {
          "rows": [
            { "key": "Anytown", "value": 2 },  // 2 uživatelé z Anytown
            { "key": "Neverland", "value": 1 } // 1 uživatel z Neverlandu
          ]
        }
        ```

        Tento výsledek *správně* ukazuje počet uživatelů v každém městě.

    *   **`group_level`:**  Pokud by váš klíč byl pole (např. `emit([doc.address.city, doc.address.street], 1)`), `group_level` by určoval, podle kolika prvků pole se má seskupovat.  Pro tento příklad ho nepotřebujete.


#### Mango Queries (`_find`)

Mango queries jsou *jednodušší* na zápis pro běžné dotazy.

**1. Použití:**

*   V levém menu klikněte na `mydb`.
*   Klikněte na "Query".
*   Zadejte dotaz v JSON formátu.

**Příklady:**

*   **Všichni uživatelé starší 25 let:**

    ```json
    {
      "selector": {
        "age": { "$gt": 25 }
      }
    }
    ```

*   **Uživatelé s hobby "reading":**

    ```json
    {
      "selector": {
        "hobbies": { "$in": ["reading"] }
      }
    }
    ```

*   **Jméno a email uživatelů (projekce):**

    ```json
    {
      "selector": {},
      "fields": ["name", "email"]
    }
    ```

*   **Uživatelé seřazení podle jména sestupně (je třeba vytvořit index):**

    ```json
    {
      "selector": {},
      "sort": [{"name": "desc"}]
    }
    ```
* **Uživatelé začínající na "J"**:
    ```json
    {
        "selector": {
            "name": {"$regex": "^J"}
        }
    }
    ```

*   **Uživatelé, kteří mají definovanou ulici:**

    ```json
    {
        "selector": {
           "address.street": {"$exists": true}
        }
    }
    ```

**2. Vytvoření Mango Indexu (pro optimalizaci):**

*   Klikněte na "Query", pak na "Manage Indexes".
*  Klikněte na "+ Create Index".
*  **Index Name:** nazev indexu.
*   **Index Fields:**  Zadejte pole, která chcete indexovat, *v pořadí, ve kterém je budete používat v dotazech*.  Např. pro dotaz `{"selector": {"age": {"$gt": 25}, "name": "John"}}` by byl vhodný index `[{"age": "asc"}, {"name": "asc"}]`.
*   Klikněte na "Create Index".

**Důležité:**  Pokud nepoužijete existující view nebo nevytvoříte Mango index, CouchDB *může* provést full scan (projít všechny dokumenty), což je *velmi neefektivní* u větších databází. *Vždy vytvářejte indexy pro pole, podle kterých často vyhledáváte.*

### Úkoly

1.  **Prozkoumejte data:**  Prohlédněte si dokumenty v databázi.  Všimněte si, jak je u uživatelů definováno propojeni s příspěvky.

2.  **Základní dotazy (Mango):**
    *   Najděte všechny uživatele starší 28 let.
    *   Najděte uživatele se jménem "John Doe".
    *   Najděte všechny příspěvky (v kolekci `posts`).

3.  **Vytvoření View (MapReduce):**
    *   **`users_by_name`:** Vytvořte view, který indexuje uživatele podle jména (`name`).  Map funkce:

        ```javascript
        function (doc) {
          if (doc.name) {
            emit(doc.name, null);
          }
        }
        ```

    *   **Otestujte view:**  Pomocí `curl` najděte uživatele se jménem "Jane Doe".

4.  **Pokročilejší dotazy (Mango):**
    *  Najděte uživatele s hobby "reading" *a* věkem menším než 35.  Použijte `$and`, `$in`, a `$lt`.
    *   Získejte *pouze* jména a emaily uživatelů (projekce).
    *   Seřaďte uživatele podle věku *sestupně*.
    *   Najděte uživatele, jejichž jméno *nezačíná* na "P" (použijte `$regex` a negaci: `{ "name": { "$not": { "$regex": "^P" } } }`).
    * **Najděte všechny příspěvky od autora "john_doe"**.

5. **Vytvoření Mango Indexů:** Vytvořte indexy pro:
     * Pole `age` v kolekci `users`
     * Pole `name` v kolekci `users`.
     * Pole `author` v kolekci `posts`.

6. **(Pokročilé) Agregace s MapReduce:**
   * Vytvořte view (MapReduce), který spočítá *celkový* počet příspěvků.  (Použijte `_count` reduce funkci.)
   * **(Velmi pokročilé):** Vytvořte view, který spočítá počet příspěvků *pro každého uživatele*.  (Budete muset emitovat ID uživatele jako klíč a pak použít reduce funkci.)

7. **(Diskuze) Kdy byste *nepoužili* CouchDB (nebo jinou dokumentovou databázi) pro tento typ aplikace (správa uživatelů a příspěvků)?**
