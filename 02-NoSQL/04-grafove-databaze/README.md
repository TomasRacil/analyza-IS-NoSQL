# Grafové Databáze

## 1. Grafové Databáze: Teorie

### 1.1 Datový Model

Grafové databáze ukládají data ve formě *grafu*. Graf se skládá z *uzlů* (nodes) a *hran* (relationships/edges), které uzly propojují.  Uzly i hrany mohou mít *vlastnosti* (properties).

*   **Uzly (Nodes):**  Reprezentují entity, např. osoby, produkty, místa.  Uzly mají *popisky* (labels), které určují jejich typ (např. `Person`, `Product`, `City`).
*   **Hrany (Relationships/Edges):**  Reprezentují vztahy mezi uzly.  Hrany mají *typ* (např. `FRIENDS_WITH`, `PURCHASED`, `LOCATED_IN`) a *směr*.  Hrany *nemusí* být obousměrné.
*   **Vlastnosti (Properties):**  Klíč-hodnota páry, které uchovávají informace o uzlech a hranách (např. jméno osoby, cena produktu, datum nákupu).

**Příklad (konceptuální):**

```
(alice:Person {name: "Alice", age: 30})
(bob:Person {name: "Bob", age: 25})
(carol:Person {name: "Carol", age: 35})

(alice)-[:FRIENDS_WITH]->(bob)
(bob)-[:FRIENDS_WITH]->(carol)
(alice)-[:LIVES_IN]->(prague:City {name: "Prague"})
(bob)-[:WORKS_AT]->(company:Company {name: "Acme Corp"})
(carol)-[:PURCHASED {date: "2023-11-15"}]->(product:Product {name: "Laptop", price: 1200})
```

*   `alice`, `bob`, `carol`, `prague`, `company`, `product` jsou *uzly*.
*   `Person`, `City`, `Company`, `Product` jsou *popisky* uzlů.
*   `name`, `age`, `date`, `price` jsou *vlastnosti*.
*   `FRIENDS_WITH`, `LIVES_IN`, `WORKS_AT`, `PURCHASED` jsou *typy* hran.
* Šipky ukazují *směr* hrany.

**Klíčové vlastnosti grafového modelu:**

*   **Přirozené modelování vztahů:**  Velmi intuitivní pro reprezentaci vztahů mezi entitami.
*   **Vysoký výkon pro dotazy procházející graf:**  Dotazy, které sledují vztahy mezi uzly (např. "najdi všechny přátele přátel Alice"), jsou velmi rychlé.
*   **Flexibilní schéma:**  Není nutné definovat všechny typy uzlů, hran a vlastností předem.
*   **Snadná vizualizace:**  Grafy se dají snadno vizualizovat, což pomáhá pochopit strukturu dat.

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Vysoký výkon pro komplexní dotazy na vztahy:**  Ideální pro sociální sítě, doporučovací systémy, detekci podvodů, atd.
*   **Intuitivní modelování dat:**  Snadno se mapuje na reálný svět.
*   **Flexibilita:**  Schéma se dá snadno rozšiřovat.
*   **Agilní vývoj:**  Rychlý vývoj prototypů a iterativní vývoj.
*   **Dobrá škálovatelnost (u některých grafových databází).**

**Nevýhody:**

*   **Méně vhodné pro jednoduché agregace přes celý dataset:**  Agregace (např. `SUM`, `AVG`) přes všechny uzly *určitého typu* mohou být pomalejší než v relačních nebo sloupcových databázích. (Záleží na konkrétní implementaci a typu dotazu.)
*   **Někdy složitější dotazovací jazyk:**  Cypher (pro Neo4j) je sice relativně snadný, ale může být složitější než SQL pro *některé* typy dotazů.
*   **Menší rozšířenost (oproti relačním databázím).**
*  **Omezená podpora transakcí (ACID) v některých grafových databázích.** Neo4j podporuje ACID transakce.
*  **Některé grafové databáze nemají tak dobrou horizontální škálovatelnost jako např. Cassandra.**

### 1.3 Příklady Grafových Databází

*   **Neo4j:**  Nejpopulárnější grafová databáze.  Používá dotazovací jazyk Cypher.  Dobrá volba pro většinu grafových aplikací.  Podporuje ACID transakce.
*   **Amazon Neptune:**  Plně spravovaná grafová databáze na AWS.  Podporuje RDF/SPARQL a Gremlin.
*   **ArangoDB:**  Multi-model databáze (podporuje grafy, dokumenty a key-value).  Používá AQL (ArangoDB Query Language).
*   **JanusGraph:**  Open-source, distribuovaná grafová databáze.  Může používat různé backendy (např. Cassandra, HBase, Bigtable).
* **Microsoft Azure Cosmos DB:** (s Gremlin API) multi-model databáze která podporuje mimo jiné i Grafový model
* **TigerGraph:** grafová databáze která se prezentuje jako velmi výkonné řešení vhodné pro enterprise.

### 1.4 Kdy je grafová databáze lepší volbou než relační?

*   **Aplikace s komplexními vztahy mezi daty:**  Kde jsou vztahy *stejně důležité* (nebo *důležitější*) než samotné entity.
*   **Sociální sítě:**  Modelování vztahů mezi uživateli, skupinami, příspěvky.
*   **Doporučovací systémy:**  Doporučování produktů, obsahu, přátel na základě vztahů.
*   **Detekce podvodů:**  Odhalování podezřelých vzorců chování v síti transakcí.
*   **Správa znalostí (Knowledge Graphs):**  Ukládání a propojování informací z různých zdrojů.
*   **Řízení přístupu (Access Control):**  Modelování hierarchií oprávnění a rolí.
*   **Sítě (např. dopravní, telekomunikační):**  Modelování a optimalizace sítí.
* **Bioinformatika** modelování genových interakcí a proteinových struktur
* **Kdy se grafová databáze nehodí**:
    *   Pokud nepotřebujete složité dotazy přes vztahy, a jde vám primárně o jednoduché CRUD operace (create, read, update, delete) nad jednotlivými entitami.
    *   Pokud potřebujete silné ACID transakce přes *velké množství* uzlů a hran (Neo4j podporuje ACID, ale s určitými omezeními při distribuovaném provozu).
    *   Pokud potřebujete primárně agregovat data přes *velký počet* uzlů (např. spočítat průměrný věk všech uživatelů). V tomto případě by mohla být lepší sloupcová databáze.

## 2. Neo4j: Praktický Příklad s Neo4j Browserem

Tento příklad ukazuje, jak používat Neo4j Browser a jeho vestavěné interaktivní tutoriály.

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**

2.  **Otevřete terminál** a přejděte do adresáře s `docker-compose.yml`.

3.  **Spusťte kontejner:**

    ```bash
    docker-compose up -d
    ```

### 2.1 Neo4j Browser a Interaktivní Průvodci

1.  **Otevřete Neo4j Browser:**  V prohlížeči přejděte na adresu `http://localhost:7474`.

2.  **Přihlášení:**  Přihlaste se pomocí uživatelského jména `neo4j` a hesla `neo4j`. Budete vyzváni ke změně hesla po prvním přihlášení.

3.  **Prozkoumejte úvodní obrazovku:** Neo4j Browser má interaktivní úvodní obrazovku s několika sekcemi:

    *   **Learn:**  Obsahuje odkazy na dokumentaci, tutoriály a další zdroje.
    *   **Query:**  Zde píšete a spouštíte Cypher dotazy.  Výsledky se zobrazují vizuálně i v tabulkové podobě.
    *   **Style:**  Umožňuje upravit vzhled vizualizace grafu (barvy, velikosti uzlů, atd.).
    *   **Settings:**  Nastavení připojení k databázi a další konfigurace.
    *   **Information Panel (ikona "i" vlevo):**  Zobrazuje informace o aktuálně vybraném uzlu nebo hraně.

4.  **Interaktivní průvodce "Movie Database":**

    *   V horní části okna prohlížeče, v sekci pro psaní dotazů, začněte psát `:play`.
    *   Měla by se vám zobrazit nabídka s několika průvodci.  Vyberte **"Movie Database"** (nebo "Movies").  Tím se spustí interaktivní průvodce.
    *   Průvodce vás krok za krokem provede:
        *   **Načtením datové sady "Movies".**  Průvodce obsahuje Cypher příkazy, které vytvoří uzly pro filmy, herce, režiséry a vztahy mezi nimi.  Stačí kliknout na tlačítko "Play" (trojúhelníček) u každého příkazu.
        *   **Základními dotazy v Cypheru.**  Průvodce obsahuje příklady dotazů, které můžete spustit a upravovat.  Uvidíte, jak se data vizualizují.
        *   **Pokročilejšími dotazy.**  Průvodce ukazuje, jak filtrovat data, používat agregace, a procházet graf.

5. **Další průvodci:** Neo4j Browser obsahuje i další průvodce (např. "Northwind" pro ukázku obchodních dat). Můžete je prozkoumat stejným způsobem (pomocí `:play`).

6. **Vlastní dotazy:**  Po dokončení průvodců (nebo i během nich) můžete začít psát vlastní Cypher dotazy do okna prohlížeče.  Experimentujte s různými dotazy a sledujte, jak se vizualizují.

**Příklady dotazů (které najdete i v průvodci "Movie Database"):**

*   **Najít všechny filmy:**

    ```cypher
    MATCH (m:Movie)
    RETURN m
    ```

*   **Najít film "The Matrix":**

    ```cypher
    MATCH (m:Movie {title: "The Matrix"})
    RETURN m
    ```

*   **Najít herce, kteří hráli ve filmu "The Matrix":**

    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie {title: "The Matrix"})
    RETURN p
    ```

*   **Najít filmy, které režíroval Tom Tykwer:**
    ```cypher
    MATCH (m:Movie)<-[:DIRECTED]-(p:Person {name: "Tom Tykwer"})
    RETURN m.title
    ```

*   **Najít všechny herce a filmy, ve kterých hráli:**

    ```cypher
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    RETURN p.name, m.title
    ```

* **Doporučení filmů: Najdi filmy ve kterých hrali herci co hráli ve filmu "The Matrix":**

    ```cypher
    MATCH (m:Movie {title: "The Matrix"})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(rec:Movie)
    RETURN rec.title
    ```
* **Doporučení filmů: Pro uživatele co jimž se líbil film "The Matrix", najdi filmy co se líbili jiným uživatelům se stejným vkusem:**

    ```cypher
    MATCH (m:Movie {title: 'The Matrix'})<-[:RATED]-(u1:User)-[:RATED]->(rec:Movie)<-[:RATED]-(u2:User)
    WHERE u1 <> u2
    RETURN rec.title
    ```
    Tento příklad je umělý protože databáze Movie neobsahuje data o uživatelích. Je ale dobrý pro demonstraci.


### Úkoly

1.  **Projděte si interaktivní průvodce "Movie Database"** v Neo4j Browseru. Spouštějte všechny příkazy a snažte se pochopit, co dělají.  Upravujte dotazy a sledujte, jak se mění výsledky.

2.  **Prozkoumejte další průvodce,** pokud vás zajímají (např. "Northwind").

3.  **Vyzkoušejte si následující dotazy (a upravujte je):**
    *   Najděte všechny filmy vydané po roce 2000.
    *   Najděte všechny režiséry a spočítejte, kolik filmů každý z nich režíroval (použijte `count()`).
    *   Najděte všechny filmy, ve kterých hrál Keanu Reeves.
    *   Najděte všechny herce, kteří hráli ve více než 5 filmech.
    *   Najděte všechny filmy, které mají v názvu slovo "The".

4.  **Vytvořte si vlastní data:**
    *   Vytvořte několik uzlů reprezentujících *vás* a vaše *přátele*.  Přidejte jim vlastnosti (např. jméno, věk, město).
    *   Vytvořte hrany reprezentující vztahy mezi vámi a vašimi přáteli (např. `FRIENDS_WITH`, `STUDIED_WITH`).
    *   Vytvořte dotazy, které:
        *   Najdou všechny vaše přátele.
        *   Najdou všechny lidi, kteří bydlí ve stejném městě jako vy.
        *   Najdou všechny přátele vašich přátel (ale ne vás).

5.  **Vyzkoušej si indexy a constraints,** které byly popsány v teoretické části.

6. **Složitejší dotazy:**

    *   Najděte nejkratší cestu mezi dvěma herci (např. mezi Keanu Reevesem a Tomem Hanksem).  Neo4j má funkce pro hledání nejkratších cest (`shortestPath`).
    *   Napište doporučovací systém, který doporučí filmy na základě toho, co se líbilo lidem, kterým se líbily stejné filmy jako vám.

7.  **Diskuze:**  Porovnejte Neo4j s relační databází.  V jakých situacích byste použili Neo4j a v jakých relační databázi?  Jaké jsou výhody a nevýhody grafových databází?

8.  **Co dál?:** Pokud vás grafová databáze zaujala můžete si projít další příklady [zde](https://neo4j.com/docs/getting-started/appendix/example-data/).
