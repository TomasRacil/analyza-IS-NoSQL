# Message Queues (Fronty Zpráv)

## 1. Úvod do Front Zpráv

V moderních distribuovaných systémech je často potřeba, aby jednotlivé komponenty (služby, aplikace) spolu komunikovaly. Synchronní komunikace (např. přímé volání REST API nebo RPC), kdy odesílatel čeká na odpověď od příjemce, může vést k několika problémům:

* **Těsné provázání (Tight Coupling):** Odesílatel a příjemce musí být oba dostupní ve stejný čas. Pokud je příjemce dočasně nedostupný nebo přetížený, odesílatel nemůže pokračovat.
* **Škálovatelnost:** Pokud počet požadavků na příjemce náhle vzroste, může dojít k jeho přetížení.
* **Odolnost proti chybám:** Selhání příjemce může přímo ovlivnit odesílatele.
* **Latence:** Odesílatel musí čekat na dokončení operace příjemcem.

**Message Queues (Fronty Zpráv)** nabízejí řešení těchto problémů zavedením **asynchronní komunikace**. Místo přímé komunikace mezi službami se zprávy posílají do fronty, odkud si je příjemci vyzvedávají a zpracovávají ve vlastním tempu.

## 2. Základní Koncepty

* **Zpráva (Message):** Data, která se mají přenést mezi komponentami. Může to být jednoduchý text, JSON, XML, binární data atd. Zpráva obvykle obsahuje tělo (payload) a metadata (např. identifikátor, časové razítko, prioritu).
* **Producent (Producer, Publisher):** Komponenta, která vytváří a odesílá zprávy do fronty.
* **Konzument (Consumer, Subscriber):** Komponenta, která čte (vyzvedává) zprávy z fronty a zpracovává je.
* **Fronta (Queue):** Dočasné úložiště pro zprávy. Zprávy jsou obvykle ukládány v pořadí, v jakém byly přijaty (FIFO - First-In, First-Out), i když některé systémy umožňují i prioritní fronty.
* **Message Broker (Zprostředkovatel Zpráv):** Samotný software, který spravuje fronty, přijímá zprávy od producentů a doručuje je konzumentům. Příklady: RabbitMQ, Apache Kafka, Redis (s funkcionalitou front), Amazon SQS, Google Cloud Pub/Sub.

**Základní workflow:**
1. Producent vytvoří zprávu a pošle ji do specifické fronty (nebo na "exchange" v případě RabbitMQ, která ji pak směruje do front).
2. Message broker uloží zprávu do fronty.
3. Konzument se připojí k frontě a vyzvedne si zprávu ke zpracování.
4. Po úspěšném zpracování zprávy konzument obvykle potvrdí její zpracování (acknowledgement), načež message broker zprávu z fronty odstraní.

## 3. Výhody Použití Front Zpráv

* **Oddělení (Decoupling):** Producenti a konzumenti jsou na sobě nezávislí. Nemusí se znát, nemusí běžet ve stejný čas a mohou být implementováni v různých technologiích. Producentovi stačí vědět, kam poslat zprávu; konzumentovi stačí vědět, odkud zprávy číst.
* **Asynchronní komunikace:** Producent nemusí čekat na zpracování zprávy konzumentem. Může pokračovat ve své práci ihned po odeslání zprávy. To zlepšuje odezvu a propustnost systému.
* **Škálovatelnost:**
    * Lze snadno škálovat počet konzumentů, kteří zpracovávají zprávy z jedné fronty, čímž se zvyšuje rychlost zpracování.
    * Fronta může absorbovat nárazové špičky v zátěži. Pokud producenti generují zprávy rychleji, než je konzumenti stíhají zpracovávat, zprávy se hromadí ve frontě a zpracují se později.
* **Odolnost a Spolehlivost:**
    * Pokud konzument selže, zpráva (pokud nebyla potvrzena) zůstane ve frontě a může být zpracována jiným konzumentem nebo stejným konzumentem po jeho restartu.
    * Message broker může zajistit perzistenci zpráv (ukládání na disk), takže se zprávy neztratí ani při restartu brokera.
* **Rozložení zátěže (Load Balancing):** Pokud více konzumentů čte ze stejné fronty, zátěž se mezi ně automaticky rozkládá.
* **Možnost opakovaného doručení (Retry Mechanisms):** Pokud zpracování zprávy selže, může být nakonfigurováno automatické opakované doručení nebo přesunutí zprávy do speciální "dead-letter queue" (DLQ) pro pozdější analýzu.
* **Řízení toku (Flow Control):** Některé systémy umožňují omezit rychlost, jakou producenti posílají zprávy, aby nedošlo k zahlcení fronty nebo konzumentů.

## 4. Komunikační Vzory (Messaging Patterns)

* **Point-to-Point (Bod-Bod):**
    * Zpráva je odeslána do fronty a je doručena a zpracována **právě jedním** konzumentem.
    * Typické pro úlohy, kde má být každá zpráva zpracována jednou (např. zpracování objednávky).

* **Publish/Subscribe (Pub/Sub, Publikuj/Odebírej):**
    * Producent publikuje zprávu na téma (topic) nebo do "exchange" (v terminologii AMQP/RabbitMQ).
    * Zpráva je doručena **všem** konzumentům, kteří odebírají dané téma nebo jsou navázáni na daný exchange.
    * Každý odběratel obdrží kopii zprávy.
    * Typické pro notifikace, rozesílání událostí, kde více komponent potřebuje reagovat na stejnou událost.

## 5. Příklady Message Brokerů

* **RabbitMQ:**
    * Jeden z nejpopulárnějších open-source message brokerů.
    * Implementuje protokol AMQP (Advanced Message Queuing Protocol), ale podporuje i jiné (MQTT, STOMP).
    * Nabízí flexibilní routing zpráv pomocí "exchanges" a "bindings".
    * Podporuje perzistentní zprávy, potvrzování doručení, prioritní fronty.
    * Vhodný pro širokou škálu aplikací.

* **Apache Kafka:**
    * Distribuovaná streamingová platforma, která se často používá jako vysoce výkonný message broker.
    * Navržena pro zpracování obrovského množství zpráv v reálném čase s vysokou propustností a nízkou latencí.
    * Zprávy jsou organizovány do témat (topics), která jsou rozdělena na partice (partitions) pro škálovatelnost a paralelismus.
    * Ukládá zprávy na disk po definovanou dobu (retention period), což umožňuje jejich opakované čtení.
    * Vhodná pro log aggregation, stream processing, event sourcing, real-time analytics.

* **Redis:**
    * In-memory databáze, která může být použita i jako jednoduchý message broker pomocí svých datových struktur Lists (pro point-to-point fronty) a Pub/Sub příkazů.
    * Velmi rychlý, ale perzistence a pokročilé funkce front mohou být omezenější ve srovnání se specializovanými brokery.
    * Od verze 5.0 nabízí Redis Streams, což je robustnější datová struktura pro implementaci front a logů zpráv.

* **Amazon Simple Queue Service (SQS):**
    * Plně spravovaná služba front zpráv v cloudu AWS.
    * Nabízí standardní a FIFO fronty.
    * Snadno škálovatelná a spolehlivá.

* **Google Cloud Pub/Sub:**
    * Globální, škálovatelná a spolehlivá služba pro zasílání zpráv v reálném čase v Google Cloudu.

* **Apache ActiveMQ:**
    * Další populární open-source message broker, podporuje JMS (Java Message Service) a další protokoly.

## 6. Důležité Aspekty při Návrhu

* **Formát zpráv:** Zvolte vhodný formát (JSON, XML, Protocol Buffers, Avro) s ohledem na velikost, čitelnost a rychlost serializace/deserializace.
* **Idempotence konzumentů:** Konzument by měl být navržen tak, aby opakované zpracování stejné zprávy (např. po selhání a opakovaném doručení) nevedlo k nežádoucím vedlejším efektům.
* **Zpracování chyb a opakované pokusy:** Jak se systém zachová, když konzument selže při zpracování zprávy? Implementujte logiku pro opakované pokusy, případně dead-letter queues (DLQ) pro zprávy, které nelze zpracovat.
* **Potvrzování zpráv (Acknowledgements):** Konzument by měl brokeru potvrdit úspěšné zpracování zprávy, aby ji broker mohl bezpečně odstranit z fronty.
* **Monitoring:** Sledujte délku front, rychlost zpracování, počet chyb atd., abyste mohli identifikovat problémy a optimalizovat výkon.
* **Bezpečnost:** Zabezpečte přístup k message brokeru a šifrujte citlivé zprávy.

## 7. Praktická Ukázka: RabbitMQ s Pythonem

Pro praktickou demonstraci použití front zpráv v adresáři naleznete příklad s **RabbitMQ** jako message brokerem a jednoduchými Python skripty pro producenta a konzumenta.

**Kde příklad najdete:**

* Adresář: `priklad-message-queues-rabbitmq/` (v rámci této sekce `06_Message_Queues`)
* Podrobný popis, strukturu souborů, instrukce ke spuštění a testování naleznete v souboru `priklad-message-queues-rabbitmq/README.md`.

**Co příklad ukáže:**

* Jak spustit RabbitMQ server pomocí Docker Compose.
* Jak napsat Python skript (producent), který odesílá zprávy do fronty v RabbitMQ.
* Jak napsat Python skript (konzument), který přijímá a zpracovává zprávy z fronty.
* Základní principy komunikace přes frontu zpráv.

Tato ukázka vám pomůže pochopit, jak fronty zpráv fungují a jak mohou být použity k vytvoření robustnějších a škálovatelnějších aplikací.
