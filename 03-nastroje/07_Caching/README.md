# Caching (Ukládání do Mezipaměti)

## 1. Úvod do Cachování

V mnoha aplikacích se často přistupuje ke stejným datům opakovaně, nebo výpočet či získání některých dat je časově náročné. **Caching (ukládání do mezipaměti)** je technika, která řeší tento problém ukládáním často používaných nebo výpočetně náročných dat do rychlého dočasného úložiště (cache). Při následném požadavku na tato data je lze rychle načíst z cache namísto jejich opětovného generování nebo získávání z pomalejšího primárního úložiště (např. databáze, externí API).

Hlavní cíle cachování:
* **Zvýšení výkonu:** Výrazně zrychluje odezvu aplikace, protože data z cache jsou dostupná mnohem rychleji.
* **Snížení zátěže na backendové systémy:** Redukuje počet dotazů na databáze, externí služby nebo výpočetně náročné operace.
* **Zlepšení škálovatelnosti:** Snížením zátěže umožňuje systému obsloužit více uživatelů a požadavků.
* **Snížení nákladů:** Může snížit náklady na infrastrukturu (méně výkonné databázové servery) nebo na volání placených API.

## 2. Základní Koncepty

* **Cache:** Rychlé dočasné úložiště. Může být umístěna na různých úrovních (viz níže).
* **Cache Hit (Zásah do Cache):** Požadovaná data jsou nalezena v cache.
* **Cache Miss (Chyba Cache):** Požadovaná data nejsou nalezena v cache. V tomto případě se data musí načíst z primárního zdroje a obvykle se poté uloží do cache pro budoucí požadavky.
* **Cache Entry (Položka Cache):** Jednotlivá data uložená v cache, typicky jako pár klíč-hodnota.
* **Klíč Cache (Cache Key):** Unikátní identifikátor pro data uložená v cache.
* **Hodnota Cache (Cache Value):** Samotná data uložená pod klíčem.
* **Doba Platnosti (Time To Live - TTL):** Časový interval, po který je položka v cache považována za platnou. Po uplynutí TTL je položka buď automaticky odstraněna, nebo označena jako neplatná.
* **Politika Nahrazování (Eviction Policy):** Pravidla, která určují, které položky budou z cache odstraněny, když je cache plná a je potřeba uvolnit místo pro nové položky. Běžné politiky:
    * **LRU (Least Recently Used):** Odstraní nejméně nedávno použité položky.
    * **LFU (Least Frequently Used):** Odstraní nejméně často používané položky.
    * **FIFO (First-In, First-Out):** Odstraní nejstarší položky.
    * **Random:** Odstraní náhodnou položku.
* **Invalidace Cache (Cache Invalidation):** Proces odstranění nebo označení položky v cache jako neplatné, pokud se změnila odpovídající data v primárním zdroji. Toto je jedna z nejtěžších částí cachování ("There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton).

## 3. Typy Cachování (Podle Umístění)

* **Klientská Cache (Client-Side Caching):**
    * Data jsou cachována přímo na straně klienta (např. v prohlížeči, mobilní aplikaci).
    * **Příklady:** HTTP cache prohlížeče (pro statické soubory jako obrázky, CSS, JS), data uložená v `localStorage` nebo `sessionStorage`, cache v mobilních aplikacích.
    * **Výhody:** Nejrychlejší přístup pro klienta, snižuje síťový provoz.
    * **Nevýhody:** Omezená kapacita, data jsou specifická pro jednoho klienta, složitější invalidace.

* **CDN Cache (Content Delivery Network):**
    * Kopie statického obsahu (obrázky, videa, CSS, JS) jsou uloženy na serverech CDN rozmístěných geograficky blízko uživatelům.
    * **Příklady:** Cloudflare, Akamai, Amazon CloudFront.
    * **Výhody:** Výrazné zrychlení načítání webových stránek pro globální publikum, snížení zátěže na origin server.
    * **Nevýhody:** Primárně pro statický obsah, náklady na CDN službu.

* **Serverová Cache (Server-Side Caching):**
    * Data jsou cachována na aplikačním serveru nebo na specializovaných cache serverech.
    * **Aplikační Cache (In-Process):** Cache je součástí aplikačního procesu (např. proměnná v paměti, knihovna pro cachování).
        * **Výhody:** Velmi rychlý přístup (v paměti procesu).
        * **Nevýhody:** Omezeno pamětí jednoho procesu, data se ztratí při restartu aplikace, není sdílená mezi více instancemi aplikace.
    * **Distribuovaná Cache (Out-of-Process):** Cache je provozována jako samostatná služba (nebo cluster služeb), ke které se připojují aplikační servery.
        * **Příklady:** Redis, Memcached.
        * **Výhody:** Sdílená mezi více instancemi aplikace, větší kapacita, může být perzistentní, vyšší dostupnost.
        * **Nevýhody:** Vyšší latence přístupu (síťová komunikace), složitější nastavení a správa.

* **Databázová Cache:**
    * Mnoho databázových systémů má vlastní interní mechanismy cachování (např. buffer pool pro často používané datové bloky, cache pro výsledky dotazů).
    * Aplikace mohou také implementovat cachování výsledků databázových dotazů.

## 4. Strategie Cachování

* **Read-Through Cache:**
    1. Aplikace požaduje data z cache.
    2. Pokud jsou data v cache (cache hit), vrátí se aplikaci.
    3. Pokud data v cache nejsou (cache miss), cache sama načte data z primárního zdroje, uloží je k sobě a vrátí aplikaci.
    * Aplikace komunikuje pouze s cache.

* **Write-Through Cache:**
    1. Aplikace zapíše data do cache.
    2. Cache okamžitě zapíše data také do primárního zdroje.
    3. Operace zápisu je dokončena až po úspěšném zápisu do obou (cache i primární zdroj).
    * **Výhody:** Konzistence dat mezi cache a primárním zdrojem.
    * **Nevýhody:** Vyšší latence zápisu.

* **Write-Behind Cache (Write-Back Cache):**
    1. Aplikace zapíše data do cache.
    2. Cache potvrdí zápis aplikaci okamžitě.
    3. Cache zapíše data do primárního zdroje asynchronně (později, v dávkách).
    * **Výhody:** Velmi nízká latence zápisu.
    * **Nevýhody:** Riziko ztráty dat, pokud cache selže před zapsáním do primárního zdroje. Vyšší komplexita.

* **Write-Around Cache:**
    1. Aplikace zapíše data přímo do primárního zdroje.
    2. Cache se při zápisu neaktualizuje. Data se do cache dostanou až při následném čtení (cache miss), pokud je implementována strategie jako read-through.
    * **Výhody:** Vhodné pro data, která se často zapisují, ale málo čtou.
    * **Nevýhody:** Při prvním čtení po zápisu vždy dojde k cache miss.

* **Cache-Aside (Lazy Loading):**
    1. Aplikace nejprve zkusí načíst data z cache.
    2. Pokud data v cache nejsou (cache miss), aplikace načte data z primárního zdroje.
    3. Aplikace poté data uloží do cache.
    4. Aplikace vrátí data.
    * Toto je velmi běžný vzor. Aplikace je zodpovědná za komunikaci s cache i s primárním zdrojem.

## 5. Strategie Invalidace Cache

* **TTL (Time To Live):** Nejjednodušší strategie. Každá položka má definovanou dobu platnosti. Po jejím uplynutí je považována za neplatnou. Vhodné pro data, u kterých nevadí, pokud jsou dočasně mírně neaktuální.
* **Explicitní Invalidace:** Když se data v primárním zdroji změní, aplikace (nebo jiný mechanismus) explicitně pošle příkaz do cache, aby danou položku zneplatnila nebo odstranila.
* **Write-Through s Invalidací:** Při zápisu do primárního zdroje se zároveň invaliduje odpovídající položka v cache.
* **Event-Driven Invalidation:** Primární zdroj (nebo systém, který ho spravuje) publikuje události o změnách dat. Cache (nebo aplikační vrstva) na tyto události reaguje a invaliduje příslušné položky.

## 6. Nástroje a Technologie pro Cachování

* **Redis:** Velmi populární, rychlá in-memory key-value databáze, často používaná jako distribuovaná cache. Podporuje různé datové struktury, perzistenci, replikaci, TTL.
* **Memcached:** Další populární in-memory key-value store, jednodušší než Redis, primárně zaměřený na cachování. Nepodporuje perzistenci ve stejném rozsahu jako Redis.
* **Aplikační knihovny:** Mnoho programovacích jazyků a frameworků má vestavěné nebo externí knihovny pro in-process cachování (např. Ehcache v Javě, `functools.lru_cache` v Pythonu).
* **HTTP Cache Hlavičky:** `Cache-Control`, `Expires`, `ETag`, `Last-Modified` pro řízení cachování v prohlížečích a CDN.
* **Databázové cache mechanismy.**

## 7. Praktická Ukázka: Webová Aplikace s Redis Cache

Pro demonstraci principů cachování je v adresáři příklad jednoduché webové aplikace (napsané v Pythonu s Flaskem), která využívá Redis jako externí cache pro výsledky "náročného" výpočtu nebo "pomalého" databázového dotazu.

**Kde příklad najdete:**

* Adresář: `priklad-redis-caching/` (v rámci této sekce `07_Caching`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad-redis-caching/README.md`.

**Co příklad ukáže:**

* Jak spustit Flask webovou aplikaci a Redis server pomocí Docker Compose.
* Jak se Flask aplikace připojí k Redisu.
* Implementaci strategie cache-aside:
    * Při požadavku na data se aplikace nejprve podívá do Redis cache.
    * Pokud data v cache jsou (cache hit), vrátí je.
    * Pokud data v cache nejsou (cache miss), aplikace provede "pomalou operaci" (simulovanou pomocí `time.sleep()`), uloží výsledek do Redis cache s nastaveným TTL a poté výsledek vrátí.
* Jak ověřit, že cachování funguje a zrychluje následné požadavky.

Tato ukázka vám pomůže pochopit, jak může cachování výrazně zlepšit výkon aplikace.
