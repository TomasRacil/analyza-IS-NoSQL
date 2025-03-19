# Multimodelové Databáze

## 1 Multimodelové Databáze: Teorie

V předchozích lekcích jsme prozkoumali různé typy NoSQL databází, z nichž každá je optimalizovaná pro specifický datový model (dokumentový, klíč-hodnota, sloupcový, grafový, atd.). Nyní se zaměříme na *multimodelové databáze*, které kombinují více datových modelů v rámci jednoho systému.  Probereme si, co to znamená, jaké výhody a nevýhody tento přístup přináší, a podíváme se na příklady konkrétních multimodelových databází a jejich použití.

### 1.1 Co jsou multimodelové databáze?

Multimodelová databáze je databázový systém, který podporuje *více než jeden* datový model. To znamená, že v rámci jedné databáze můžete ukládat a pracovat s daty různými způsoby – například jako s dokumenty, grafy, klíči-hodnotami, nebo i relačními tabulkami.  Místo použití specializovaných databází pro každý typ dat můžete mít vše na jednom místě. Klíčové vlastnosti a motivace pro použití multimodelových databází zahrnují:

*   **Flexibilita:** Možnost zvolit nejvhodnější datový model pro daný úkol nebo část aplikace.
*   **Jednotná správa:** Správa a údržba jediné databáze místo několika různých.
*   **Snížení komplexity:** Zjednodušení architektury aplikace, protože není potřeba integrovat více databází.
*   **Konzistence dat:** Snadnější zajištění konzistence dat, pokud jsou všechna data uložena v jedné databázi (i když to závisí na konkrétní implementaci a nastavení).
*   **Polyglot Persistence:** Multimodelové databáze rozšiřují koncept "polyglot persistence" (použití více různých typů databází) tím, že umožňují kombinovat různé modely v rámci *jedné* databáze.  To zjednodušuje infrastrukturu a snižuje latenci.
* **Komplexní Dotazy Napříč Modely:** Umožňuje psát dotazy, které kombinují data z různých modelů (např. dotaz, který kombinuje data z dokumentové kolekce s daty z grafové struktury).

**Příklad flexibility (ArangoDB):**

Představte si, že vyvíjíte sociální síť.  Potřebujete ukládat:

1.  **Uživatelské profily:**  Jméno, e-mail, zájmy (dokumentový model)
2.  **Vztahy mezi uživateli:**  Přátelství, sledování (grafový model)
3.  **Uživatelské relace:**  Dočasné informace o přihlášených uživatelích (klíč-hodnota model).

V multimodelové databázi, jako je ArangoDB, můžete všechny tyto typy dat ukládat a spravovat v *jedné* databázi, a dokonce je kombinovat v dotazech.

```json
// Uživatelský profil (dokument)
{
  "_key": "alice",
  "name": "Alice",
  "email": "[e-mailová adresa byla odstraněna]",
  "interests": ["hiking", "photography"]
}

// Vztah (hrana v grafu)
{
  "_from": "users/alice", // Odkaz na dokument uživatele Alice
  "_to": "users/bob",   // Odkaz na dokument uživatele Boba
  "type": "friend"
}

// Relace (klíč-hodnota)
{
 //(V ArangoDB lze i klíč/hodnota reprezentovat dokumentem)
 "_key": "session:12345",
 "userId": "alice",
 "expires": 1678886400
}

```
### 1.2 Multimodelové vs. Specializované a Relační Databáze

| Vlastnost | Relační databáze (RDBMS) | Specializované NoSQL databáze (např. MongoDB, Redis, Cassandra, Neo4j) | Multimodelové databáze |
| - | - | - | - |
| **Datový model** | Tabulky, řádky, sloupce, pevné schéma (schema-on-write), normalizace. | Jeden specifický datový model (dokumentový, klíč-hodnota, sloupcový, grafový, ...). Schéma může být flexibilní (schema-on-read) nebo i chybět (schemaless). | Více datových modelů v rámci jedné databáze (např. dokumentový + grafový + klíč-hodnota). Flexibilita schématu závisí na konkrétním modelu a implementaci. |
| **Dotazovací jazyk** | SQL. | Různé (závisí na typu databáze). | Různé. Často vlastní dotazovací jazyk, který umožňuje kombinovat dotazy napříč různými modely (např. AQL v ArangoDB). Některé podporují i podmnožinu SQL nebo více dotazovacích jazyků. |
| **Konzistence** | Silná konzistence (ACID). | Často "eventual consistency". Některé nabízejí i silnou konzistenci. | Závisí na konfiguraci a použitém modelu. Některé umožňují nastavit úroveň konzistence pro jednotlivé operace nebo modely. |
| **Škálovatelnost** | Obvykle vertikální. Horizontální škálování je složitější. | Obvykle horizontální. | Obvykle horizontální. |
| **Transakce** | Podpora ACID transakcí. | Zavisí na konkrétním řešení. Často omezená nebo žádná podpora transakcí (často na úrovni jednoho dokumentu/klíče). | Závisí na implementaci. Některé podporují transakce napříč různými modely, ale s omezeními. |
| **Vztahy** | Definované pomocí cizích klíčů, relační integrita. | Řeší se různě (vnořené dokumenty, reference, ...). Aplikace musí zajistit konzistenci. | Závisí na modelu. Grafový model je optimalizovaný pro vztahy. U ostatních modelů se vztahy řeší podobně jako u specializovaných NoSQL databází (vnořené dokumenty, reference). |
| **Použití** | Aplikace s důrazem na integritu dat a konzistenci (bankovnictví, účetnictví, ERP). | Aplikace s důrazem na výkon/škálovatelnost/flexibilitu (sociální sítě, webové aplikace, IoT). Specializované úlohy (např. caching, grafové algoritmy). | Aplikace, které vyžadují kombinaci různých datových modelů. Aplikace, kde se v průběhu vývoje mohou měnit požadavky na datový model. Aplikace, kde je potřeba zjednodušit architekturu a snížit počet používaných databází. |
| **Náročnost na správu** | Vyšší. Vyžaduje DBA. | Obvykle nižší než u RDBMS. | Může být složitější než u specializovaných NoSQL databází, protože je potřeba rozumět více datovým modelům. Ale stále jednodušší než správa *více* různých databází. |
| **Náklady** | Licence na komerční RDBMS mohou být drahé, ale existuje celá řade open source RDBMS. Náklady na vertikální škálování. | Mnoho NoSQL databází je open source. Horizontální škálování.pay-as-you-go. | Podobné jako u NoSQL databází. Některé jsou open source, jiné komerční. |
| **Maturita** | Velmi vyspělá technologie. | Různá. Některé NoSQL technologie jsou velmi vyspělé, jiné méně. | Relativně novější technologie, ale rychle se vyvíjí. Některé multimodelové databáze jsou postaveny na základech existujících NoSQL databází a dědí jejich vyspělost. |

### 1.3 Výhody multimodelových databází (podrobněji)

*   **Snížení latence:** Data jsou uložena v jedné databázi, takže není potřeba provádět dotazy přes síť do různých databází.
*   **Zjednodušení vývoje:** Vývojáři nemusí ovládat a integrovat více různých databázových technologií.
*   **Lepší výkon pro komplexní dotazy:** Dotazy, které kombinují data z různých modelů, mohou být efektivnější, protože se provádějí v rámci jedné databáze.
* **Snadnější správa záloh a obnovy**

### 1.4 Nevýhody multimodelových databází (podrobněji)

*   **Složitost učení:** Vývojáři se musí naučit pracovat s více datovými modely a dotazovacími jazyky (i když je často k dispozici jednotné API).
*   **Potenciální kompromisy ve výkonu:** Optimalizace pro *všechny* datové modely může být obtížnější než optimalizace pro *jeden* specifický model.  Některé operace mohou být pomalejší než v specializované databázi.
*   **Méně vyzrálé nástroje:** Oproti zavedeným relačním a některým NoSQL databázím může být k dispozici méně nástrojů pro monitoring, ladění výkonu a správu.
*   **Menší komunita:** Menší komunita uživatelů a vývojářů může znamenat méně dostupné podpory a dokumentace.
* **Vendor Lock-in**: Přechod na jiný systém, pokud databáze přestane splňovat požadavky, může být velmi složitý.

### 1.5 Příklady multimodelových databází

*   **ArangoDB:** Podporuje dokumentový, grafový a klíč-hodnota model. Má vlastní dotazovací jazyk AQL (ArangoDB Query Language), který umožňuje kombinovat dotazy napříč různými modely.
*   **OrientDB:** (Nyní SAP OrientDB) Podporuje dokumentový, grafový, klíč-hodnota a objektový model.
*   **Azure Cosmos DB:** Cloudová služba od Microsoftu. Podporuje dokumentový, grafový, klíč-hodnota a sloupcový model. Nabízí různé API (včetně API kompatibilních s MongoDB a Cassandra).
* **FoundationDB:** Distribuovaná klíč-hodnota databáze, nad kterou lze stavět další vrstvy (layers) implementující různé datové modely (dokumentový, grafový, ...).
*   **MarkLogic:** Podporuje dokumentový (JSON, XML), grafový (RDF triplestore) a relační model.
*   **Couchbase:** Primárně dokumentová databáze, ale s podporou klíč-hodnota operací a N1QL (dotazovací jazyk podobný SQL).
*   **Fauna:** Serverless databáze, která kombinuje flexibilitu dokumentového modelu s možnostmi relačních dotazů a grafových operací.  Fauna používá vlastní dotazovací jazyk FQL (Fauna Query Language).

## 2 Praktická ukázka (ArangoDB )

Pro praktickou ukázku použijeme ArangoDB, protože je open-source, má relativně jednoduché nastavení a nabízí uživatelsky přívětivé webové rozhraní.

1.  **Instalace a spuštění ArangoDB:**

    *   **Předpoklady:** Ujistěte se, že máte nainstalovaný Docker a Docker Compose na svém počítači. Instalační návody najdete zde:
        *   Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
        *   Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

    * **Spuštění ArangoDB:** Otevřete terminál (nebo příkazový řádek) v tomto adresáři a spusťte příkaz:

        ```bash
        docker-compose up -d
        ```
    *   Otevřete webové rozhraní ArangoDB (obvykle na adrese `http://localhost:8529`).

2.  **Vytvoření databáze a kolekcí:**

    *   Ve webovém rozhraní vytvořte novou databázi (např. "social_network").
    *   Vytvořte kolekci "users" (typ: Document). Tato kolekce bude ukládat uživatelské profily.
    *   Vytvořte kolekci "friendships" (typ: Edge). Tato kolekce bude ukládat vztahy mezi uživateli (hrany).

3.  **Vkládání dat:**
    *   Pomocí webového rozhraní vložte několik dokumentů do kolekce "users".  Každý dokument by měl reprezentovat jednoho uživatele a obsahovat pole jako `_key` (unikátní identifikátor), `name`, `email`, atd.

        ```json
        // Příklad dokumentu v kolekci "users"
        {
          "_key": "alice",
          "name": "Alice Smith",
          "email": "[e-mailová adresa byla odstraněna]",
          "age": 30,
          "interests": ["reading", "hiking"]
        }

        {
          "_key": "bob",
          "name": "Bob Johnson",
          "email": "[e-mailová adresa byla odstraněna]",
          "age": 25,
          "interests": ["coding", "gaming"]
        }
        ```
    * Do kolekce "friendships" vložte několik hran, které propojují uživatele. Každá hrana by měla obsahovat pole `_from` (odkaz na zdrojový uzel – uživatele), `_to` (odkaz na cílový uzel – uživatele) a případně další vlastnosti vztahu.

        ```json
        // Příklad hrany v kolekci "friendships"
        {
          "_from": "users/alice",
          "_to": "users/bob",
          "since": "2023-01-15"
        }
        ```
    * Další dokumenty importujeme hromadně pomocí tlačítka upload documents a zvolením příslušného souboru, který můžete najít v tomto adresáři ve složce data. `users.json` importujte do colekce users a `friendships.json` do kolekce friendships.

4.  **Dotazování (AQL):**

    *   Ve webovém rozhraní ArangoDB přejděte do editoru dotazů (Queries).
    *   Zde můžete psát dotazy v jazyce AQL (ArangoDB Query Language).  AQL umožňuje kombinovat dotazy napříč různými datovými modely.

    *   **Příklad 1: Nalezení všech přátel uživatele Alice:**

        ```aql
        FOR user IN users
          FILTER user._key == "alice"
          FOR friend IN OUTBOUND user friendships
          RETURN friend
        ```
        * Vysvětlení:
            * `FOR user IN users`: Prochází všechny dokumenty v kolekci "users".
            * `FILTER user._key == "alice"`: Vybere uživatele s klíčem "alice".
            * `FOR friend IN OUTBOUND user friendships`: Pro vybraného uživatele ("alice") prochází všechny *výchozí* hrany (OUTBOUND) v kolekci "friendships".
            * `RETURN friend`: Vrací dokumenty uživatelů, kteří jsou přáteli Alice.

    *   **Příklad 2: Nalezení všech uživatelů a jejich zájmů:**

        ```aql
        FOR user IN users
          RETURN {
            name: user.name,
            interests: user.interests
          }
        ```
         *Vysvětlení:*
             *  `FOR user IN users`: Prochází všechny dokumenty v kolekci "users".
             * `RETURN { name: user.name, interests: user.interests }`: Vrací pro každého uživatele objekt s jeho jménem a zájmy.

    *   **Příklad 3: Nalezení uživatelů, kteří mají alespoň dva společné zájmy s Alicí:**

        ```aql
        LET aliceInterests = (
            FOR u IN users
                FILTER u._key == "alice"
                RETURN u.interests
        )[0]

        FOR u IN users
            FILTER u._key != "alice"  // Mimo Alici
            LET commonInterests = INTERSECTION(aliceInterests, u.interests)
            FILTER LENGTH(commonInterests) >= 2
            RETURN {
                name: u.name,
                commonInterests: commonInterests
            }
        ```

        *   **Vysvětlení:**
            *   `LET aliceInterests = ...`:  Nejdříve si do proměnné `aliceInterests` uložíme pole zájmů uživatele Alice.  Všimni si `[0]` na konci - tím získáme *samotné pole* zájmů, ne pole obsahující pole zájmů.
            *   `FOR u IN users ...`: Procházíme všechny uživatele.
            *   `FILTER u._key != "alice"`:  Vynecháme Alici samotnou (chceme najít uživatele *s* nimiž má Alice společné zájmy).
            *   `LET commonInterests = INTERSECTION(aliceInterests, u.interests)`:  Pomocí funkce `INTERSECTION` najdeme průnik zájmů Alice a aktuálního uživatele `u`.  Výsledkem je pole společných zájmů.
            *   `FILTER LENGTH(commonInterests) >= 2`: Filtrujeme pouze ty uživatele, kteří mají s Alicí alespoň dva společné zájmy.
            *   `RETURN { name: u.name, commonInterests: commonInterests }`:  Vracíme objekt obsahující jméno uživatele a pole jeho společných zájmů s Alicí.

        **Další příklady (rozšiřující možnosti AQL a multimodelového přístupu):**

        *   **Příklad 4: Nalezení všech přátel Boba a jejich zájmů:**

            ```aql
            FOR user IN users
            FILTER user._key == "bob"
            FOR friend IN ANY user friendships
            RETURN {
                friendName: friend.name,
                friendInterests: friend.interests
            }
            ```

            *   **Vysvětlení:**
                *   Podobné příkladu 1, ale tentokrát získáme i zájmy přátel.
                *   `ANY user friendships`: Sledujeme všechny hrany (přátelství) *od i do* uživatele "bob".

        *   **Příklad 5: Nalezení všech přátel přátel Alice  a kolik mají s Alicí společných přátel.**

            ```aql
            FOR alice IN users
                FILTER alice._key == "alice"
                FOR friend IN OUTBOUND alice friendships
                    FOR friendOfFriend IN OUTBOUND friend friendships
                    FILTER friendOfFriend._key != "alice" // Vyloučíme Alici

                    // Spočítáme SPOLEČNÉ přátele:
                    LET commonFriends = (
                        FOR common IN INTERSECTION(
                        (FOR f IN OUTBOUND alice friendships RETURN f._key),  // Klíče přátel Alice
                        (FOR ff IN OUTBOUND friendOfFriend friendships RETURN ff._key) // Klíče přátel friendOfFriend
                        )
                        RETURN common
                    )

                    RETURN {
                        friendOfFriendName: friendOfFriend.name,
                        commonFriendsCount: LENGTH(commonFriends)
                    }
            ```

            *   **Vysvětlení:**
                *   `FOR alice IN users ...`: Najdeme Alici.
                *   `FOR friend IN OUTBOUND alice friendships`: Najdeme Aliciny přátele.
                *   `FOR friendOfFriend IN OUTBOUND friend friendships`: Pro každého přítele najdeme *jeho* přátele.
                *   `FILTER friendOfFriend._key != "alice"`:  Vyloučíme Alici ze seznamu přátel přátel.
                * `LET commonFriends`: Spočítá kolikrát se alice vyskytne v přátelých daného friendOfFriend
                *   `RETURN { ... }`:  Vrátíme jméno přítele přítele a počet společných přátel s Alicí.

        * **Příklad 6: Doporučení přátel pro Alici na základě společných zájmů a přátel (kombinace dokumentového a grafového modelu):**

            ```aql
            LET aliceInterests = (
                FOR u IN users
                    FILTER u._key == "alice"
                    RETURN u.interests
            )[0]

            FOR user IN users
                FILTER user._key != "alice" // Vynecháme Alici
                LET commonInterests = INTERSECTION(aliceInterests, user.interests)
                // Spočítáme, kolik má uživatel "user" přátel, kteří jsou *také* přáteli Alice.
                LET commonFriends = (
                    FOR friendOfAlice IN OUTBOUND "users/alice" friendships //Přátele alice
                        FOR friendOfUser IN OUTBOUND user friendships // Přátelé potenciálního přítele
                            FILTER friendOfAlice._key == friendOfUser._key //Shoda
                            RETURN 1
                )
                // Doporučíme uživatele, kteří mají alespoň 1 společný zájem *nebo* alespoň 1 společného přítele.
                FILTER LENGTH(commonInterests) > 0 OR LENGTH(commonFriends) > 0
                SORT LENGTH(commonInterests) * 2 + LENGTH(commonFriends) DESC // Seřadíme podle skóre
                LIMIT 5 // Vrátíme 5 nejlepších doporučení
                RETURN {
                    name: user.name,
                    commonInterests: commonInterests,
                    commonFriends: LENGTH(commonFriends),
                    // Vypočítáme "skóre" doporučení (jednoduchý příklad)
                    recommendationScore: LENGTH(commonInterests) * 2 + LENGTH(commonFriends)
                }
            ```
        * **Vysvětlení**
            * `LET aliceInterests`: Uložíme si zájmy Alice
            * `FOR user IN users`: Procházíme všechny uživatele
            * `FILTER user._key != "alice"`: Vyfiltrujeme Alici
            * `LET commonInterests`: Průnik zájmů
            * `LET commonFriends`: Spočítáme kolik přátel alice je i přáteli potenciálního doporučeného uživatele.
            * `FILTER LENGTH(commonInterests) > 0 OR LENGTH(commonFriends) > 0`: Filtrujeme uživatele kteří splnují podmínky.
            * `recommendationScore`: Jednoduchý algoritmus ohodnocení.
            * `SORT recommendationScore DESC`: Seřadíme sestupně.
            * `LIMIT 5`: Vezmeme prvních pět.

## Úkoly

1.  **Práce s dokumentovou kolekcí:** V databázi `cviceni` vytvořte kolekci `produkty` (typ: Document). Vložte do ní alespoň 5 dokumentů reprezentujících produkty. Každý produkt by měl mít následující pole:
    *   `_key` (řetězec, unikátní klíč produktu)
    *   `nazev` (řetězec)
    *   `cena` (číslo)
    *   `kategorie` (řetězec)
    *   `skladem` (boolean)

2.  **Základní dotazy (AQL):** Napište a spusťte AQL dotazy, které:
    *   a) Vrátí všechny produkty.
    *   b) Vrátí produkty s cenou vyšší než 100.
    *   c) Vrátí název a cenu všech produktů.
    *   d) Vrátí produkty z kategorie "Elektronika".
    *   e) Seřadí produkty podle ceny sestupně.
    *   f) Vrátí prvních 3 nejlevnější produkty.

3.  **Práce s poli:**  Upravte dokumenty v kolekci `produkty` tak, aby každý produkt měl pole `tagy` (pole řetězců). Přidejte k produktům relevantní tagy (např. "sleva", "novinka", "doprava zdarma"). Napište AQL dotazy, které:
    *   a) Vrátí produkty, které mají tag "sleva".
    *   b) Přidají tag "doporucujeme" k produktu s klíčem "produkt123".
    *   c) Odstraní tag "novinka" ze všech produktů.
    *   d) Zjistí, kolik tagů má každý produkt.

4.  **Vytvoření grafu (hranová kolekce):** V databázi `cviceni` vytvořte kolekci `souvislosti` (typ: Edge).  Tato kolekce bude reprezentovat vztahy mezi produkty. Například:
    *   "Podobné produkty"
    *   "Často kupováno spolu s"
    *   "Příslušenství k"

    Vložte do kolekce `souvislosti` alespoň 10 hran.  Každá hrana musí mít:
    *   `_from`: Odkaz na `_key` zdrojového produktu (z kolekce `produkty`).  Formát: `produkty/klic_produktu`
    *   `_to`: Odkaz na `_key` cílového produktu (z kolekce `produkty`). Formát: `produkty/klic_produktu`
    *   `typ`: Typ vztahu (řetězec, např. "podobne", "koupeno_spolu", "prislusenstvi").

6.  **Dotazy na graf:** Napište AQL dotazy, které:
    *   a) Pro zadaný produkt (např. s `_key` "produkt123") najdou všechny *podobné* produkty (pomocí `OUTBOUND` a `souvislosti`).
    *   b) Pro zadaný produkt najdou všechny produkty, které se s ním *často kupují spolu* (pomocí `OUTBOUND` a `souvislosti`).
    *   c) Pro zadaný produkt najdou *všechny* související produkty (bez ohledu na typ vztahu, pomocí `ANY`).
    *   d) Najdou nejkratší cestu mezi dvěma produkty v grafu (pomocí `SHORTEST_PATH`).

7. **Kombinace dotazů (dokument + graf):** Napište AQL dotaz, který pro zadaný produkt (např. "_key": "produktXYZ"):
    * Zjistí jeho kategorii.
    * Najde všechny *podobné* produkty (pomocí grafu).
    * Z těchto podobných produktů vybere pouze ty, které jsou ze *stejné* kategorie jako zadaný produkt.
    * Vrátí názvy a ceny těchto vybraných produktů.

8.  **Doporučovací systém:** Rozšiřte model o hodnocení produktů uživateli (např. nová kolekce `hodnoceni`, kde každý dokument obsahuje `_key` uživatele, `_key` produktu a hodnocení – číslo 1-5). Na základě těchto dat vytvořte jednoduchý doporučovací systém, který pro daného uživatele doporučí produkty, které:
    *   a) Se líbily uživatelům, kteří hodnotili podobně jako on.
    *   b) Jsou podobné produktům (pomocí grafu), které uživatel kladně ohodnotil.

9. **Agregace:** Napište AQL dotazy, které:
    * a) Spočítají průměrnou cenu produktu v každé kategorii.
    * b) Zjistí počet produktů, které mají alespoň jeden tag.
    * c) Najdou kategorii s nejvíce produkty.

10. **Optimalizace (indexy):** Změřte dobu provádění některých z předchozích dotazů (pomocí profilování ve webovém rozhraní).  Zkuste přidat indexy na relevantní pole (např. `cena`, `kategorie`, `tagy`, `_from`, `_to`) a znovu změřte dobu provádění dotazů.  Zjistěte, zda a jak indexy ovlivnily výkon.

11. **Transakce:** Vytvořte jednoduchou simulaci bankovních převodů mezi účty. Vytvořte kolekci `ucty` (dokumenty s poli `_key` a `zustatek`). Napište kód (v JavaScriptu, který spustíte v ArangoDB - viz dokumentace "Transactions"), který provede transakci: převede zadanou částku z jednoho účtu na druhý. Zajistěte, aby transakce byla atomická (buď se provedou obě změny, nebo žádná).

12. **Diskuze:** V jakých scénářích byste nepoužili multimodelovou databázi? Kdy byste dali přednost relační databázi nebo specializované NoSQL databázi (uveďte příklady)? Jaké jsou hlavní výhody a nevýhody použití multimodelového přístupu oproti kombinaci více specializovaných databází? V jakých situacích se hodí který přístup a proč?
