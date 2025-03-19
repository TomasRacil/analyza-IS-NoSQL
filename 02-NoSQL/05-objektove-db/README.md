# Objektové Databáze

## 1. Objektové Databáze: Teorie

### 1.1 Datový Model

Objektové databáze (Object Databases, ODBMS - Object Database Management Systems) ukládají data ve formě *objektů*, podobně jako v objektově orientovaném programování (OOP).  To znamená, že data nejsou uložena v tabulkách (jako v relačních databázích) ani v jednoduchých párech klíč-hodnota (jako v key-value stores), ale jako instance tříd s atributy a metodami.

*   **Objekt (Object):** Základní jednotka uložení.  Reprezentuje entitu z reálného světa (např. uživatel, produkt, objednávka).  Obsahuje:
    *   **Atributy (Attributes):** Data popisující objekt (např. jméno, věk, adresa uživatele).  Atributy mohou být jednoduché datové typy (čísla, řetězce, booleany) nebo *odkazy na jiné objekty* (tím se vytvářejí vztahy mezi objekty).
    *   **Metody (Methods):** Funkce, které operují s daty objektu (např. metoda pro změnu adresy uživatele, metoda pro výpočet ceny objednávky).  Metody jsou *součástí definice třídy* a jsou uloženy *spolu s daty* v databázi.
*   **Třída (Class):** Šablona pro vytváření objektů.  Definuje atributy a metody, které objekty dané třídy budou mít.  Třídy mohou být organizovány do hierarchie (dědičnost).
*   **Dědičnost (Inheritance):** Třída může *dědit* atributy a metody od jiné třídy (nadřazené třídy, superclass).  To umožňuje znovupoužitelnost kódu a modelování hierarchických vztahů (např. třída `Zaměstnanec` dědí od třídy `Osoba`).
*   **Polymorfismus (Polymorphism):** Schopnost objektů různých tříd reagovat na stejnou metodu různým způsobem.  Např. třídy `Čtverec` a `Kruh` (obě dědící od třídy `Tvar`) mohou mít metodu `obsah()`, ale každá ji bude implementovat jinak.
*   **Zapouzdření (Encapsulation):** Skrývání vnitřní implementace objektu a zpřístupnění pouze rozhraní (metod).
* **Identita Objektu (Object Identity):** Každý objekt má unikátní identifikátor (OID - Object Identifier), který je *nezávislý* na hodnotách jeho atributů.  Dva objekty se stejnými atributy jsou *různé* objekty, pokud mají různé OID.  V relačních databázích se identita obvykle odvozuje od hodnot primárního klíče (který se může změnit).  OID v objektových databázích je *neměnný*.

**Příklad (konceptuální, nejedná se o konkrétní syntaxi):**

```
// Definice tříd
class Osoba {
  atributy:
    jmeno: Řetězec
    vek: Číslo
  metody:
    pozdrav(): Řetězec
}

class Zamestnanec dědí od Osoba {
  atributy:
    pozice: Řetězec
    plat: Číslo
  metody:
    zvysPlat(procento: Číslo)
}

// Vytvoření objektů
osoba1 = new Osoba(jmeno: "Jan Novák", vek: 30)
zamestnanec1 = new Zamestnanec(jmeno: "Eva Dvořáková", vek: 25, pozice: "Programátorka", plat: 50000)

// Použití metod
vypis(osoba1.pozdrav()) // Vypíše "Ahoj, já jsem Jan Novák"
zamestnanec1.zvysPlat(10) // Zvýší plat Evy Dvořákové o 10%
```

### 1.2 Výhody a Nevýhody

**Výhody:**

*   **Přirozené modelování složitých dat:** Objektový model je vhodný pro reprezentaci složitých, hierarchických dat s mnoha vztahy.  Je bližší tomu, jak objekty vnímáme v reálném světě a jak s nimi pracujeme v objektově orientovaném programování.
*   **Znovupoužitelnost kódu (dědičnost, polymorfismus):** Snižuje redundanci kódu a usnadňuje údržbu.
*   **Zapouzdření:**  Zlepšuje modularitu a bezpečnost kódu.
*   **Výkon pro určité typy operací:**  Procházení grafu objektů (navigace mezi propojenými objekty) může být *velmi rychlé*, protože se používají přímé odkazy (OID) místo JOINů (jako v relačních databázích).
*   **Integrita dat:**  Metody definované ve třídách mohou vynucovat integritu dat (např. kontrolovat platnost vstupních hodnot).

**Nevýhody:**

*   **Složitost:**  Objektové databáze mohou být složitější na návrh a správu než relační databáze.
*   **Méně standardizované:**  Neexistuje tak široce přijímaný standardní dotazovací jazyk jako SQL pro relační databáze.  Každý ODBMS má obvykle svůj vlastní dotazovací jazyk (i když existují snahy o standardizaci, např. ODMG, Object Query Language - OQL).
*   **Menší rozšířenost a podpora:**  Objektové databáze jsou méně rozšířené než relační databáze, což může znamenat menší komunitu, méně dostupných nástrojů a menší počet odborníků.
*   **Výkon pro určité typy operací:**  Složité dotazy, které zahrnují agregace a filtrování přes *velké* množství objektů, mohou být *pomalejší* než v relačních databázích (které jsou na tyto typy operací optimalizované).
* **Zralost:** I když se objektové databáze vyvíjejí po desetiletí, některé implementace nemusí být tak robustní a odladěné jako zavedené relační databázové systémy.

### 1.3 Příklady Objektových Databází

*   **db4o (Database for Objects):**  Open-source objektová databáze pro Javu a .NET.  Zaměřená na embedded použití (v mobilních aplikacích, desktopových aplikacích, atd.).  *Poznámka:* db4o je již v režimu údržby a nedoporučuje se pro nové projekty.
*   **ObjectDB:**  Komerční objektová databáze pro Javu.  Podporuje JPA (Java Persistence API) a JDO (Java Data Objects).
*   **ObjectStore:**  Komerční objektová databáze od společnosti Progress Software.
*   **Versant Object Database:** Komerční.
*  **Perst:** Open Source, pro Javu a .NET
* **ZODB (Z Object Database):**  Objektová databáze pro Python. Používaná v Zope aplikačním serveru.

Je důležité poznamenat, že mnoho *moderních* databází kombinuje prvky různých modelů. Například:

*   **PostgreSQL:**  Relační databáze s *objektově-relačními* rozšířeními (podpora uživatelsky definovaných typů, dědičnosti tabulek, atd.).
*   **MongoDB:**  *Dokumentová* databáze (která je někdy považována za podmnožinu objektových databází).  Data jsou uložena v dokumentech (podobných objektům), ale bez metod.

### 1.4 Kdy je objektová databáze lepší volbou než relační?

*   **Složité, hierarchické datové struktury:**  Kde máte mnoho vzájemně propojených objektů s komplexními vztahy (např. CAD systémy, správa dokumentů, multimediální data).
*   **Objektově orientované aplikace:**  Pokud je vaše aplikace napsaná v objektově orientovaném jazyce (Java, C#, Python, atd.), objektová databáze může zjednodušit ukládání a načítání objektů, protože *není potřeba* mapování mezi objekty a relačními tabulkami (tzv. *impedance mismatch*).
*   **Aplikace, kde je důležitá rychlost navigace mezi objekty:**  Procházení grafu objektů je obvykle rychlejší než JOINy v relačních databázích.
*   **Aplikace, kde je potřeba ukládat metody spolu s daty:**  Např. pokud chcete, aby databáze sama prováděla určité výpočty nebo kontroly nad daty.
* **Vývoj her:** Pro správu komplexních herních objektů.
* **Simulace:** Pro modelování komplexních systémů.

**Kdy objektová databáze *není* dobrá volba:**

*   **Jednoduchá data:**  Pokud máte data, která lze snadno reprezentovat v tabulkách, relační databáze je obvykle jednodušší a efektivnější.
*   **Aplikace vyžadující složité dotazy a reporty:**  Relační databáze a SQL jsou pro tyto účely obvykle lepší.
*   **Aplikace, kde je důležitá široká podpora a standardizace:**  SQL a relační databáze jsou mnohem rozšířenější a standardizovanější.
* **Kde potřebujete ACID transakce přes více objektů s vysokou mírou souběžnosti:** I když některé ODBMS transakce podporují, nemusí být tak robustní nebo škálovatelné jako u vyspělých relačních systémů.

## 2. ZODB: Praktický Příklad

Tento příklad ukazuje, jak nastavit a používat ZODB (Z Object Database), objektovou databázi pro Python.  Budeme pracovat s persistentními objekty, transakcemi a základními CRUD (Create, Read, Update, Delete) operacemi.

### 2.1. Struktura a Nastavení

*   **`Dockerfile`:** Definuje obraz Dockeru s Pythonem, ZODB a potřebnými závislostmi.
*   **`docker-compose.yml`:**  Definuje službu `app` pro ZODB a persistentní volume (`zodb_data`), aby se data uchovala mezi spuštěními kontejneru.
*   **`init_db.py`:** Skript pro inicializaci databáze (vytvoření kořenového objektu a vložení několika počátečních objektů).
*   **`interactive.py`:** Skript, který otevírá spojení s databází a předává řízení interaktivnímu Python shellu.  Uživatel tak může přímo pracovat s databází.

**Spuštění:**

1.  **Instalace:** Ujistěte se, že máte nainstalovaný Docker a Docker Compose.
2.  **Přechod do adresáře:** Otevřete terminál a přejděte do adresáře, kde máte soubory `Dockerfile`, `docker-compose.yml`, `init_db.py` a `interactive.py`.
3.  **Sestavení a spuštění:** Spusťte kontejnery pomocí příkazu:

    ```bash
    docker-compose run app
    ```

Tím se spustí interaktivní Python shell s přednačtenými objekty z `interactive.py`.  Nyní můžete začít pracovat s databází.

### 2.2. Interaktivní Práce se ZODB a Vysvětlení

Po spuštění Python shellu máte k dispozici tyto objekty:

*   **`root`:**  Kořenový objekt databáze (typu `PersistentMapping`).  Slouží jako hlavní vstupní bod do databáze.  Můžete si ho představit jako kořenový adresář na disku.
*   **`root.people`:** Persistentní slovník (typu `PersistentMapping`), který obsahuje objekty `john` a `eva`.  Je to jako podadresář v kořenovém adresáři.
*   **`Person`:** Třída definující persistentní objekt "Osoba".
*   **`Employee`:** Třída definující persistentní objekt "Zaměstnanec" (dědí od `Person`).
*   **`transaction`:** Modul pro správu transakcí.  Umožňuje potvrzovat (`commit()`) a rušit (`abort()`) změny.
* **`connection`, `db`, `storage`**: objekty, které zprostředkovávají spojení s databází

**Základní Operace a Koncepty:**

*   **Persistentní Objekty:**  Objekty, které dědí od třídy `persistent.Persistent`, jsou automaticky sledovány ZODB.  Když změníte atribut takového objektu, ZODB tuto změnu zaznamená (ale zatím ji neuloží na disk).

    ```python
    # Příklad:
    print(root.people['john'].age)  # Vypíše věk Johna (např. 30)
    root.people['john'].age = 32    # Změníme věk Johna
    print(root.people['john'].age)  # Vypíše 32 (změna je zatím jen v paměti)
    ```

*   **Transakce:** Změny v persistentních objektech se neukládají hned.  Ukládají se *hromadně* v rámci *transakce*.  Transakci musíte buď *potvrdit* (`transaction.commit()`) – pak se změny trvale uloží, nebo *zrušit* (`transaction.abort()`) – pak se změny zahodí.

    ```python
    # Pokračování předchozího příkladu:
    transaction.commit()  # Uloží změnu věku Johna do databáze
    ```

    ```python
    # Příklad zrušení transakce:
    root.people['john'].name = "John Newname"  # Změníme jméno (jen v paměti)
    transaction.abort()                      # Zrušíme transakci - změna jména se neuloží
    print(root.people['john'].name)             # Vypíše původní jméno (např. "John Doe")
    ```

*   **Vyhledávání v ZODB**

    ZODB je *objektová* databáze, ne relační.  Neexistuje zde SQL.  Vyhledávání probíhá primárně procházením objektů.

    1.  **Přímý Přístup (podle klíče):**

        ```python
        john = root.people['john']  # Pokud známe klíč
        print(john.name)
        ```

    2.  **Iterace a Filtrování:**

        ```python
        # Najít všechny osoby starší 30 let:
        for person in root.people.values():
            if person.age > 30:
                print(person.name)

        # Najít osobu se jménem "Alice":
        for key, person in root.people.items():
            if person.name == "Alice":
                print(f"Found Alice with key: {key}")
                break
        else:
            print("Alice not found")
        ```

    3.  **List Comprehension (stručnější):**

        ```python
        # Seznam jmen osob starších 30 let:
        names = [person.name for person in root.people.values() if person.age > 30]
        print(names)
        ```
    4.  **`OOBTree` Metody**:
        ```python
        #Najít klíče v rozsahu:
        for key in root.people.keys(min='j', max='m'):
        print(key)

        #Získat minimální a maximální hodnotu
        print(root.people.minKey())
        print(root.people.maxKey())

*   **Přidávání a Odebírání Objektů:**  Nový persistentní objekt přidáte do databáze tak, že ho přiřadíte jako hodnotu do kořenového objektu (nebo do jiného persistentního kontejneru, např. `PersistentMapping` nebo `PersistentList`). Objekt smažete pomocí `del`.

    ```python
    # Přidání nového zaměstnance:
    mary = Employee("Mary Smith", 35, "Accountant", 60000)
    root.people['mary'] = mary  # Tím se Mary stane persistentní
    transaction.commit()

    # Smazání zaměstnance:
    del root.people['mary']
    transaction.commit()
    ```

*   **Vztahy mezi Objekty:** Objekty na sebe mohou odkazovat.

    ```python
    # Přidání Johna jako přítele Evy:
    root.people['john'].friends.append(root.people['eva'])
    transaction.commit()

    print(root.people['john'].friends) #Vypíše list přátel
    ```

* **Použití `OOBTree`:** OOBTree je další persistentní typ, který umožňuje efektivnější práci s velkým množstvím záznamů a umí řadit data
  ```python
  # zmena root.people na OOBTree
  root.people = OOBTree()
  #Vložení dat
  john = Person("John Doe", 30)
  root.people['john'] = john
  # iterace
  for key in root.people.keys():
    print(key)
  transaction.commit()
  ```
*   **Dědičnost (Inheritance):**  `Employee` dědí od `Person`, takže má všechny atributy a metody jako `Person`, a navíc své vlastní (např. `position` a `salary`).

    ```python
    print(root.people['eva'].position)  # Můžeme přistupovat k atributům specifickým pro Employee
    ```
* **Uzavření spojení:**
  ```python
  connection.close()
  db.close()
  storage.close()
  ```
  
**Důležité poznámky:**

*   ZODB je *objektová* databáze. Nepracujete s tabulkami a SQL, ale s *objekty* a jejich *atributy*.
*   Persistentní objekty musí dědit od `persistent.Persistent`.
*   Změny se neukládají hned, ale až po `transaction.commit()`.
*   `transaction.abort()` zahodí všechny neuložené změny.

## Úkoly

Vyzkoušejte si následující úkoly v interaktivním shellu.  Nezapomeňte *vždy* potvrdit transakci (`transaction.commit()`) po provedení změn, které chcete uložit.

1.  **Základní Manipulace:**
    *   Změňte věk Johna na 33 let.
    *   Přidejte do adresy Johna PSČ (zip code).
    *   Vytvořte novou osobu (objekt `Person`) jménem "Alice" s věkem 25 let a uložte ji do `root.people` pod klíčem 'alice'.
    *   Vytvořte nového zaměstnance (objekt `Employee`) a uložte ho.
    *   Zvyšte plat existujícího zaměstnance o 5%.
    *   Smažte Alici z databáze.
    *   Vypište jména všech osob a zaměstnanců v databázi. (Můžete použít cyklus `for key in root.people: ...`).

2.  **Práce se Vztahy:**
    *   Přidejte Alici (pokud jste ji smazali, vytvořte ji znovu) do seznamu přátel Johna.
    *   Ověřte, že je Alice v seznamu přátel Johna.
    *   Odeberte Alici ze seznamu přátel Johna.

3.  **Experimentování s Transakcemi:**
    *   Změňte jméno Johna, ale *nepotvrzujte* transakci.  Ověřte, že změna *není* uložena (např. zavřete a znovu otevřete Python shell – viz instrukce ke znovuspuštění níže).
    *   Zkuste vyvolat chybu (např. dělení nulou) *uvnitř* transakce a sledujte, co se stane. Změny by se neměly uložit.

4.  **Použití `OOBTree`:**
    * Změňte typ `root.people` na `OOBTree`.
    * Vložte několik nových záznamů.
    * Vypište klíče seřazené podle abecedy.
    * Zjistěte minimální a maximální klíč.

5.  **Vlastní Třídy:**
    *   Vytvořte vlastní persistentní třídu (např. `Product` s atributy `name`, `price`, `description`).
    *   Vytvořte instanci této třídy a uložte ji do databáze.
    *   Ověřte, že se data správně uložila a načetla.

6. **Znovunačtení dat:**
      * Ukončete Python shell (`exit()`).
      * Znovu se připojte ke kontejneru (`docker run app`).
      * Ověřte, že všechny změny provedené a uložené v předchozích krocích jsou stále v databázi.

7.  **Vyhledávání:**
    *   Najděte všechny osoby jménem "John Doe".
    *   Najděte všechny osoby starší 30 let.
    *   Najděte všechny zaměstnance s platem nad 60000.
    *   Najděte osobu/zaměstnance podle klíče, který zadá uživatel (můžete použít `input()` – ale *mimo* kontejner, v *běžném* terminálu; pak hodnotu zkopírujte do interaktivního shellu v kontejneru).

8. **Vyčištění databáze (volitelné):**
    *  Pokud chcete databázi "vyčistit" a začít znovu, můžete smazat soubor `mydata.fs` a `mydata.fs.index` (v kontejneru) a znovu spustit `init_db.py`. Nezapomeňte, že tím *trvale* smažete všechna data! Toto *není* nutné pro plnění úkolů. Je to jen pro případ, že byste chtěli databázi "resetovat".

        ```bash
        # V kontejneru:
        rm /app/mydata.fs /app/mydata.fs.index /app/mydata.fs.tmp /app/mydata.fs.lock
        python init_db.py
        ```

9. **Diskuze:**
    *   **Kdy ne ZODB?** Uveďte příklady situací, kdy byste *nepoužili* ZODB a proč (zvolili byste relační, nebo jinou NoSQL databázi?).
    *   **Výhody a Nevýhody:** Jaké jsou *největší* výhody a nevýhody ZODB?
    *   **Objektový vs. Relační:** V čem se *zásadně* liší práce s objektovou a relační databází?
    *   **ZODB a Web:** Je ZODB vhodná pro moderní webové aplikace? Proč ano/ne?

