## 7. Stream Processing (Zpracování dat v reálném čase)

Zatímco datové sklady a jezera se primárně zaměřují na ukládání a dávkovou analýzu dat (batch processing), mnoho moderních aplikací vyžaduje zpracování dat **okamžitě nebo s velmi nízkou latencí**, jakmile data dorazí. Tento přístup se nazývá **stream processing** nebo zpracování datových toků.

### 7.1 Definice a motivace

*   **Definice:** Stream processing je paradigma zpracování dat, kde jsou data (události) zpracovávána kontinuálně, jakmile jsou generována nebo přijata systémem. Na rozdíl od dávkového zpracování, kde se data nejprve shromáždí a pak zpracují v dávkách, stream processing pracuje s **nekonečnými (unbounded) proudy dat**.
    
*   **Proč stream processing?** Existuje mnoho scénářů, kde je okamžitá reakce na příchozí data klíčová:
    *   **Real-time rozhodování:** Umožňuje reagovat na události okamžitě (např. detekce podvodů při online transakci, dynamická úprava cen v e-shopu, personalizovaná doporučení obsahu na webu v reálném čase).
    *   **Monitorování a alerting:** Sledování metrik systémů (využití CPU, dostupnost služeb), senzorických dat (teplota, tlak v průmyslových zařízeních), logů aplikací a okamžité generování upozornění (alertů) při překročení definovaných prahových hodnot nebo detekci anomálií.
    *   **Analýza aktuálních trendů:** Sledování sentimentu na sociálních sítích v reálném čase, monitorování pohybů na finančních trzích, analýza zpravodajských toků.
    *   **Zpracování IoT dat:** Kontinuální příjem a analýza dat z velkého počtu připojených zařízení (chytré domácnosti, nositelná elektronika, průmyslové senzory).
    *   **Personalizované uživatelské zážitky:** Okamžitá úprava obsahu webové stránky nebo aplikace na základě aktuálního chování uživatele.
        

### 7.2 Základní koncepty stream processingu

Pro pochopení fungování systémů pro zpracování datových toků je důležité znát následující pojmy:

*   **Datový tok (Data Stream / Event Stream):**
    *   Představuje nekonečnou, kontinuální sekvenci datových záznamů (událostí), které jsou uspořádány v čase.
    *   Data v toku jsou typicky neměnná (immutable) – jakmile je událost zaznamenána, už se nemění.
        
*   **Událost (Event):**
    *   Jednotlivý datový záznam v toku.
    *   Obvykle obsahuje:
        *   **Časové razítko (Timestamp):** Kdy událost nastala.
        *   **Klíč (Key) (volitelný):** Pro identifikaci nebo particionování událostí (např. ID uživatele, ID senzoru).
        *   **Hodnota (Payload):** Samotná data události (např. JSON objekt, textová zpráva).
            
*   **Zdroj (Source):**
    
    *   Komponenta, která generuje nebo poskytuje datový tok.
    *   Příklady: Senzory, logy aplikací a serverů, databáze (pomocí Change Data Capture - CDC), fronty zpráv (např. Apache Kafka, RabbitMQ), kliknutí uživatelů na webu.
        
*   **Operátor zpracování (Processing Operator / Transformation):**
    *   Funkce nebo transformace aplikovaná na jeden nebo více datových toků.
    *   Příklady:

        *   **Stateless operace:** Nevyžadují udržování stavu mezi událostmi.
            *   map(): Transformuje každou událost (např. extrakce polí, změna formátu).
            *   filter(): Odstraňuje události, které nesplňují podmínku.
            *   flatMap(): Podobné jako map, ale může vrátit nula, jednu nebo více událostí pro každou vstupní událost.
                
        *   **Stateful operace:** Vyžadují udržování stavu.
            *   reduce() / aggregate(): Agreguje hodnoty v rámci okna nebo klíče.
            *   join(): Spojuje události z více toků na základě klíče a časového okna.
                
*   **Výstup (Sink):**
    *   Cíl, kam jsou výsledky zpracování (nový datový tok nebo agregované hodnoty) odesílány.
    *   Příklady: Jiný datový tok (pro další zpracování), databáze (NoSQL, RDBMS), datový sklad, dashboardy pro vizualizaci, systém pro alerty, externí API.
        
*   **Okno (Window):**
    *   Protože datové toky jsou potenciálně nekonečné, mnoho operací (zejména agregace) se provádí nad omezenými úseky toku nazývanými **okna**. Okna umožňují analyzovat data v definovaných časových nebo počtových intervalech.
        
    *   **Typy oken:**

        *   **Časová (Time-based Windows):**
            *   **Tumbling Windows (Posuvná nepřekrývající se okna):** Tok je rozdělen na fixní, nepřekrývající se časové intervaly (např. každých 5 minut). Každá událost patří právě do jednoho okna.
            *   **Sliding Windows (Klouzavá překrývající se okna):** Okna mají fixní délku, ale posouvají se o kratší interval (délka skluzu). Událost může patřit do více oken. (Např. okno o délce 5 minut, které se posouvá každou 1 minutu).
            *   **Session Windows (Relační okna):** Okna jsou definována dynamicky na základě aktivity. Seskupují události, které nastanou blízko sebe v čase (v rámci definované neaktivity - gap), oddělené delšími obdobími neaktivity. Vhodné pro analýzu uživatelských seancí.
                
        *   **Počítací (Count-based Windows):** Agregují data po obdržení určitého počtu událostí (např. každých 100 událostí).
            
*   **Stav (State):**
    *   Některé streamovací operace (např. agregace v oknech, spojování toků, komplexní zpracování událostí) vyžadují udržování stavu mezi jednotlivými událostmi. Například pro výpočet průměru v okně si systém musí pamatovat součet a počet prvků.
    *   Správa stavu v distribuovaném, škálovatelném a odolném prostředí je jednou z klíčových a nejnáročnějších výzev stream processingu. Frameworky musí zajistit, že stav je konzistentní a obnovitelný i při selhání uzlů.
        
*   **Čas události vs. Čas zpracování (Event Time vs. Processing Time):**
    *   **Event Time:** Časové razítko, kdy událost skutečně nastala ve zdrojovém systému nebo v reálném světě.
    *   **Processing Time:** Čas, kdy je událost zpracována streamovacím systémem (tj. kdy ji systém "vidí").
    *   Mezi těmito časy může být rozdíl (latence sítě, výpadky, zpoždění ve frontách). Pro mnoho analýz je důležité pracovat s **časem události**, aby byly výsledky přesné a nezávislé na zpožděních ve zpracování.
        
    *   Zpracování na základě času události vyžaduje řešení problémů jako jsou:
        *   **Pozdní (late-arriving) události:** Události, které dorazí do systému až poté, co bylo okno, do kterého časově patří, již zpracováno.
        *   **Neuspořádané (out-of-order) události:** Události nemusí přicházet v přesném chronologickém pořadí.
            
    *   **Vodoznaky (Watermarks):** Mechanismus používaný v mnoha streamovacích systémech k odhadu, jak "kompletní" jsou data pro daný čas události, a k rozhodnutí, kdy uzavřít časová okna pro zpracování.
        

### 7.3 Frameworky pro stream processing (přehled)

Existuje několik populárních open-source i komerčních frameworků a platforem pro stream processing:

*   **Apache Kafka Streams:**
    *   Knihovna (nikoli samostatný cluster) pro Javu a Scalu.
    *   Umožňuje vytvářet streamovací aplikace, které čtou data z Apache Kafka témat, zpracovávají je a výsledky zapisují zpět do Kafky nebo jiných systémů.
    *   Nabízí vysokoúrovňové DSL (Domain Specific Language) a nízkoúrovňové Processor API.
    *   Integruje se těsně s ekosystémem Kafka.
        
*   **Apache Flink:**
    *   Výkonný, distribuovaný open-source framework navržený od základu pro **stream-first** zpracování (i když zvládá i dávkové úlohy jako speciální případ streamu).
    *   Poskytuje velmi nízkou latenci a vysokou propustnost.
    *   Nabízí bohaté API v Javě, Scale a Pythonu (PyFlink).
    *   Má pokročilou podporu pro správu stavu, čas událostí, okna a komplexní zpracování událostí (CEP).
    *   Považován za jeden z nejmodernějších a nejvýkonnějších streamovacích enginů.
        
*   **Apache Spark Streaming (starší DStreams API) a Structured Streaming (novější):**
    *   **Spark Streaming (DStreams):** Původní streamovací komponenta Sparku. Zpracovává data v tzv. **mikro-dávkách (micro-batches)** – krátkých časových intervalech (např. sekundy). Není to "pravé" streamování událost po události, ale pro mnoho aplikací je tento přístup dostatečně rychlý a poskytuje dobrý kompromis mezi latencí a propustností.
    *   **Structured Streaming:** Novější API ve Sparku, které je postaveno na Spark SQL enginu a DataFrame/Dataset API. Poskytuje vysokoúrovňové API pro práci se streamy jako s nekonečnými tabulkami. Zjednodušuje vývoj streamovacích aplikací a nabízí lepší integraci s dávkovým zpracováním. Interně také často používá mikro-dávky, ale snaží se poskytovat sémantiku bližší kontinuálnímu zpracování.
        
*   **Apache Samza:**
    *   Distribuovaný streamovací framework původně vyvinutý v LinkedIn.
    *   Často se používá ve spojení s Apache Kafka pro zprávy a Hadoop YARN pro správu zdrojů.
    *   Zaměřuje se na jednoduchost, škálovatelnost a robustní správu stavu.
        
*   **Cloudové služby:**
    *   **Google Cloud Dataflow:** Plně spravovaná služba pro dávkové i streamovací zpracování dat, založená na open-source modelu Apache Beam (který poskytuje unifikované API pro různé enginy).
    *   **Amazon Kinesis:** Sada služeb AWS pro práci se streamovanými daty:
        *   **Kinesis Data Streams:** Pro sběr a ukládání streamů dat.
        *   **Kinesis Data Firehose:** Pro nahrávání streamovaných dat do datových skladů a jezer.
        *   **Kinesis Data Analytics:** Pro analýzu streamovaných dat pomocí SQL nebo Apache Flink.
    *   **Azure Stream Analytics:** Služba Microsoft Azure pro analýzu dat v reálném čase z různých zdrojů.
        

### 7.4 Výzvy stream processingu

Navzdory výhodám přináší stream processing i specifické výzvy:

*   **Správa stavu (State Management):** Udržování stavu v distribuovaném, škálovatelném a odolném prostředí je komplexní. Systém musí zajistit konzistenci stavu a jeho obnovu po selhání.
*   **Zpracování pozdních a neuspořádaných dat (Late and Out-of-Order Data):** Jak korektně zpracovat události, které dorazí se zpožděním nebo v jiném pořadí, než nastaly?
*   **Sémantika zpracování (Processing Semantics):**
    *   **At-most-once:** Každá událost je zpracována nejvýše jednou (může dojít ke ztrátě dat při selhání).
    *   **At-least-once:** Každá událost je zpracována alespoň jednou (může dojít k duplicitnímu zpracování při selhání a obnově).
    *   **Exactly-once:** Každá událost je zpracována právě jednou, i při selháních. Dosažení této sémantiky je nejnáročnější, ale poskytuje nejsilnější záruky.
*   **Škálovatelnost a Odolnost proti chybám:** Systém musí být schopen škálovat podle zátěže a automaticky se zotavit ze selhání uzlů bez ztráty dat nebo konzistence.
*   **Monitoring a Ladění:** Sledování a ladění komplexních, distribuovaných streamovacích pipeline může být obtížné. Je potřeba mít nástroje pro vizualizaci toků dat, sledování latence, propustnosti a detekci úzkých hrdel.
*   **Vývoj a Testování:** Vývoj a testování streamovacích aplikací může být složitější než u dávkových aplikací kvůli jejich kontinuální povaze a závislosti na čase.
*   **Integrace s ostatními systémy:** Zajištění spolehlivé integrace se zdroji dat a výstupy (sinks).
    
Stream processing je dynamicky se rozvíjející oblast, která je nezbytná pro mnoho moderních aplikací zaměřených na analýzu a reakci na data v reálném čase. Výběr správného frameworku a pečlivý návrh architektury jsou klíčové pro úspěšnou implementaci.