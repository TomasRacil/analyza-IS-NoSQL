# Prostorové Databáze (Spatial Databases)

## 1. Prostorové Databáze: Teorie

### 1.1 Datový Model

Prostorové databáze (Spatial Databases) jsou databáze optimalizované pro ukládání a dotazování se na data, která reprezentují objekty definované v geometrickém prostoru.  Tyto objekty mohou být jednoduché geometrické tvary (body, linie, polygony) nebo složitější struktury (multibody, kolekce geometrických tvarů).  Klíčový rozdíl oproti běžným databázím je schopnost prostorových databází *indexovat* prostorová data a provádět *prostorové operace*.

**Základní pojmy:**

*   **Geometrický datový typ (Geometry):** Základní datový typ pro reprezentaci prostorových objektů.  Definuje *tvar* objektu. Nejčastější geometrické typy jsou:
    *   **POINT (Bod):**  Reprezentuje jeden bod v prostoru, definovaný souřadnicemi (např. X, Y, případně Z pro 3D).
    *   **LINESTRING (Linie, Lomená čára):**  Reprezentuje posloupnost bodů spojených úsečkami.
    *   **POLYGON (Polygon):**  Reprezentuje uzavřenou oblast vymezenou linií (může obsahovat díry).
    *   **MULTIPOINT:**  Kolekce bodů.
    *   **MULTILINESTRING:**  Kolekce linií.
    *   **MULTIPOLYGON:**  Kolekce polygonů.
    *   **GEOMETRYCOLLECTION:**  Heterogenní kolekce geometrických objektů (může obsahovat body, linie, polygony atd.).
*   **Prostorové referenční systémy (SRS/SRID):**  Určují *souřadnicový systém* a *projekci*, ve kterých jsou geometrické objekty definovány.  SRID (Spatial Reference Identifier) je *číselný identifikátor* SRS.  Různé SRS používají různé jednotky (metry, stupně) a různé projekce (např. Mercator, UTM).  Správná interpretace geometrických dat *vyžaduje* znalost SRS.
    *   **EPSG kódy:**  Běžně používané SRIDy jsou definovány organizací EPSG (European Petroleum Survey Group). Např. EPSG:4326 je WGS 84 (používaný GPS), EPSG:3857 je Web Mercator (používaný webovými mapami).
    *   **WGS 84 (World Geodetic System 1984):**  Standardní geografický souřadnicový systém používaný GPS.  Používá zeměpisnou šířku a délku (v stupních).
*   **Prostorové indexy:**  Datové struktury, které umožňují *rychlé* vyhledávání prostorových objektů.  Bez prostorových indexů by prostorové dotazy (např. "najdi všechny objekty v daném okruhu") byly velmi pomalé. Nejčastější typy prostorových indexů jsou:
    *   **R-strom (R-tree):**  Vyvážený strom, který organizuje prostorové objekty do hierarchie obdélníků (bounding boxes). Velmi efektivní pro různé typy prostorových dotazů.
    *   **Quadtree:**  Stromová struktura, která rekurzivně dělí prostor na čtyři kvadranty.
    * **GeoHash:** Převede 2D souřadnice do textového řetězce.
*   **Prostorové operace (Spatial Operations/Functions):**  Funkce, které provádějí operace nad geometrickými objekty.  Tyto operace jsou *klíčovou* vlastností prostorových databází. Příklady:
    *   **ST_Contains(geometry1, geometry2):**  Vrací true, pokud geometry1 *obsahuje* geometry2.
    *   **ST_Intersects(geometry1, geometry2):**  Vrací true, pokud se geometry1 a geometry2 *protínají*.
    *   **ST_DWithin(geometry1, geometry2, distance):**  Vrací true, pokud jsou geometry1 a geometry2 v dané *vzdálenosti*.
    *   **ST_Distance(geometry1, geometry2):**  Vypočítá *vzdálenost* mezi geometry1 a geometry2.
    *   **ST_Area(geometry):**  Vypočítá *plochu* polygonu.
    *   **ST_Length(geometry):**  Vypočítá *délku* linie.
    *   **ST_Centroid(geometry):**  Vypočítá *těžiště* (centroid) geometrie.
    *   **ST_Buffer(geometry, distance):**  Vytvoří *obalovou zónu* (buffer) kolem geometrie.
    *   **ST_Intersection(geometry1, geometry2):** Vypočítá *průnik* dvou geometrií.
    *   **ST_Union(geometry1, geometry2):**  Vypočítá *sjednocení* dvou geometrií.
    *   **ST_Transform(geometry, SRID):**  *Transformuje* geometrii do jiného SRS.
*   **OGC Simple Features:** Standard definovaný Open Geospatial Consortium (OGC), který specifikuje společný model pro reprezentaci a práci s prostorovými daty. Většina prostorových databází dodržuje tento standard.
* **WKT (Well-Known Text):** Textový formát pro reprezentaci geometrických objektů (součást OGC Simple Features). Příklad: `POINT(10 20)`
* **WKB (Well-Known Binary):** Binární formát pro reprezentaci geometrických objektů (součást OGC Simple Features). Efektivnější než WKT.
* **GeoJSON:** Populární formát pro reprezentaci geometrických objektů založený na JSON.

**Příklad (konceptuální):**

```
Table: restaurants
  Column: id (INTEGER, PRIMARY KEY)
  Column: name (TEXT)
  Column: location (GEOMETRY(POINT, 4326)) -- Bod, WGS 84
  Column: address (TEXT)

Data:
  (1, 'Restaurant A', ST_GeomFromText('POINT(-73.9857 40.7484)', 4326), '123 Main St')
  (2, 'Restaurant B', ST_GeomFromText('POINT(-73.9910 40.7577)', 4326), '456 Elm St')

Prostorový dotaz:
  "Najdi všechny restaurace do 5 km od bodu (-73.99, 40.75)"

SQL dotaz:
  SELECT name, address
  FROM restaurants
  WHERE ST_DWithin(location, ST_GeomFromText('POINT(-73.99 40.75)', 4326), 5000);
```

*   `restaurants` je tabulka.
*   `location` je sloupec typu `GEOMETRY`, který ukládá polohu restaurace (bod) v souřadnicovém systému WGS 84 (SRID 4326).
*   `ST_GeomFromText` je funkce, která vytváří geometrický objekt z WKT reprezentace.
*   `ST_DWithin` je prostorová funkce, která testuje, zda jsou dva geometrické objekty v dané vzdálenosti (v tomto případě 5000 metrů).

**Klíčové vlastnosti prostorového modelu:**

*   **Geometrické datové typy:**  Umožňují ukládat prostorová data (body, linie, polygony atd.).
*   **Prostorové referenční systémy:**  Zajišťují správnou interpretaci souřadnic.
*   **Prostorové indexy:**  Umožňují rychlé prostorové dotazy.
*   **Prostorové operace:**  Poskytují funkce pro analýzu a manipulaci s prostorovými daty.
*   **Standardizace (OGC):**  Zajišťuje interoperabilitu mezi různými prostorovými databázemi.

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Efektivní ukládání a dotazování se na prostorová data:**  Optimalizováno pro práci s geometriemi.
*   **Prostorové indexy:**  Rychlé vyhledávání objektů v prostoru.
*   **Prostorové operace:**  Bohatá sada funkcí pro analýzu prostorových vztahů (průniky, vzdálenosti, obalové zóny atd.).
*   **Integrace s GIS (Geographic Information Systems):**  Prostorové databáze jsou základním kamenem GIS aplikací.
*   **Škálovatelnost:**  Mnoho prostorových databází je navrženo pro distribuované prostředí.

**Nevýhody:**

*   **Složitější modelování dat:**  Vyžaduje znalost prostorových konceptů (geometrie, SRS).
*   **Vyšší nároky na zdroje:**  Prostorové indexy a operace mohou být náročné na výpočetní výkon a paměť.
*   **Omezená podpora v některých běžných databázích:**  Ne všechny databáze mají plnohodnotnou podporu prostorových dat.

### 1.3 Příklady Prostorových Databází

*   **PostGIS:**  Nejpopulárnější *open-source* prostorové rozšíření pro PostgreSQL.  Poskytuje plnou podporu OGC Simple Features, bohatou sadu prostorových funkcí a výkonné prostorové indexy (R-strom).
*   **Oracle Spatial:**  Prostorové rozšíření pro Oracle Database.
*   **SQL Server Spatial:**  Prostorové rozšíření pro Microsoft SQL Server.
*   **MySQL:**  Má *základní* podporu prostorových dat (geometrické typy a *některé* prostorové funkce), ale *nemá* plnohodnotné prostorové indexy (pouze R-stromy pro MyISAM, ne pro InnoDB).  Pro vážnější prostorové aplikace se doporučuje PostGIS.
*   **MongoDB:**  NoSQL dokumentová databáze s podporou GeoJSON a *některých* prostorových dotazů (2dsphere index).
*  **SpatiaLite:** Prostorové rozšíření pro SQLite

### 1.4 Kdy je prostorová databáze lepší volbou než běžná databáze?

*   **Ukládání a analýza prostorových dat:**  Pokud vaše aplikace pracuje s geografickými daty (mapy, polohy, trasy, oblasti), prostorová databáze je nezbytná.
*   **Prostorové dotazy:**  Pokud potřebujete provádět dotazy typu "najdi všechny objekty v daném okruhu", "zjisti, zda se dva objekty protínají", "vypočítej vzdálenost mezi dvěma body" atd.
*   **GIS aplikace:**  Prostorové databáze jsou základem GIS aplikací (mapové servery, navigace, analýza prostorových dat).
*   **Logistika a doprava:**  Plánování tras, optimalizace dopravy, sledování vozidel.
*   **Realitní trh:**  Vyhledávání nemovitostí v dané lokalitě, analýza cenových map.
*   **Životní prostředí:**  Modelování šíření znečištění, analýza lesních porostů, sledování pohybu zvířat.
* **Telekomunikace:** Plánování sítí, optimalizace pokrytí signálem.
* **Urbanismus:** Plánování městské zástavby, analýza dopravní infrastruktury.

**Kdy prostorová databáze *není* nutná:**

*   **Pokud pracujete pouze s jednoduchými souřadnicemi (X, Y) a nepotřebujete provádět složité prostorové operace.**  V takovém případě může stačit běžná databáze s indexy na sloupcích X a Y.
* **Pokud ukládáte pouze názvy míst, nikoli jejich přesné geometrické tvary.**

## 2. PostGIS: Praktický Příklad

Tento příklad ukazuje, jak nastavit PostgreSQL s rozšířením PostGIS pomocí Dockeru, připojit se k databázi pomocí `psql` a provádět základní prostorové operace.

### Struktura

*   **`docker-compose.yml`:** Definuje službu PostGIS.

### Spuštění

1.  **Ujistěte se, že máte nainstalovaný Docker a Docker Compose.**
2.  **Otevřete terminál** a přejděte do tohoto adresáře.
3.  **Spusťte kontejnery:**

    ```bash
    docker-compose up -d
    ```

### 2.1 psql

#### Připojení k PostGIS

*   **Pomocí `psql` (v novém terminálu):**

    ```bash
    docker exec -it postgis psql -U postgres
    ```

    Tím se připojíte k PostgreSQL serveru běžícímu uvnitř kontejneru.  `psql` je interaktivní terminálový klient pro PostgreSQL (podobný `mysql` klientovi pro MySQL).

#### Základní operace (v `psql`)

*   **Vytvoření databáze (volitelné):**

    ```sql
    CREATE DATABASE gisdb;
    ```

*   **Připojení k databázi:**

    ```sql
    \c gisdb
    ```

*   **Povolení rozšíření PostGIS:**

    ```sql
    CREATE EXTENSION postgis;
    ```
    Toto *musíte* udělat v každé databázi, kde chcete používat PostGIS.

*   **Ověření, že PostGIS je nainstalován:**

    ```sql
    SELECT PostGIS_Version();
    ```

*   **Vytvoření tabulky s prostorovým sloupcem:**

    ```sql
    CREATE TABLE cities (
      id SERIAL PRIMARY KEY,
      name TEXT,
      location GEOMETRY(Point, 4326) -- Bod, WGS 84
    );
    ```

    *   `CREATE TABLE`:  Příkaz pro vytvoření tabulky.
    *   `cities`:  Název tabulky.
    *   `location GEOMETRY(Point, 4326)`:  Definuje sloupec `location` typu `GEOMETRY`, který bude ukládat body (Point) v souřadnicovém systému WGS 84 (SRID 4326).

*   **Vložení dat:**

    ```sql
    INSERT INTO cities (name, location) VALUES
      ('Prague', ST_GeomFromText('POINT(14.4378 50.0755)', 4326)),
      ('London', ST_GeomFromText('POINT(-0.1278 51.5074)', 4326)),
      ('New York', ST_GeomFromText('POINT(-74.0060 40.7128)', 4326));
    ```

    *   `ST_GeomFromText`:  Funkce, která vytváří geometrický objekt z WKT reprezentace a SRID.

*   **Vytvoření prostorového indexu:**

    ```sql
    CREATE INDEX cities_location_idx ON cities USING GIST (location);
    ```

    *   `CREATE INDEX`:  Příkaz pro vytvoření indexu.
    *   `cities_location_idx`:  Název indexu.
    *   `ON cities`:  Určuje tabulku, pro kterou se index vytváří.
    *   `USING GIST`:  Určuje typ indexu (GIST - Generalized Search Tree, implementace R-stromu v PostGIS).
    *   `(location)`:  Určuje sloupec, který se má indexovat.

*   **Prostorové dotazy:**

    ```sql
    -- Předpoklady: Existuje tabulka 'cities' se sloupci 'name' (TEXT) a 'location' (GEOMETRY(Point, 4326))
    -- Obsahuje minimálně řádky pro 'Prague', 'London', 'New York'.

    -- 1. Najdi všechna města do 1000 km od Prahy (opraveno pro metry)
    -- Používáme ST_DWithin s přetypováním na geography pro výpočet v metrech.
    -- Poddotaz dynamicky získá polohu Prahy.
    -- Podmínka c1.name != 'Prague' vyloučí Prahu ze výsledků.
    SELECT c1.name
    FROM cities c1
    WHERE ST_DWithin(
        c1.location::geography,  -- Geometrie aktuálního města jako geography
        (SELECT c2.location FROM cities c2 WHERE c2.name = 'Prague')::geography, -- Geometrie Prahy jako geography
        5000000  -- Vzdálenost v METRECH (5000 km)
    )
    AND c1.name != 'Prague'; -- Volitelné: vyloučení Prahy

    -- 2. Spočítej vzdálenost mezi Prahou a Londýnem v METRECH
    -- Přetypování na geography zajistí výpočet sférické vzdálenosti v metrech.
    SELECT ST_Distance(
        (SELECT location FROM cities WHERE name = 'Prague')::geography,
        (SELECT location FROM cities WHERE name = 'London')::geography
    ) AS distance_meters;

    -- 3. Alternativní (čitelnější) zápis pro výpočet vzdálenosti pomocí JOIN syntaxe
    -- Výsledek je stejný jako v bodě 2.
    SELECT ST_Distance(prague.location::geography, london.location::geography) AS distance_meters
    FROM
        (SELECT location FROM cities WHERE name = 'Prague') AS prague,
        (SELECT location FROM cities WHERE name = 'London') AS london;

    -- 4. Transformuj souřadnice měst do SRS EPSG:3857 (Web Mercator)
    -- ST_Transform převede geometrii do jiného souřadnicového systému.
    -- Užitečné pro zobrazení na webových mapách (např. Google Maps, OpenStreetMap).
    SELECT name, ST_AsText(ST_Transform(location, 3857)) AS location_mercator_wkt
    FROM cities;
    -- ST_AsText se používá pro zobrazení výsledné geometrie jako textu (WKT)

    -- 5. Vytvoř obalovou zónu (buffer) 100 km kolem Prahy
    -- Přetypování na geography zajistí, že poloměr bufferu je v metrech.
    -- Výsledkem je geometrie typu POLYGON.
    SELECT ST_AsText(ST_Buffer(location::geography, 100000)) AS prague_buffer_wkt -- 100000 metrů = 100 km
    FROM cities
    WHERE name = 'Prague';

    -- 6. Zjisti, zda New York leží v okruhu 2000 km od Londýna
    -- Použití ST_DWithin je preferovaný způsob pro kontrolu vzdálenosti u typu geography.
    SELECT ST_DWithin(
        (SELECT location::geography FROM cities WHERE name = 'London'), -- Bod Londýna
        (SELECT location::geography FROM cities WHERE name = 'New York'), -- Bod New Yorku
        2000000  -- Vzdálenost v METRECH (2000 km)
    ) AS is_within_2000km; -- Vrátí false

    -- 7. Vytvoření tabulky a vložení polygonu (kraje) - Původní příklad
    CREATE TABLE regions (
        id SERIAL PRIMARY KEY,
        name TEXT,
        boundary GEOMETRY(Polygon, 4326) -- Geometrie s SRID 4326
    );
    -- Vložení velmi zjednodušeného polygonu pro Středočeský kraj
    INSERT INTO regions (name, boundary) VALUES
    ('Středočeský kraj', ST_GeomFromText('POLYGON((14 50, 15 50, 15 51, 14 51, 14 50))', 4326));

    -- 8. Zjisti, ve kterém kraji leží Praha (použití ST_Contains)
    -- ST_Contains pracuje správně s typem geometry.
    -- Tento dotaz předpokládá, že bod Prahy skutečně leží uvnitř definovaného polygonu.
    SELECT r.name
    FROM regions r
    JOIN cities c ON ST_Contains(r.boundary, c.location) -- JOIN je často čitelnější než WHERE r, c
    WHERE c.name = 'Prague';

    -- 9. Vypočítej plochu Středočeského kraje (v metrech čtverečních)
    -- Pro výpočet reálné plochy je nutné přetypovat na geography.
    -- Výsledek ST_Area(geography) je v metrech čtverečních.
    SELECT ST_Area(boundary::geography) AS area_sq_meters
    FROM regions
    WHERE name = 'Středočeský kraj';
    -- Poznámka: Pro velmi zjednodušený čtvercový polygon bude výsledek nepřesný.
    -- Pro přesnější výpočet je nutné použít reálná data hranic.

    -- 10. Vytvoř tabulku silnic a najdi ty, které protínají Středočeský kraj
    CREATE TABLE roads (
        id SERIAL PRIMARY KEY,
        name TEXT,
        path GEOMETRY(LineString, 4326)
    );
    -- Vložení ukázkové silnice (např. část dálnice D1)
    INSERT INTO roads (name, path) VALUES
    ('D1 segment 1', ST_GeomFromText('LINESTRING(14.5 49.9, 14.8 49.8, 15.1 49.7)', 4326));
    INSERT INTO roads (name, path) VALUES('D1 segment 2', ST_GeomFromText('LINESTRING(14.5 49.9, 14.7 50.5, 15.2 50.6)', 4326)); 

    -- Najdi silnice protínající kraj (ST_Intersects)
    SELECT rd.name AS road_name, rg.name AS region_name
    FROM roads rd
    JOIN regions rg ON ST_Intersects(rd.path, rg.boundary)
    WHERE rg.name = 'Středočeský kraj';

    -- 11. Najdi nejbližší město k Londýnu (kromě Londýna samotného)
    -- Použití operátoru <-> (KNN - K-Nearest Neighbors) je efektivní pro hledání nejbližších.
    -- Vyžaduje prostorový index (GIST) na sloupci 'location'.
    -- CREATE INDEX IF NOT EXISTS cities_location_idx ON cities USING GIST (location); -- Pokud index neexistuje
    SELECT
        c1.name AS nearest_city,
        ST_Distance(c1.location::geography, london.location::geography) AS distance_meters
    FROM
        cities c1,
        (SELECT location FROM cities WHERE name = 'London') AS london
    WHERE
        c1.name != 'London'
    ORDER BY
        c1.location <-> london.location -- Operátor pro vzdálenost (pracuje s geometry)
    LIMIT 1;

    ```

*   **Smazání dat:**

    ```sql
    DELETE FROM cities WHERE name = 'New York';
    ```
    Prostorové indexy se aktualizují automaticky při mazání dat.

### 2.2 Užitečné funkce PostGIS

PostGIS nabízí stovky funkcí. Zde je několik dalších, které se často používají:

*   **ST_Area(geometry):**  Vypočítá plochu polygonu (v jednotkách SRS).
*   **ST_Length(geometry):**  Vypočítá délku linie (v jednotkách SRS).
*   **ST_Centroid(geometry):**  Vypočítá těžiště geometrie.
*   **ST_Intersection(geometry1, geometry2):**  Vypočítá průnik dvou geometrií.
*   **ST_Union(geometry1, geometry2):**  Vypočítá sjednocení dvou geometrií.
*   **ST_Difference(geometry1, geometry2):** Vypočítá rozdíl dvou geometrií.
*   **ST_Simplify(geometry, tolerance):**  Zjednoduší geometrii (sníží počet bodů) s danou tolerancí.
*   **ST_IsValid(geometry):**  Ověří, zda je geometrie platná (např. zda se polygon sám neprotíná).
*   **ST_AsGeoJSON(geometry):** Převede geometrii do formátu GeoJSON.
*   **ST_GeomFromGeoJSON(geojson_text):**  Vytvoří geometrii z GeoJSON řetězce.

### Úkoly

1.  **Základní operace:**
    *   Vytvořte novou tabulku `roads` s primárním klíčem `id` (serial), sloupcem `name` (text) a sloupcem `path` (geometry, typ `LineString`, SRID 4326).
    *   Vložte do tabulky `roads` několik linií reprezentujících silnice (použijte `ST_GeomFromText` a WKT).
    *   Vytvořte prostorový index na sloupci `path`.
    *   Vyberte všechny silnice, které protínají Prahu (použijte `ST_Intersects` a data z tabulky `cities`).
    *   Spočítejte celkovou délku všech silnic v tabulce `roads`.
    *   Vytvořte novou tabulku `buildings` s bodovou geometrií. Vložte několik bodů.
    *   Pro každou budovu najděte nejbližší silnici (použijte kombinaci `ST_Distance` a poddotazu, případně laterální spojení `LATERAL JOIN` - viz dokumentace PostgreSQL).

2.  **Import dat:**
    *   Stáhněte si nějaká reálná prostorová data (např. ve formátu Shapefile nebo GeoJSON) z internetu (např. data o hranicích států, řekách, silnicích).  Zkuste najít data pro Českou republiku.  Můžete použít například data z ČÚZK (Český úřad zeměměřický a katastrální) nebo OpenStreetMap.
    *   Importujte tato data do PostGIS.  Můžete použít:
        *   **`shp2pgsql`:**  Nástroj příkazové řádky pro import Shapefile (.shp) do PostGIS (součást PostGIS).  Je to *nejrychlejší* způsob importu velkých Shapefile souborů.
        *   **`ogr2ogr`:**  Univerzální nástroj příkazové řádky pro konverzi mezi různými prostorovými formáty (součást GDAL - Geospatial Data Abstraction Library).  Umí importovat i exportovat data z/do PostGIS.
        *   **QGIS:**  Desktopový GIS software, který umožňuje importovat různá prostorová data a ukládat je do PostGIS.
        *   **pgAdmin:**  Administrační nástroj pro PostgreSQL, který má (omezenou) podporu pro import Shapefile.
    *   Po importu ověřte, že se data správně načetla (např. zobrazením v QGIS nebo provedením jednoduchého prostorového dotazu).

3.  **Prostorové analýzy:**
    *    Pomocí importovaných dat (nebo dat, která jste vytvořili ručně), proveďte nějaké prostorové analýzy.  Například:
        *   Najděte všechny budovy v okruhu 500 metrů od nějaké silnice.
        *   Spočítejte plochu všech lesů v daném okrese (pokud máte data o lesích a okresech).
        *   Zjistěte, které silnice protínají daný kraj.
        * Vypočítejte délku toku řeky (pokud máte data o řekách).
        * Vytvořte obalovou zónu 1km podél dané řeky.

4. **Transformace souřadnicových systémů:**
     * Zjistěte jaký je SRID vašich importovaných dat.
     * Transformujte vaše data do jiného SRID (např. z WGS 84 (EPSG:4326) do S-JTSK (EPSG:5514) - Křovák, používaný v ČR).
     * Ověřte, že transformace proběhla správně (např. porovnáním souřadnic před a po transformaci).

5.  **Diskuze:**
    *   V jakých situacích byste *nepoužili* prostorovou databázi?
    *   Jaké jsou výhody a nevýhody PostGIS oproti jiným prostorovým databázím (např. Oracle Spatial, SQL Server Spatial)?
    *  Jaký je rozdíl mezi `ST_Distance` a `ST_DWithin`? Kdy byste použili kterou funkci?
    *  Vysvětlete, co je to R-strom a jak funguje.
    *  Jak byste řešili situaci, kdy máte velmi velké množství prostorových dat (např. miliardy bodů) a potřebujete provádět rychlé prostorové dotazy? (Hint: partitioning, sharding).
    * Jak byste řešili situaci, kdy potřebujete sledovat pohyb objektů v čase (např. vozidel)? (Hint: Trajectory data types, moving objects databases).
