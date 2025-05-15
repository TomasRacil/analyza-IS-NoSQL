# Replikace Dat

## 1. Úvod do Replikace

Replikace dat je proces vytváření a udržování více kopií stejných dat na různých serverech (uzlech) nebo v různých datových centrech. Hlavním cílem replikace je zajistit:

* **Vysokou dostupnost (High Availability):** Pokud jeden server selže, data jsou stále dostupná z ostatních replik. Systém tak může pokračovat v provozu s minimálním nebo žádným výpadkem.
* **Odolnost proti chybám (Fault Tolerance):** Systém je schopen odolat selhání jednoho nebo více svých komponent (serverů s daty).
* **Škálovatelnost čtení (Read Scalability):** Čtecí operace mohou být rozloženy mezi více replik, čímž se snižuje zátěž primárního serveru a zvyšuje se celková propustnost pro čtení.
* **Zotavení po havárii (Disaster Recovery):** Repliky v geograficky odlišných lokalitách mohou sloužit k obnově dat v případě rozsáhlé havárie (např. přírodní katastrofa postihující celé datové centrum).
* **Snížení latence pro geograficky rozložené uživatele:** Uživatelé mohou přistupovat k datům z geograficky bližší repliky, což snižuje dobu odezvy.

## 2. Základní Koncepty Replikace

* **Master (Primární uzel, Zdroj):** Server, který přijímá operace zápisu (CREATE, UPDATE, DELETE). Změny provedené na masteru jsou následně propagovány na slave uzly.
* **Slave (Sekundární uzel, Replika, Cíl):** Server, který přijímá kopie dat z masteru. Obvykle slouží pro čtecí operace. V některých konfiguracích mohou i slave uzly přijímat zápisy, což ale může vést ke konfliktům.
* **Protokol replikace:** Definice způsobu, jakým se změny z masteru přenášejí na slave(s).
* **Synchronizace:** Proces udržování konzistence dat mezi masterem a slave(s).

## 3. Typy Replikace

### Podle směru toku dat:

* **Master-Slave Replikace (Primární-Sekundární):**
    * Jeden master uzel přijímá všechny zápisy.
    * Jeden nebo více slave uzlů replikuje data z masteru.
    * Slave uzly jsou typicky read-only (pouze pro čtení), aby se předešlo konfliktům.
    * **Výhody:** Jednoduchost, jasně definovaný tok dat.
    * **Nevýhody:** Master je jediným bodem selhání pro zápisy (single point of failure for writes). Pokud master selže, je potřeba proces "failover" (povýšení slavea na nového mastera), který může být manuální nebo automatický (např. pomocí nástrojů jako Redis Sentinel, Patroni pro PostgreSQL).

* **Master-Master Replikace (Více-Masterů, Aktivní-Aktivní):**
    * Více master uzlů, z nichž každý může přijímat zápisy.
    * Změny provedené na jednom masteru se replikují na ostatní mastery.
    * **Výhody:** Vyšší dostupnost pro zápisy (pokud jeden master selže, ostatní mohou stále přijímat zápisy), lepší rozložení zátěže pro zápisy.
    * **Nevýhody:** Mnohem složitější na implementaci a správu. Hlavním problémem je **řešení konfliktů zápisu** (write conflicts) – co se stane, když dva různí uživatelé současně upraví stejná data na různých masterech? Vyžaduje robustní mechanismy pro detekci a řešení konfliktů.

### Podle způsobu synchronizace:

* **Synchronní replikace:**
    * Operace zápisu na masteru je považována za dokončenou až poté, co je potvrzeno, že data byla úspěšně zapsána na *všechny* (nebo definovaný počet) slave uzly.
    * **Výhody:** Zaručuje silnou konzistenci dat mezi masterem a slavem. Žádná ztráta dat při selhání masteru (pokud alespoň jeden slave stihl potvrdit zápis).
    * **Nevýhody:** Vyšší latence zápisu (master musí čekat na potvrzení od slaveů). Pokud je některý slave pomalý nebo nedostupný, může to zpomalit nebo zablokovat zápisy na masteru.

* **Asynchronní replikace:**
    * Operace zápisu na masteru je považována za dokončenou ihned po zapsání na mastera. Data se na slave(s) replikují "na pozadí" s určitým zpožděním.
    * **Výhody:** Nižší latence zápisu na masteru. Master není blokován slave uzly.
    * **Nevýhody:** Možnost ztráty dat (pokud master selže dříve, než se změny stihnou zreplikovat na slave). Slave může mít dočasně neaktuální data (eventual consistency).

* **Polosynchronní replikace (Semi-synchronous):**
    * Kombinace synchronní a asynchronní replikace.
    * Master čeká na potvrzení od *alespoň jednoho* slavea, než operaci zápisu považuje za dokončenou. Ostatní slave uzly se mohou synchronizovat asynchronně.
    * **Výhody:** Lepší kompromis mezi konzistencí a výkonem než čistě synchronní nebo asynchronní přístup. Snižuje riziko ztráty dat oproti asynchronní replikaci.
    * **Nevýhody:** Stále může mít vyšší latenci než asynchronní replikace.

## 4. Konzistence a CAP Teorém

Replikace úzce souvisí s **CAP teorémem**, který říká, že v distribuovaném systému je nemožné současně zaručit všechny tři následující vlastnosti:
* **Consistency (Konzistence):** Všechny uzly vidí stejná data ve stejný okamžik.
* **Availability (Dostupnost):** Každý požadavek obdrží odpověď (i když nemusí obsahovat nejaktuálnější data).
* **Partition Tolerance (Odolnost vůči rozdělení sítě):** Systém funguje i v případě, že dojde k výpadku komunikace mezi uzly.

V praxi je odolnost vůči rozdělení sítě (P) nutností. Proto se systémy obvykle rozhodují mezi:
* **CP (Consistency + Partition Tolerance):** Preferuje konzistenci před dostupností. V případě síťového rozdělení může systém přestat přijímat zápisy, aby zajistil konzistenci. Synchronní replikace se blíží tomuto modelu.
* **AP (Availability + Partition Tolerance):** Preferuje dostupnost před konzistencí. Systém zůstane dostupný i při síťovém rozdělení, ale některé uzly mohou mít dočasně neaktuální data. Asynchronní replikace se blíží tomuto modelu.

## 5. Výzvy Replikace

* **Latence replikace (Replication Lag):** Zpoždění mezi zápisem na mastera a jeho zobrazením na slaveu (zejména u asynchronní replikace).
* **Řešení konfliktů (Conflict Resolution):** U master-master replikace nebo pokud je povoleno zapisovat na slave uzly.
* **Failover a Failback:** Proces přepnutí na záložní uzel (failover) a návrat k původnímu masteru po jeho obnově (failback).
* **Správa a monitoring:** Sledování stavu replikace, výkonu a konzistence.
* **Náklady na infrastrukturu:** Provozování více serverů.

## 6. Replikace v Různých Databázových Systémech

* **Relační databáze (např. PostgreSQL, MySQL):**
    * Typicky podporují master-slave replikaci (streamovací replikace, log shipping).
    * Existují i řešení pro master-master (např. Galera Cluster pro MySQL/MariaDB, nebo pomocí externích nástrojů).
* **NoSQL databáze:**
    * **MongoDB:** Podporuje "replica sets" (master-slave s automatickým failoverem).
    * **Redis:** Podporuje master-slave replikaci. Pro automatický failover se používá Redis Sentinel. Redis Cluster poskytuje sharding i replikaci.
    * **Cassandra:** Distribuovaná databáze, kde je replikace základním prvkem architektury (bez explicitního mastera, data jsou replikována na více uzlů podle replikačního faktoru).
    * **CouchDB:** Podporuje master-master replikaci (eventual consistency).

## 7. Praktická Ukázka: Redis Master-Slave Replikace

Pro praktické vyzkoušení konceptu replikace najdete v adresáři jednoduchý příklad nastavení Master-Slave replikace pro Redis pomocí Docker Compose.

**Kde příklad najdete:**

* Adresář: `priklad_redis_replikace/` (v rámci této sekce `03_Replikace`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad_redis_replikace/README.md`.

**Co příklad ukazuje:**

* Jak nakonfigurovat jednu Redis instanci jako master.
* Jak nakonfigurovat druhou Redis instanci jako slave, která replikuje data z mastera.
* Jak ověřit, že zápisy provedené na masteru jsou viditelné na slaveu.
* Jak slave instance ve výchozím stavu odmítá operace zápisu.

Tento příklad vám pomůže pochopit základní principy replikace a jak ji lze jednoduše nastavit v kontejnerizovaném prostředí.
