# Neo4j Cypher Cheat Sheet

## Základní Pojmy

*   **Uzel (Node):** `(node)` - Reprezentuje entitu.  Zapisuje se do kulatých závorek.
*   **Popisek (Label):** `:Label` - Typ uzlu (např. `:Person`, `:Movie`).  Píše se za dvojtečku.
*   **Hrana (Relationship):** `-[relation]->` - Reprezentuje vztah mezi uzly.  Zapisuje se do hranatých závorek.  Šipka určuje směr.
*   **Typ Hrany (Relationship Type):** `[:TYPE]` - Typ hrany (např. `:ACTED_IN`, `:FRIENDS_WITH`). Píše se za dvojtečku uvnitř hranatých závorek.
*   **Vlastnost (Property):** `{key: value}` -  Klíč-hodnota pár uvnitř složených závorek.  Např. `{name: "Alice", age: 30}`.
*   **Proměnná:** `n`, `m`, `r` -  Označení uzlu, hrany, nebo výsledku, které se dá použít v dalších částech dotazu.

## Základní CRUD Operace

### 1. CREATE - Vytváření Uzlů a Hran

*   **Vytvoření uzlu:**

    ```cypher
    CREATE (n:Person {name: 'John Doe', age: 30})
    RETURN n
    ```
    Vytvoří uzel s popiskem `Person` a vlastnostmi `name` a `age`.
* **Vytvoření uzlu s více labely**
    ```cypher
     CREATE (n:Person:Employee {name: 'John Doe', age: 30})
     RETURN n
     ```
*   **Vytvoření hrany mezi existujícími uzly:**

    ```cypher
    MATCH (a:Person {name: 'John Doe'}), (b:Person {name: 'Alice'})
    CREATE (a)-[:FRIENDS_WITH]->(b)
    RETURN a, b
    ```
    Najde dva uzly podle jména a vytvoří mezi nimi hranu typu `FRIENDS_WITH`.
*   **Vytvoření hrany s vlastnostmi:**

    ```cypher
    MATCH (a:Person {name: 'John Doe'}), (b:Person {name: 'Alice'})
    CREATE (a)-[:FRIENDS_WITH {since: 2020}]->(b)
    RETURN a, b
    ```
*  **Vytvoření uzlů a hrany najednou:**

    ```cypher
    CREATE (a:Person {name: 'John Doe'})-[:WORKS_AT]->(b:Company {name: 'Acme Corp'})
    RETURN a, b
    ```
* **Vytvoření více entit**
    ```cypher
    CREATE (alice:Person {name: 'Alice'}), (bob:Person {name: 'Bob'}), (alice)-[:FRIENDS_WITH]->(bob)
    ```

### 2. MATCH - Vyhledávání Uzlů a Hran (Čtení)

*   **Nalezení všech uzlů s určitým popiskem:**

    ```cypher
    MATCH (n:Person)
    RETURN n
    ```
*   **Nalezení uzlů s určitou vlastností:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    RETURN n
    ```
*   **Nalezení uzlů a jejich vztahů:**

    ```cypher
    MATCH (p:Person)-[:FRIENDS_WITH]->(f:Person)
    RETURN p, f
    ```
    Najde všechny osoby (`Person`) a jejich přátele (`FRIENDS_WITH`).
*   **Filtrování podle vlastností hrany:**

    ```cypher
    MATCH (p:Person)-[r:FRIENDS_WITH {since: 2020}]->(f:Person)
    RETURN p, f, r
    ```
* **Nalezení uzlu bez specifikace labelu:**
   ```cypher
    MATCH (n)
    RETURN n LIMIT 25
   ```
   Vrátí prvních 25 uzlů (jakéhokoliv labelu). `LIMIT` je důležité, jinak by to mohlo vrátit *celou* databázi.
* **Vracení specifických vlastností**
    ```cypher
    MATCH (m:Movie {title: "The Matrix"})
    RETURN m.title, m.released, m.tagline
    ```
* **MATCH s WHERE**
    ```cypher
    MATCH (p:Person)
    WHERE p.age > 30
    RETURN p.name, p.age
    ```
* **MATCH s řetězovými operátory**
    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person)
    RETURN p, m, d
    ```
    Najde herce, filmy, ve kterých hráli, a režiséry těchto filmů.

### 3. RETURN - Vrácení Výsledků

*   **Vrácení celého uzlu:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    RETURN n
    ```
*   **Vrácení konkrétních vlastností:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    RETURN n.name, n.age
    ```
*   **Přejmenování vrácených vlastností (alias):**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    RETURN n.name AS PersonName, n.age AS PersonAge
    ```
*   **Vrácení typu hrany:**

    ```cypher
    MATCH (a)-[r]->(b)
    RETURN type(r)
    ```
*   **Vrácení unikátních výsledků (DISTINCT):**

    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    RETURN DISTINCT p.name
    ```
*   **Vrácení počtu výsledků (COUNT):**

    ```cypher
    MATCH (p:Person)
    RETURN count(p)
    ```
*   **Vrácení s omezením počtu výsledků (LIMIT) a přeskočením (SKIP):**

    ```cypher
    MATCH (n:Person)
    RETURN n
    SKIP 10  // Přeskočí prvních 10
    LIMIT 5   // Vrátí následujících 5
    ```

* **Vrácení uspořádané dle vlastnosti (ORDER BY)**
    ```cypher
    MATCH (p:Person)
    RETURN p.name, p.age
    ORDER BY p.age DESC // Sestupně
    ```

### 4. SET - Aktualizace Vlastností

*   **Změna existující vlastnosti:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n.age = 31
    RETURN n
    ```
*   **Přidání nové vlastnosti:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n.city = 'Prague'
    RETURN n
    ```
*   **Nastavení více vlastností najednou:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n.age = 32, n.city = 'Brno'
    RETURN n
    ```
*   **Nastavení vlastností z mapy (dictionary):**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n += {age: 33, city: 'Ostrava', occupation: 'Engineer'}
    RETURN n
    ```
* **Nastavení labelu**
    ```cypher
     MATCH (n {name: 'John Doe'})
     SET n:Employee
     RETURN n
    ```
*   **Odstranění vlastnosti:**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n.city = null  // Nastaví hodnotu na null, což v Neo4j odstraní vlastnost
    RETURN n
    ```

### 5. DELETE / REMOVE - Mazání

*   **Smazání hrany:**

    ```cypher
    MATCH (a:Person {name: 'John Doe'})-[r:FRIENDS_WITH]->(b:Person {name: 'Alice'})
    DELETE r
    ```
*   **Smazání uzlu (musí být smazány i všechny jeho hrany):**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    DETACH DELETE n
    ```
    `DETACH DELETE` smaže uzel *a* všechny jeho hrany.  Používejte opatrně!
* **Smazání labelu z uzlu:**
    ```cypher
        MATCH (n:Person:Employee {name: 'John Doe'})
        REMOVE n:Employee
        RETURN n
    ```
*   **Odstranění vlastnosti (pomocí `SET` na `null`):**

    ```cypher
    MATCH (n:Person {name: 'John Doe'})
    SET n.age = null
    RETURN n
    ```

### 6. WHERE - Filtrování

*   **Filtrování podle více podmínek:**

    ```cypher
    MATCH (n:Person)
    WHERE n.age > 25 AND n.city = 'Prague'
    RETURN n
    ```
*   **Použití `OR`:**

    ```cypher
    MATCH (n:Person)
    WHERE n.age > 30 OR n.city = 'Brno'
    RETURN n
    ```
*   **Použití `NOT`:**

    ```cypher
    MATCH (n:Person)
    WHERE NOT n.age = 25
    RETURN n
    ```

*   **Filtrování podle existence vlastnosti:**

    ```cypher
    MATCH (n:Person)
    WHERE EXISTS(n.city) // Vlastnost city musí existovat
    RETURN n
    ```

*   **Filtrování podle regulárního výrazu:**

    ```cypher
    MATCH (n:Person)
    WHERE n.name =~ 'J.*'  // Jméno začíná na J
    RETURN n
    ```
* **Filtrování podle existence vztahu**
    ```cypher
    MATCH (p:Person)
    WHERE (p)-[:LIVES_IN]->(:City) // Osoba musí bydlet v nejakem meste
    RETURN p
    ```

### 7. OPTIONAL MATCH

*   **Vrací i uzly, které nemají odpovídající vztah (jako LEFT JOIN v SQL):**

    ```cypher
    MATCH (p:Person)
    OPTIONAL MATCH (p)-[:WORKS_AT]->(c:Company)
    RETURN p.name, c.name AS CompanyName // c.name bude null, pokud osoba nepracuje
    ```

### 8. WITH - Řetězení Dotazů

*   **Používá se pro předání výsledků z jedné části dotazu do další:**

    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WITH p, count(m) AS MoviesActedIn
    WHERE MoviesActedIn > 5
    RETURN p.name, MoviesActedIn
    ```
    Spočítá, kolik filmů každý herec hrál, a pak vybere jen ty, kteří hráli ve více než 5 filmech.
* **WITH a DISTINCT**
    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WITH DISTINCT p
    ORDER BY p.name
    RETURN p.name
    ```
* **WITH a LIMIT / SKIP**
    ```cypher
      MATCH (p:Person)
      WITH p
      ORDER BY p.age DESC
      LIMIT 5
      RETURN p.name, p.age
    ```

### 9. Indexy a Omezení (Constraints)

*   **Vytvoření indexu (pro urychlení vyhledávání):**

    ```cypher
    CREATE INDEX ON :Person(name)
    ```
    Indexuje vlastnost `name` uzlů s popiskem `Person`.
* **Index pro více vlastností**
    ```cypher
    CREATE INDEX ON :Person(name, age)
    ```
    Indexuje kombinaci `name` a `age`
* **Index pro fulltextové vyhledávání**
    ```cypher
    CALL db.index.fulltext.createNodeIndex("movieTitlesAndDescriptions",["Movie"],["title", "description"])
    ```
    Umožňuje dotazy jako:
    ```cypher
    CALL db.index.fulltext.queryNodes("movieTitlesAndDescriptions", "matrix reloaded") YIELD node, score
    RETURN node.title, score
    ```
*   **Vytvoření omezení (constraint) - unikátnost:**

    ```cypher
    CREATE CONSTRAINT ON (p:Person) ASSERT p.email IS UNIQUE
    ```
    Zajišťuje, že vlastnost `email` je unikátní pro všechny uzly s popiskem `Person`.  Vytvoří také index automaticky.
*   **Vytvoření omezení (constraint) - existence:**

    ```cypher
    CREATE CONSTRAINT ON (b:Book) ASSERT EXISTS (b.isbn)
    ```
    Zajišťuje, že všechny uzly `Book` *musí* mít vlastnost `isbn`.
* **Omezení na typ nodu**
    ```cypher
    CREATE CONSTRAINT ON (p:Person) ASSERT (p.name, p.age) IS NODE KEY
    ```
    Zajišťuje že kombinace vlastností `name` a `age` identifikuje node.
* **Omezení na existenci relace**
    ```cypher
    CREATE CONSTRAINT ON ()-[r:LIKES]-() ASSERT EXISTS (r.since)
    ```
*   **Zobrazení indexů a omezení:**

    ```cypher
    SHOW INDEXES
    SHOW CONSTRAINTS
    ```

*  **Smazání indexu**
    ```cypher
     DROP INDEX ON :Person(name)
    ```
*  **Smazání constraintu**
    ```cypher
    DROP CONSTRAINT ON (p:Person) ASSERT p.email IS UNIQUE
    ```
### 10. Funkce

*   **`count()`:**  Počet.

    ```cypher
    MATCH (p:Person)
    RETURN count(p)
    ```

*   **`collect()`:**  Vytvoří seznam.

    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    RETURN p.name, collect(m.title) AS Movies
    ```

*   **`shortestPath()`:**  Nejkratší cesta.

    ```cypher
    MATCH (a:Person {name: 'Keanu Reeves'}), (b:Person {name: 'Tom Hanks'})
    MATCH p=shortestPath((a)-[*]-(b))
    RETURN p
    ```

*   **`nodes()`, `relationships()`:**  Vrátí seznam uzlů/hran v cestě.

    ```cypher
    MATCH p=(a:Person {name: 'Keanu Reeves'})-[*]-(b:Person {name: 'Tom Hanks'})
    RETURN nodes(p), relationships(p)
    ```

*   **`coalesce()`:**  Vrátí první non-null hodnotu.

    ```cypher
    MATCH (p:Person)
    RETURN coalesce(p.nickname, p.name, 'No Name') // Vrátí přezdívku, jméno, nebo "No Name"
    ```
*   **Řetězcové funkce:** `toLower()`, `toUpper()`, `trim()`, `replace()`, `substring()`, `split()`.
* **Matematické funkce:**  `abs()`, `ceil()`, `floor()`, `round()`, `sqrt()`, `rand()` a další.

*  **Predikátové funkce:**  `exists()`, `all()`, `any()`, `none()`, `single()`.  Tyto se používají uvnitř `WHERE` nebo `CASE`.
    ```cypher
        MATCH (p:Person)
        WHERE all(x IN p.interests WHERE x STARTS WITH 'Neo4j') //Vsechny zájmy začínají na Neo4j
        RETURN p
    ```

### 11. CASE - Podmíněné Výrazy

*   **Podobné `switch` nebo `if-else` v jiných jazycích (pokračování):**

    ```cypher
    MATCH (n)
    RETURN n.name,
           CASE n.age
               WHEN 20 THEN 'Twenty'
               WHEN 30 THEN 'Thirty'
               ELSE 'Other Age'
           END AS AgeCategory
    ```

    Tento příklad vrací jméno uzlu a kategorizuje věk.  `END` je povinné.

*   **`CASE` s obecnými výrazy:**

    ```cypher
    MATCH (n:Person)
    RETURN n.name,
           CASE
               WHEN n.age < 18 THEN 'Minor'
               WHEN n.age >= 18 AND n.age < 65 THEN 'Adult'
               ELSE 'Senior'
           END AS AgeGroup
    ```

    Zde se nepoužívá `CASE n.age`, ale `CASE` samotné, a jednotlivé `WHEN` klauzule obsahují kompletní podmínky.

*   **`CASE` uvnitř `WHERE`:**

    ```cypher
    MATCH (n:Person)
    WHERE
      CASE
        WHEN n.city = 'Prague' THEN n.age > 20
        ELSE n.age > 25
      END
    RETURN n.name, n.age, n.city
    ```
    Filtruje osoby starší 20 let z Prahy, a osoby starší 25 let z ostatních měst.

*  **`CASE` s `coalesce()`:**

    ```cypher
    MATCH (n:Person)
    RETURN n.name,
           CASE
               WHEN n.nickname IS NOT NULL THEN n.nickname
               ELSE n.name
           END AS DisplayName
    ```
    Je ekvivalentní:
    ```cypher
      MATCH (n:Person)
      RETURN n.name, coalesce(n.nickname, n.name) AS DisplayName
    ```

### 12. UNWIND - Rozbalení Seznamů

*   **Transformuje seznam na řádky:**

    ```cypher
    WITH [1, 2, 3, null, 4] AS numbers
    UNWIND numbers AS number
    RETURN number
    ```

    Výsledek:

    ```
    number
    ------
    1
    2
    3
    null
    4
    ```
* **`UNWIND` s `collect()`**
    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WITH p, collect(m.title) AS movies
    UNWIND movies AS movieTitle
    RETURN p.name, movieTitle
    ```
    Zobrazí jména herců a *každý* film, ve kterém hráli, na samostatném řádku.
*   **`UNWIND` s prázdným seznamem:**
  Pokud je seznam prázdný, `UNWIND` *odstraní* řádek z výsledků.  To se dá kombinovat s `OPTIONAL MATCH`:

    ```cypher
    MATCH (p:Person)
    OPTIONAL MATCH (p)-[:HAS_HOBBY]->(h:Hobby)
    WITH p, collect(h.name) AS hobbies
    UNWIND (CASE WHEN size(hobbies) = 0 THEN [null] ELSE hobbies END) AS hobby  // Důležitý trik!
    RETURN p.name, hobby
    ```

    Tento *důležitý trik* zajistí, že se zobrazí i osoby bez koníčků (s `hobby = null`).  Bez něj by se osoby bez koníčků nezobrazily vůbec.

### 13. UNION / UNION ALL - Spojení Výsledků

*   **`UNION` - Odstraní duplicity:**

    ```cypher
    MATCH (n:Person {city: 'Prague'})
    RETURN n.name AS Name
    UNION
    MATCH (m:Movie {city: 'Prague'}) // Předpokládejme, že i filmy mají vlastnost city.
    RETURN m.title AS Name
    ```

    Vrátí jména osob *a* názvy filmů z Prahy, bez duplicit.  Sloupce se musí jmenovat stejně (zde `Name`).
* **UNION ALL neodstraňuje duplicity**

### 14. CALL { ... } - Subdotazy (od Neo4j 4.0)

*   **Umožňuje složitější logiku a oddělení částí dotazu:**

    ```cypher
    MATCH (p:Person)
    CALL {
        WITH p
        MATCH (p)-[:FRIENDS_WITH]->(f:Person)
        RETURN count(f) AS FriendCount
    }
    RETURN p.name, FriendCount
    ```
    Spočítá počet přátel pro každou osobu.  `WITH p` je *nutné* pro předání proměnné `p` do subdotazu.

*   **Subdotazy s importem proměnných:**

    ```cypher
     MATCH (m:Movie)
     CALL {
       WITH m
       MATCH (m)<-[:ACTED_IN]-(a:Person)
       RETURN a
       ORDER BY a.name
       LIMIT 3
     }
     RETURN m.title, collect(a.name) AS Top3Actors
    ```
    Vrátí název filmu a jména prvních 3 herců (podle abecedy).

*   **Subdotazy s `UNION`:**

    ```cypher
    MATCH (p:Person)
    CALL {
      WITH p
      MATCH (p)-[:LIVES_IN]->(c:City)
      RETURN c.name AS Location, 'City' AS Type
      UNION
      WITH p
      MATCH (p)-[:WORKS_AT]->(co:Company)
      RETURN co.name AS Location, 'Company' AS Type
    }
    RETURN p.name, Location, Type
    ```

### 15. CALL ... YIELD - Volání Procedur

*   **Neo4j má vestavěné procedury, a je možné psát vlastní (v Javě).**

*   **`apoc.*` (Awesome Procedures on Cypher) - Velmi užitečná knihovna procedur (musí být nainstalována).**

    ```cypher
    // Příklad: apoc.load.json - načtení dat z JSON URL
    CALL apoc.load.json("https://example.com/data.json") YIELD value
    RETURN value
    ```

    ```cypher
    //Příklad: apoc.create.nodes vytvoření vice nodů najednou
    CALL apoc.create.nodes(['Person', 'Actor'], [{name: 'Keanu Reeves'}, {name: 'Carrie-Anne Moss'}])
    ```

    ```cypher
    //Příklad: apoc.create.relationship - vytvoření relace
    MATCH (keanu:Person {name: 'Keanu Reeves'}),(carrie:Person {name: 'Carrie-Anne Moss'})
    CALL apoc.create.relationship(keanu, 'FRIENDS_WITH', {}, carrie) YIELD rel
    RETURN rel
    ```
*   **`db.*` - Procedury pro správu databáze.**

    ```cypher
    CALL db.labels() YIELD label // Seznam všech labelů
    ```

    ```cypher
    CALL db.relationshipTypes() YIELD relationshipType // Seznam všech typů relací
    ```

### 16. Práce s Datumy a Časy

*   **Neo4j má datové typy `Date`, `DateTime`, `Time`, `LocalTime`, `LocalDateTime`.**

*   **Funkce pro vytvoření:** `date()`, `datetime()`, `time()`, `localtime()`, `localdatetime()`.

    ```cypher
    RETURN date("2024-07-24") // Datum
    RETURN datetime("2024-07-24T19:32:24+02:00") // Datum a čas s časovou zónou
    ```

*   **Funkce pro extrakci částí:** `date.year`, `date.month`, `date.day`, `datetime.hour`, `datetime.minute`, `datetime.second`, atd.

*   **Funkce pro výpočty:** `date.diff` (pro rozdíl mezi datumy).

    ```cypher
     MATCH (p:Person)
     WHERE date.diff(date({year:p.birthYear, month: p.birthMonth, day:p.birthDay}),date()).years  > 18 // Osoby starší 18 let.
     RETURN p
    ```

*   **Formátování:** `apoc.date.format` (z APOC knihovny).

### 17. Import Dat

*   **`LOAD CSV` - Import z CSV souborů:**

    ```cypher
    LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
    CREATE (:Person {name: row.name, age: toInteger(row.age)})
    ```
    *  `file:///` pro lokální soubory (musí být v import adresáři Neo4j, viz konfigurace).
    *  `https://...` pro soubory na webu.
    *  `WITH HEADERS` - první řádek je hlavička.
    *  `AS row` - každý řádek je dostupný jako mapa `row`.
    *  `toInteger()`, `toFloat()`, `toString()` - konverze typů.

* **`apoc.load.json` a `apoc.load.jsonParams`** - Import z JSON (z APOC).
* **`neo4j-admin import`** - Nástroj pro rychlý import *velkých* CSV souborů (při inicializaci databáze).

### 18. Tipy a Triky

*   **Profilování dotazů:**  Použijte `PROFILE` před dotazem (v Neo4j Browseru) pro zobrazení plánu provádění a identifikaci úzkých míst.

    ```cypher
    PROFILE
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    RETURN p, m
    ```

*   **`EXPLAIN`:** Podobné jako `PROFILE`, ale neprovede dotaz, jen zobrazí plán.

* **Používejte parametry:** Místo vkládání hodnot přímo do dotazu, používejte parametry.  Zvyšuje to bezpečnost a umožňuje znovupoužití plánu provádění.

    ```cypher
    // Špatně:
    MATCH (p:Person {name: 'Alice'}) RETURN p

    // Správně:
    MATCH (p:Person {name: $name}) RETURN p
    // A pak předat parametr {name: 'Alice'}
    ```

    V Neo4j Browseru můžete parametry zadat pomocí `:param name => 'Alice'`. V programovacích jazycích se parametry předávají obvykle jako součást volání databázového driveru.

*   **Komentáře:**

    ```cypher
    // Jednořádkový komentář

    /*
     Víceřádkový
     komentář
    */
    ```
* **Doporučení ohledně labelů:**
    *   Používejte CamelCase (např. `Movie`, `PersonOfInterest`).
    *   Vyhněte se mezerám a speciálním znakům v labelech a typech relací.
* **Doporuceni ohledně relací**
    *  Používejte UPPER_SNAKE_CASE (např. `ACTED_IN`, `FRIENDS_WITH`).
* **Doporučení ohledně properties**
     * používejte  camelCase (napr. `firstName`, `lastName`).
