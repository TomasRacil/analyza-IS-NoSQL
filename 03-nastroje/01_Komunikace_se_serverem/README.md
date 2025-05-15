# Komunikace se Serverem

## 1. Úvod do API a Komunikace

Moderní informační systémy se často skládají z více nezávislých částí (komponent), které spolu potřebují komunikovat. Například:

* **Frontend** (webová stránka v prohlížeči) potřebuje získat data od **backendu** (serverové části aplikace).
* **Backend** potřebuje komunikovat s **databází** (relační nebo NoSQL).
* Různé **mikroslužby** si mohou vyměňovat data.

K této komunikaci slouží **API (Application Programming Interface)** – rozhraní pro programování aplikací. API definuje sadu pravidel a protokolů, jak spolu softwarové komponenty mohou interagovat. Můžeme si ho představit jako smlouvu, která říká: "Pokud mi pošleš požadavek v tomto formátu na tuto adresu, odpovím ti tímto způsobem."

V kontextu webových aplikací a služeb je nejrozšířenějším architektonickým stylem pro tvorbu API **REST**.

## 2. REST (Representational State Transfer)

REST není protokol ani standard, ale **architektonický styl**, sada principů a omezení pro návrh síťových aplikací. API navržené podle principů REST se označuje jako **RESTful API**.

**Klíčové principy REST:**

1.  **Klient-Server (Client-Server):** Architektura je rozdělena na klienta (který žádá o zdroje) a server (který zdroje poskytuje). Jsou na sobě nezávislí a mohou se vyvíjet odděleně. Klient neví nic o vnitřní implementaci serveru a naopak.
2.  **Bezstavovost (Stateless):** Každý požadavek od klienta na server musí obsahovat *všechny* informace potřebné k jeho zpracování. Server si *neukládá* žádný kontext (stav) o klientovi mezi jednotlivými požadavky. Pokud je potřeba udržovat stav (např. přihlášený uživatel), musí být součástí každého požadavku (např. pomocí tokenu). To zjednodušuje server a zlepšuje škálovatelnost.
3.  **Cacheovatelnost (Cacheable):** Odpovědi serveru by měly být označeny jako cacheovatelné nebo necacheovatelné. Pokud je odpověď cacheovatelná, klient (nebo mezivrstva, např. proxy) si ji může uložit a použít pro budoucí stejné požadavky, čímž se snižuje zátěž serveru a zlepšuje rychlost odezvy.
4.  **Jednotné Rozhraní (Uniform Interface):** Toto je klíčový princip, který zjednodušuje a odděluje architekturu. Skládá se z několika částí:
    * **Identifikace zdrojů:** Každý zdroj (např. uživatel, produkt, článek) je jednoznačně identifikován pomocí URI (Uniform Resource Identifier), typicky URL. Např. `/users/123`, `/products/45`.
    * **Manipulace se zdroji pomocí reprezentací:** Klient nepracuje přímo se zdrojem na serveru, ale s jeho *reprezentací* (např. JSON nebo XML dokumentem). Server posílá klientovi reprezentaci zdroje a klient může poslat upravenou reprezentaci zpět na server pro aktualizaci zdroje.
    * **Samo-popisné zprávy (Self-descriptive messages):** Každá zpráva (požadavek i odpověď) obsahuje dostatek informací, aby ji druhá strana pochopila (např. HTTP metoda, URI, hlavičky jako `Content-Type` určující formát dat, stavový kód odpovědi).
    * **HATEOAS (Hypermedia as the Engine of Application State):** Reprezentace zdroje by měla obsahovat odkazy (hypermedia) na další související akce nebo zdroje. Klient tak může "objevovat" API procházením odkazů, aniž by musel znát všechny URI předem. (Tento princip je v praxi často méně striktně dodržován).
5.  **Vrstevnatý Systém (Layered System):** Klient nemusí vědět, zda komunikuje přímo s koncovým serverem, nebo s mezivrstvou (např. load balancer, proxy, cache). Mezivrstvy mohou zlepšit škálovatelnost, bezpečnost a výkon.
6.  **Kód na vyžádání (Code on Demand - Volitelné):** Server může dočasně rozšířit funkcionalitu klienta zasláním spustitelného kódu (např. JavaScript). Tento princip se používá méně často.

## 3. HTTP a REST

RESTful API téměř výhradně používají **HTTP protokol** pro komunikaci. Využívají standardní **HTTP metody** (někdy označované jako "slovesa") k definování akce, která se má provést se zdrojem identifikovaným pomocí URI:

* **GET:** Získání reprezentace zdroje (nebo kolekce zdrojů). Je **bezpečná** (nemění stav serveru) a **idempotentní** (opakované volání má stejný efekt jako jedno volání).
    * Příklad: `GET /users/123` (získání uživatele s ID 123)
    * Příklad: `GET /users` (získání seznamu všech uživatelů)
* **POST:** Vytvoření nového podřízeného zdroje v rámci kolekce, nebo provedení akce, která se nehodí na jiné metody. **Není** bezpečná ani idempotentní (opakované volání může vytvořit více zdrojů).
    * Příklad: `POST /users` (vytvoření nového uživatele; data uživatele jsou v těle požadavku)
    * Příklad: `POST /orders/123/recalculate` (provedení specifické akce)
* **PUT:** Aktualizace *celého* existujícího zdroje, nebo vytvoření zdroje na *konkrétním* URI (pokud neexistuje). Je **idempotentní** (opakované volání se stejnými daty má stejný výsledek jako jedno volání). Tělo požadavku obsahuje *kompletní* novou reprezentaci zdroje.
    * Příklad: `PUT /users/123` (nahrazení *všech* dat uživatele 123 daty z těla požadavku)
* **DELETE:** Smazání zdroje. Je **idempotentní** (opakované volání na smazaný zdroj by mělo vrátit stejný výsledek, typicky úspěch nebo "nenalezeno").
    * Příklad: `DELETE /users/123` (smazání uživatele 123)
* **PATCH:** Částečná aktualizace existujícího zdroje. Na rozdíl od `PUT` posílá pouze *změny*, které se mají aplikovat. **Není** nutně idempotentní (závisí na povaze změn).
    * Příklad: `PATCH /users/123` (aktualizace pouze emailu uživatele 123; změna je specifikována v těle požadavku)

**Struktura HTTP Požadavku/Odpovědi v REST:**

* **Metoda:** GET, POST, PUT, DELETE, PATCH, ...
* **URI (Endpoint):** URL adresa identifikující zdroj (např. `/api/v1/users/123`).
* **HTTP Verze:** Např. `HTTP/1.1`.
* **Hlavičky (Headers):** Metadata požadavku/odpovědi.
    * `Content-Type`: Určuje formát dat v těle požadavku (např. `application/json`).
    * `Accept`: Určuje formáty dat, které klient akceptuje v odpovědi (např. `application/json`).
    * `Authorization`: Obsahuje autentizační údaje (např. API klíč, Bearer token).
    * `Cache-Control`: Instrukce pro cachování.
    * ... a mnoho dalších.
* **Tělo (Body/Payload):** Samotná data (reprezentace zdroje), typicky ve formátu JSON. Používá se u metod POST, PUT, PATCH. GET a DELETE obvykle tělo nemají.
* **Stavový kód odpovědi (Status Code):** Číslo indikující výsledek požadavku (např. `200 OK`, `201 Created`, `404 Not Found`, `500 Internal Server Error`).

## 4. JSON (JavaScript Object Notation)

JSON je lehký, textový formát pro výměnu dat, který je snadno čitelný pro lidi i stroje. Stal se *de facto standardem* pro data přenášená v REST API.

**Syntaxe JSON:**

* Data jsou reprezentována jako páry **klíč-hodnota**.
* Klíče jsou **řetězce** uzavřené v uvozovkách (`"`).
* Hodnoty mohou být:
    * **Řetězec (String):** Uzavřený v uvozovkách (`"Ahoj"`).
    * **Číslo (Number):** Integer nebo float (`123`, `3.14`).
    * **Boolean:** `true` nebo `false`.
    * **Null:** `null`.
    * **Pole (Array):** Uspořádaný seznam hodnot uzavřený v hranatých závorkách (`[` `]`). Hodnoty mohou být různých typů.
        ```json
        ["jablko", "hruška", 123, true]
        ```
    * **Objekt (Object):** Neuspořádaná kolekce párů klíč-hodnota uzavřená ve složených závorkách (`{` `}`).
        ```json
        {
          "jmeno": "Jan",
          "prijmeni": "Novák",
          "vek": 30,
          "aktivni": true,
          "adresa": {
            "ulice": "Hlavní 1",
            "mesto": "Praha"
          },
          "konicky": ["čtení", "sport"]
        }
        ```

**Výhody JSON:**

* **Čitelnost:** Snadno čitelný pro lidi.
* **Jednoduchost:** Jednoduchá a jasná syntaxe.
* **Rozšířenost:** Podporován prakticky všemi programovacími jazyky a platformami.
* **Kompaktnost:** Méně "ukecaný" než XML.
* **Snadné parsování:** Snadno se zpracovává programově.

## 5. Použití REST API a JSON pro Databáze

REST API a JSON se běžně používají jako rozhraní pro komunikaci s backendovými službami, které následně interagují s databázemi (včetně NoSQL). CRUD operace (Create, Read, Update, Delete) nad databázovými záznamy se typicky mapují na HTTP metody:

* **CREATE:** `POST /kolekce` (např. `POST /users`) - Data nového záznamu jsou v JSON těle požadavku.
* **READ (jeden záznam):** `GET /kolekce/{id}` (např. `GET /users/123`) - Vrací JSON reprezentaci záznamu.
* **READ (více záznamů):** `GET /kolekce` (např. `GET /users`) - Vrací pole JSON objektů. Často podporuje filtrování, řazení a stránkování pomocí query parametrů (např. `GET /users?city=Prague&limit=10`).
* **UPDATE (celý záznam):** `PUT /kolekce/{id}` (např. `PUT /users/123`) - Kompletní nová JSON reprezentace záznamu je v těle požadavku.
* **UPDATE (částečný záznam):** `PATCH /kolekce/{id}` (např. `PATCH /users/123`) - JSON tělo obsahuje pouze pole, která se mají změnit.
* **DELETE:** `DELETE /kolekce/{id}` (např. `DELETE /users/123`).

**Příklad `curl` požadavku pro vytvoření uživatele:**

```bash
curl -X POST [http://example.com/api/v1/users](http://example.com/api/v1/users) \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Alice",
           "email": "[e-mailová adresa byla odstraněna]",
           "age": 28
         }'
```

## 6. Best Practices pro Návrh REST API

* **Používejte podstatná jména pro URI:** URI by měly identifikovat *zdroje* (podstatná jména), ne akce (slovesa). Používejte množné číslo pro kolekce.
    * Dobře: `/users`, `/users/123`, `/products`, `/orders/45/items`
    * Špatně: `/getAllUsers`, `/createUser`, `/deleteProduct/45`
* **Používejte HTTP metody pro akce:** Akce definujte pomocí standardních HTTP metod (GET, POST, PUT, DELETE, PATCH).
* **Používejte HTTP stavové kódy správně:** Vracejte smysluplné stavové kódy (200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error, atd.).
* **Poskytujte užitečné chybové zprávy:** V těle odpovědi u chybových stavů (4xx, 5xx) poskytněte detailnější informace o chybě ve formátu JSON.
* **Verzování API:** Pokud plánujete změny API, které nejsou zpětně kompatibilní, zaveďte verzování (např. `/api/v1/users`, `/api/v2/users`).
* **Filtrování, řazení, stránkování:** U kolekcí zdrojů (`GET /kolekce`) umožněte filtrování, řazení a stránkování pomocí query parametrů (např. `?status=active&sort=name&limit=20&offset=40`).
* **Používejte JSON konzistentně:** Používejte JSON pro těla požadavků i odpovědí. Dodržujte konzistentní pojmenování klíčů (např. camelCase).
* **Zabezpečení:** Používejte HTTPS. Zvažte vhodný mechanismus autentizace a autorizace (např. API klíče, OAuth 2.0, JWT tokeny).
* **Dokumentace:** Poskytněte jasnou a aktuální dokumentaci API (např. pomocí nástrojů jako Swagger/OpenAPI).

## 7. Nástroje pro Práci s REST API

* **`curl`:** Univerzální nástroj příkazové řádky pro posílání HTTP požadavků. Skvělý pro rychlé testování a skriptování.
* **Postman:** Populární grafická aplikace pro návrh, testování a dokumentaci API. Velmi uživatelsky přívětivý.
* **Insomnia:** Další populární grafický API klient.
* **REST Client (VS Code Extension - humao.rest-client):** Lehké rozšíření pro Visual Studio Code, které umožňuje posílat HTTP požadavky a prohlížet odpovědi přímo v editoru. Požadavky se definují v souborech s příponou `.http` nebo `.rest` pomocí jednoduché syntaxe.
* **Swagger UI / OpenAPI Explorer:** Nástroje pro interaktivní vizualizaci a testování API dokumentovaných pomocí OpenAPI specifikace.
* **Knihovny v programovacích jazycích:** Každý jazyk má knihovny pro snadné vytváření HTTP požadavků (např. `requests` v Pythonu, `fetch` v JavaScriptu, `HttpClient` v Javě a C#).

## 8. GraphQL

GraphQL je **dotazovací jazyk pro API** a zároveň **runtime pro vykonávání těchto dotazů** pomocí existujících dat. Byl vyvinut Facebookem (nyní Meta) a v roce 2015 uvolněn jako open-source. Na rozdíl od RESTu, který obvykle vyžaduje více endpointů pro různé zdroje, GraphQL používá **jeden endpoint**, na který klienti posílají strukturované dotazy.

**Klíčové vlastnosti a výhody GraphQL:**

1.  **Klient specifikuje data:** Největší výhodou je, že klient v dotazu přesně definuje, která data potřebuje. Server vrátí *pouze* tato data, nic víc, nic míň.
    * **Řeší Over-fetching:** Klient nedostává zbytečná data, která nepotřebuje (což se v RESTu často stává, pokud endpoint vrací fixní strukturu).
    * **Řeší Under-fetching:** Klient nemusí posílat více požadavků na různé endpointy, aby získal všechna potřebná související data. Vše lze získat jedním GraphQL dotazem.
2.  **Silně typované schéma (Strongly Typed Schema):** GraphQL API je definováno pomocí schématu, které popisuje dostupné typy dat a operace. Toto schéma slouží jako "smlouva" mezi klientem a serverem a umožňuje validaci dotazů a introspekci (klient může zjistit, jaké dotazy jsou možné).
3.  **Jeden Endpoint:** Veškerá komunikace probíhá přes jeden URI (např. `/graphql`), obvykle pomocí metody `POST`. Typ operace (čtení, zápis) je určen strukturou dotazu, nikoli HTTP metodou nebo URI.
4.  **Introspekce:** Klienti mohou posílat dotazy na samotné schéma API, aby zjistili, jaké typy, pole a operace jsou k dispozici. To usnadňuje vývoj nástrojů a klientských aplikací.

**Základní koncepty GraphQL:**

* **Schéma (Schema):** Definuje datový model API. Skládá se z typů.
    * **Typy (Types):** Definují strukturu dat (objekty s poli). Mohou být skalární (Int, Float, String, Boolean, ID) nebo objektové.
    * **Dotazy (Queries):** Operace pro čtení dat. Definují vstupní bod pro dotazy ve schématu.
    * **Mutace (Mutations):** Operace pro zápis, aktualizaci nebo mazání dat. Obdoba POST, PUT, PATCH, DELETE v RESTu.
    * **Předplatná (Subscriptions):** Umožňují klientům odebírat data v reálném čase (server posílá aktualizace, když nastane událost). Typicky implementováno pomocí WebSockets.
* **Resolvery (Resolvers):** Funkce na straně serveru, které jsou zodpovědné za získání dat pro konkrétní pole ve schématu. Když server obdrží dotaz, zavolá příslušné resolvery, aby data sestavil.

**Příklad GraphQL Dotazu (Query):**

Klient chce získat jméno a email uživatele s ID 123 a názvy jeho posledních 3 příspěvků.

```graphql
query GetUserAndPosts {
  user(id: "123") {
    name
    email
    posts(last: 3) {
      title
    }
  }
}
```

**Příklad Odpovědi (JSON):**

Server vrátí JSON, který přesně odpovídá struktuře dotazu:

```json
{
  "data": {
    "user": {
      "name": "Jan Novák",
      "email": "[e-mailová adresa byla odstraněna]",
      "posts": [
        { "title": "Můj třetí příspěvek" },
        { "title": "Další zajímavost" },
        { "title": "První myšlenky" }
      ]
    }
  }
}
```

**Příklad GraphQL Mutace (Mutation):**

Klient chce vytvořit nový příspěvek a získat zpět jeho ID a název.

```graphql
mutation CreatePost {
  createPost(title: "Nový příspěvek", content: "Obsah...") {
    id
    title
  }
}
```

**GraphQL vs. REST:**

| Vlastnost         | REST                                       | GraphQL                                     |
| :---------------- | :----------------------------------------- | :------------------------------------------ |
| **Endpointy** | Více endpointů (URI pro každý zdroj)      | Jeden endpoint                              |
| **Načítání dat** | Fixní struktura odpovědi (over/under-fetching) | Klient specifikuje potřebná data           |
| **HTTP Metody** | Definuje akci (GET, POST, PUT, DELETE)     | Obvykle jen POST, akce definována dotazem   |
| **Typování** | Slabé (záleží na dokumentaci/konvencích)  | Silné (definováno schématem)                |
| **Introspekce** | Omezená (závisí na implementaci, např. OpenAPI) | Vestavěná                                   |
| **Caching** | Snadný (standardní HTTP caching)           | Složitější (obvykle na úrovni klienta)      |
| **Vývoj klienta** | Jednodušší pro základní případy           | Může být složitější (nutnost sestavit dotaz) |
| **Vývoj serveru** | Jednodušší na implementaci základního API  | Složitější (nutnost implementovat schéma a resolvery) |
| **Zabezpečení** | Standardní HTTP mechanismy (HTTPS, Auth hlavičky - Basic, Bearer, API klíče). Autorizace typicky per endpoint. | Přenos přes HTTPS. Autentizace obvykle na HTTP vrstvě. Autorizace často granulární (v resolverech, direktivy), může být komplexnější. |

**Kdy použít GraphQL?**

* **Komplexní data a vztahy:** Když potřebujete získávat data z více propojených zdrojů najednou.
* **Různorodí klienti:** Mobilní aplikace, webové aplikace, různé verze klientů – každý si může vyžádat jen to, co potřebuje.
* **Omezená šířka pásma:** Mobilní aplikace, kde je důležité minimalizovat přenášená data.
* **Rychlý vývoj frontendu:** Frontend tým není blokován čekáním na specifické endpointy od backend týmu.

**Nástroje pro GraphQL:**

* **Apollo (Platforma):** Populární sada nástrojů pro server i klienta (Apollo Server, Apollo Client).
* **Relay (Facebook):** Klientská knihovna pro React.
* **GraphiQL:** Interaktivní webové rozhraní pro testování GraphQL dotazů (podobné Postmanu pro REST).
* **GraphQL Playground:** Další interaktivní IDE pro GraphQL.

## 9. Další Komunikační Protokoly a Standardy

Kromě REST a GraphQL existují i další technologie pro komunikaci mezi systémy:

* **gRPC (Google Remote Procedure Call):**
    * Moderní, vysokovýkonný open-source framework pro RPC (Remote Procedure Call - Vzdálené volání procedur).
    * Používá **HTTP/2** pro přenos a **Protocol Buffers** jako jazykově neutrální formát pro serializaci strukturovaných dat (efektivnější než JSON).
    * Nabízí funkce jako obousměrné streamování a snadnou definici služeb.
    * **Výhody:** Vysoký výkon, nízká latence, efektivní využití sítě, silné typování, podpora více jazyků.
    * **Nevýhody:** Méně čitelný formát dat (binární), omezená podpora v prohlížečích (vyžaduje proxy).
    * **Použití:** Komunikace mezi mikroslužbami v interních sítích, mobilní aplikace, kde je důležitý výkon a efektivita.

* **SOAP (Simple Object Access Protocol):**
    * Starší protokol založený na **XML** pro výměnu strukturovaných informací při implementaci webových služeb.
    * Je více standardizovaný než REST (WS-* standardy pro bezpečnost, transakce atd.).
    * **Výhody:** Standardizace, vestavěná podpora pro bezpečnost a transakce (WS-Security, WS-AtomicTransaction).
    * **Nevýhody:** Složitost, "ukecanost" XML formátu, nižší výkon oproti REST/gRPC.
    * **Použití:** Stále se používá v některých enterprise systémech, bankovnictví, státní správě, kde jsou vyžadovány striktní standardy a bezpečnostní funkce.

* **WebSockets:**
    * Komunikační protokol, který umožňuje **plně duplexní (full-duplex) komunikaci** mezi klientem a serverem přes **jedno TCP spojení**.
    * Na rozdíl od HTTP (kde klient pošle požadavek a server odpoví), WebSockets umožňují serveru posílat data klientovi *kdykoli* bez explicitního požadavku od klienta.
    * **Výhody:** Komunikace v reálném čase, nízká latence po navázání spojení, efektivní pro časté malé zprávy.
    * **Nevýhody:** Složitější správa stavu spojení, menší podpora pro cachování a mezivrstvy než u HTTP.
    * **Použití:** Chatovací aplikace, online hry, notifikace v reálném čase, živé sportovní výsledky, kolaborativní editory.

* **Webhooky:**
    * Mechanismus, kdy jedna aplikace (server) posílá **automatické HTTP notifikace** (typicky POST požadavek) na předem definovanou URL adresu jiné aplikace (klienta), když nastane určitá událost.
    * Je to způsob, jak implementovat "event-driven" komunikaci. Klient nemusí neustále dotazovat server na změny (polling), ale je informován serverem, když se něco stane.
    * **Výhody:** Efektivní (šetří zdroje oproti pollingu), jednoduchá implementace pro notifikace.
    * **Nevýhody:** Vyžaduje, aby klient měl veřejně dostupný HTTP endpoint pro příjem notifikací, menší spolehlivost (zpráva se může ztratit, pokud klient není dostupný).
    * **Použití:** Notifikace o nových commitech (GitHub), zpracování plateb (Stripe), aktualizace stavu objednávky, integrace různých služeb.

## 10. Praktická Ukázka: Jednoduché REST API

Pro praktické vyzkoušení konceptů REST API najdete v materiálech jednoduchý příklad. Tento příklad demonstruje vytvoření a spuštění REST API serveru pomocí Node.js, frameworku Express a Dockeru. API poskytuje základní CRUD operace pro správu seznamu úkolů.

**Kde příklad najdete:**

* Adresář: `priklad-rest/` (v rámci této sekce `01_Komunikace_se_serverem`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad_REST_API/README.md`.

**Co příklad ukazuje:**

* Jak definovat API endpointy pro operace GET, POST, PUT, DELETE.
* Jak pracovat s JSON daty v požadavcích a odpovědích.
* Jak kontejnerizovat Node.js aplikaci pomocí Dockeru.
* Jak spravovat vícekontejnerovou aplikaci (i když zde máme jen jeden hlavní kontejner) pomocí Docker Compose.
* Jak testovat API pomocí nástroje `curl` nebo rozšíření VS Code REST Client.