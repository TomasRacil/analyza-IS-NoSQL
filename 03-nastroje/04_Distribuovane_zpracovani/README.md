# Distribuované Zpracování (Obecně)

## 1. Úvod do Distribuovaného Zpracování

Moderní informační systémy často čelí požadavkům na zpracování velkého objemu dat, vysokou dostupnost a schopnost škálovat podle aktuální zátěže. Distribuované zpracování je přístup, který řeší tyto výzvy rozdělením úloh a dat mezi více počítačů (uzlů), které spolupracují na dosažení společného cíle. Místo spoléhání na jeden výkonný (a drahý) server se výpočetní síla a úložná kapacita rozkládá na cluster běžných serverů.

## 2. Základní Koncepty

* **Distribuovaný systém:** Systém, jehož komponenty jsou umístěny na různých propojených počítačích, které komunikují a koordinují své akce předáváním zpráv. Z pohledu uživatele by se měl distribuovaný systém jevit jako jeden koherentní celek.
* **Uzel (Node):** Jednotlivý počítač v distribuovaném systému.
* **Cluster:** Skupina propojených uzlů, které spolupracují.
* **Komunikace mezi procesy (Inter-Process Communication - IPC):** Mechanismy, které umožňují procesům běžícím na různých uzlech si vyměňovat informace (např. RPC, message queues, REST API).
* **Paralelismus a Distribuce:**
    * **Paralelismus:** Současné provádění více úloh (nebo částí jedné úlohy) pro zvýšení rychlosti. Může probíhat na jednom vícejádrovém počítači.
    * **Distribuce:** Rozložení komponent systému na více počítačů. Distribuce často umožňuje paralelismus.
* **Škálovatelnost (Scalability):** Schopnost systému zvládat rostoucí zátěž.
    * **Vertikální škálování (Scaling Up):** Zvyšování výkonu jednoho uzlu (více CPU, RAM). Má své limity a je nákladné.
    * **Horizontální škálování (Scaling Out):** Přidávání dalších uzlů do clusteru. Typické pro distribuované systémy.
* **Dostupnost (Availability):** Pravděpodobnost, že systém je funkční a schopný poskytovat služby v daném čase. Vyjadřuje se často v procentech (např. "pět devítek" - 99.999% dostupnost).
* **Odolnost proti chybám (Fault Tolerance):** Schopnost systému pokračovat v činnosti i v případě selhání některých jeho komponent (uzlů, síťových spojení).

## 3. Výhody Distribuovaného Zpracování

* **Škálovatelnost:** Možnost snadno přidávat další zdroje pro zvládnutí větší zátěže.
* **Vysoká dostupnost a odolnost proti chybám:** Selhání jednoho uzlu nemusí znamenat selhání celého systému, pokud jsou implementovány mechanismy redundance a failoveru.
* **Výkon:** Rozdělení práce mezi více uzlů může vést k rychlejšímu zpracování.
* **Cenová efektivita:** Často je levnější postavit cluster z běžných serverů než investovat do jednoho extrémně výkonného mainframe.
* **Geografická distribuce:** Možnost umístit uzly blíže k uživatelům pro snížení latence nebo pro splnění legislativních požadavků na umístění dat.

## 4. Výzvy Distribuovaného Zpracování

* **Složitost návrhu a implementace:** Distribuované systémy jsou inherentně složitější než centralizované.
* **Komunikace:** Síťová komunikace je pomalejší a méně spolehlivá než komunikace uvnitř jednoho stroje. Latence a šířka pásma sítě jsou klíčovými faktory.
* **Konzistence dat:** Udržet konzistentní data napříč více uzly je velkou výzvou. Viz CAP teorém.
* **Synchronizace a koordinace:** Zajištění, aby uzly spolupracovaly správně a nedocházelo ke konfliktům.
* **Detekce a řešení chyb:** Identifikace selhání uzlů nebo sítě a zotavení z těchto chyb.
* **Bezpečnost:** Zabezpečení komunikace a dat napříč více uzly.
* **Testování a ladění:** Může být výrazně obtížnější než u monolitických aplikací.

## 5. CAP Teorém (Brewerův Teorém)

CAP teorém je fundamentálním principem v návrhu distribuovaných systémů. Tvrdí, že jakýkoli distribuovaný datový sklad může současně poskytnout **maximálně dvě** z následujících tří záruk:

1.  **Consistency (Konzistence):** Všechny čtecí operace obdrží nejaktuálnější zapsaná data nebo chybu. To znamená, že všechny uzly vidí stejná data ve stejný okamžik.
2.  **Availability (Dostupnost):** Každý požadavek (čtení nebo zápis) obdrží odpověď (ne nutně s nejaktuálnějšími daty), aniž by byla zaručena konzistence. Systém je vždy připraven přijmout požadavky.
3.  **Partition Tolerance (Odolnost vůči rozdělení sítě):** Systém pokračuje v provozu i v případě, že dojde k výpadku síťové komunikace mezi některými uzly (síť se "rozdělí" na více částí, které spolu nemohou komunikovat).

V reálných distribuovaných systémech je **odolnost vůči rozdělení sítě (P) prakticky nutností**, protože sítě nejsou nikdy 100% spolehlivé. Proto se volba obvykle zužuje na:

* **CP (Consistency + Partition Tolerance):** Systém preferuje konzistenci. Pokud dojde k rozdělení sítě, může se stát nedostupným (např. odmítat zápisy nebo i čtení), aby se zabránilo nekonzistenci. Příkladem jsou některé tradiční relační databáze v clusteru nebo systémy jako ZooKeeper.
* **AP (Availability + Partition Tolerance):** Systém preferuje dostupnost. I při rozdělení sítě bude každý oddíl pokračovat v provozu a přijímat požadavky. To však může vést k tomu, že různé části systému budou mít dočasně odlišné verze dat (eventual consistency). Příkladem jsou mnohé NoSQL databáze jako Cassandra nebo DynamoDB.

Výběr mezi CP a AP závisí na specifických požadavcích aplikace. Pro finanční transakce je obvykle klíčová konzistence, zatímco pro sociální sítě může být přijatelnější vyšší dostupnost i za cenu dočasné nekonzistence.

## 6. Architektury Distribuovaných Systémů

* **Klient-Server:** Tradiční model, kde klienti žádají o služby od centrálního serveru (nebo skupiny serverů).
* **Peer-to-Peer (P2P):** Všechny uzly jsou si rovny a mohou fungovat jako klient i server.
* **Mikroslužby (Microservices):** Architektonický styl, kde je aplikace rozdělena na sadu malých, nezávislých a samostatně nasaditelných služeb. Každá služba implementuje specifickou business funkcionalitu a komunikuje s ostatními přes dobře definovaná API (často HTTP/REST nebo message queues).
    * **Výhody:** Nezávislý vývoj a nasazení, technologická diverzita (každá služba může být napsána v jiném jazyce/frameworku), lepší škálovatelnost a odolnost (selhání jedné služby nemusí ovlivnit ostatní).
    * **Nevýhody:** Větší provozní složitost, nutnost řešit distribuovanou komunikaci, testování, monitoring.

## 7. Distribuované Databáze

Mnoho NoSQL databází (MongoDB, Cassandra, Redis Cluster) je navrženo jako distribuované systémy, které automaticky řeší replikaci a sharding dat napříč clusterem. Relační databáze také nabízejí různá řešení pro distribuci (např. PostgreSQL s Patroni, Citus).

## 8. Nástroje a Technologie

* **Kontejnerizace (Docker, Kubernetes):** Klíčové technologie pro nasazování a správu distribuovaných aplikací (zejména mikroslužeb).
* **Message Queues (RabbitMQ, Kafka, Redis Streams):** Umožňují asynchronní komunikaci mezi komponentami systému.
* **Distribuované souborové systémy (HDFS, GlusterFS):** Pro ukládání velkých objemů dat.
* **Frameworky pro distribuované výpočty (Apache Spark, Apache Flink):** Pro zpracování velkých datových sad.
* **Service Discovery (Consul, etcd):** Pomáhají službám nalézt a komunikovat s ostatními službami v dynamickém prostředí.
* **Load Balancers (Nginx, HAProxy):** Rozkládají příchozí požadavky mezi více instancí služby.

## 9. Praktická Ukázka: Komunikace mezi Mikroslužbami

Pro ilustraci základních principů distribuovaného zpracování, konkrétně komunikace mezi jednoduchými službami, se můžete podívat na jednoduchý příklad v tomto adresáři.

**Kde příklad najdete:**

* Adresář: `priklad-distrib-zpracovani/` (v rámci této sekce `04_Distribuovane_zpracovani`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad-distrib-zpracovani/README.md`.

**Co příklad ukazuje:**

* Jak definovat a spustit dvě jednoduché, nezávislé služby (např. napsané v Pythonu s Flaskem) pomocí Docker Compose a Kubernetes.
* Jak jedna služba může zavolat API endpoint druhé služby pomocí jejich názvů služeb definovaných v `docker-compose.yml` (Docker Compose se postará o síťové propojení a DNS).
* Základní demonstraci toho, jak mohou komponenty distribuovaného systému spolu komunikovat.

Tento příklad je záměrně jednoduchý, aby se zaměřil na samotný mechanismus komunikace v distribuovaném prostředí spravovaném Dockerem.
