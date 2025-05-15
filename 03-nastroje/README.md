# Analýza informačních systémů: Systémy a nástroje

## Úvod

Po prozkoumání NoSQL databází v předchozím bloku se nyní zaměříme na klíčové systémy a nástroje, které s těmito databázemi (ale i s tradičními relačními databázemi) úzce spolupracují. Tyto nástroje a principy jsou nezbytné pro tvorbu robustních, škálovatelných a efektivních moderních informačních systémů. Databáze samotné tvoří pouze základ; pro vytvoření komplexních aplikací je potřeba zvládnout i další technologie.

Tento blok kurzu bude u každé klíčové oblasti obsahovat teoretický úvod a praktické ukázky s využitím Docker a Docker Compose, které vám umožní si dané koncepty vyzkoušet v izolovaném a reprodukovatelném prostředí.

## Klíčové oblasti

Tento blok kurzu se věnuje následujícím oblastem, které jsou kritické pro vývoj moderních aplikací:

1.  **Komunikace se Serverem (API Design):**
    * Teoretický úvod do REST API, JSON, GraphQL a dalších komunikačních protokolů.
    * Praktická ukázka: Vytvoření jednoduchého REST API serveru pomocí Node.js a Express, spuštěného v Docker kontejneru. Ukázka interakce pomocí `curl` a VS Code REST Client.
    * Viz `01_Komunikace_se_serverem/README.md`

2.  **MapReduce:**
    * Teoretický úvod do principů MapReduce a jeho využití.
    * Praktická ukázka: Jednoduchá implementace MapReduce algoritmu pro počítání slov (word count) v Pythonu, spuštěná v Docker kontejneru.
    * Viz `02_MapReduce/README.md`

3.  **Replikace:**
    * Teoretický úvod do konceptů replikace dat, typů replikace (Master-Slave, Master-Master) a jejich významu pro dostupnost a odolnost systémů.
    * Praktická ukázka: Nastavení Master-Slave replikace pro Redis pomocí Docker Compose. Ukázka zápisu na mastera a čtení ze slave.
    * Viz `03_Replikace/README.md`

4.  **Distribuované zpracování (obecně):**
    * Teoretický úvod do základních konceptů distribuovaného zpracování, výzev (konzistence, komunikace, odolnost vůči chybám) a CAP teorému.
    * Praktická ukázka (Docker Compose): Jednoduchý příklad komunikace mezi dvěma Python Flask službami (`service_a` volá `service_b`) pomocí Docker Compose, včetně Nginx load balanceru a manuálního škálování `service_b`.
    * Praktická ukázka (Kubernetes základy): Nasazení stejných služeb do Kubernetes, ukázka Kubernetes Service pro interní komunikaci a load balancing, a manuální škálování Deploymentu `service_b`.
    * Viz `04_Distribuovane_zpracovani/README.md`

5.  **Sharding (Horizontální Dělení Dat):**
    * Teoretický úvod do shardingu jako techniky pro škálování databází, typy shardingu a výběr sharding klíče.
    * Praktická ukázka: Nastavení jednoduchého Redis Clusteru pomocí Docker Compose pro demonstraci automatického shardingu a distribuce dat.
    * Viz `05_Sharding/README.md`

6.  **Message Queues (Fronty Zpráv):**
    * Teoretický úvod do asynchronní komunikace pomocí front zpráv, jejich výhod a základních konceptů (producent, konzument, fronta).
    * Praktická ukázka: Použití RabbitMQ jako message brokera s Python producentem a konzumentem, spuštěné pomocí Docker Compose. Demonstrace odesílání a přijímání zpráv.
    * Viz `06_Message_Queues/README.md`

7.  **Caching (Ukládání do Mezipaměti):**
    * Teoretický úvod do cachování jako techniky pro optimalizaci výkonu, typy cachování a strategie invalidace.
    * Praktická ukázka: Jednoduchá webová aplikace napsaná v Pythonu s Flaskem, která využívá Redis jako cache pro výsledky "pomalé" operace. Demonstrace cache hit/miss a TTL. Spuštěno pomocí Docker Compose.
    * Viz `07_Caching/README.md` 

## Propojení témat

Všechny tyto systémy a nástroje spolu úzce souvisí a vzájemně se doplňují. Různé typy API (REST, GraphQL) komunikují s databázemi, které využívají replikaci a sharding. MapReduce (nebo Spark) zpracovává data v distribuovaných databázích. Message Queues zajišťují asynchronní komunikaci mezi mikroslužbami, které přistupují k datům přes API. Caching urychluje přístup k datům. Pochopení těchto vzájemných vztahů je zásadní pro návrh a implementaci moderních informačních systémů, které jsou schopné zvládat rostoucí nároky na výkon, škálovatelnost a spolehlivost.

## Další postup

V následujících lekcích se detailně zaměříme na jednotlivá témata. Každá lekce bude obsahovat teoretické základy, praktické příklady a ukázky použití v reálných aplikacích. Cílem je poskytnout ucelený přehled o těchto důležitých technologiích a ukázat, *jak* a *proč* je používat.
