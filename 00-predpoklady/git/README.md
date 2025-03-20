# Git: Teorie a základy

Tento dokument poskytuje úvod do Gitu, systému pro správu verzí (version control system - VCS). Git je nezbytný nástroj pro moderní vývoj softwaru, který umožňuje sledovat změny v kódu, spolupracovat s ostatními vývojáři a vracet se k předchozím verzím projektu.

## Co je správa verzí?

Správa verzí je systém, který zaznamenává změny souborů v průběhu času. Umožňuje vám:

*   **Vrátit se k libovolné předchozí verzi souboru nebo celého projektu.**
*   **Zjistit, kdo, kdy a proč provedl změny.**
*   **Porovnávat změny mezi verzemi.**
*   **Vytvářet větve (branches) pro experimentování s novými funkcemi, aniž byste ovlivnili hlavní kód.**
*   **Slučovat (merge) změny z různých větví.**
*   **Spolupracovat s ostatními na stejném projektu.**

## Proč Git?

Existuje mnoho systémů pro správu verzí, ale Git je zdaleka nejoblíbenější a nejrozšířenější.  Zde jsou některé jeho výhody:

*   **Distribuovaný:**  Každý vývojář má *kompletní kopii* repozitáře (včetně celé historie). To znamená, že můžete pracovat offline a sdílet změny s ostatními, až budete online.
*   **Rychlý:** Git je velmi rychlý, i u velkých projektů.
*   **Škálovatelný:**  Git zvládne i velmi velké projekty s mnoha vývojáři.
*   **Flexibilní:** Git podporuje různé pracovní postupy (workflows).
*   **Bezpečný:** Git používá kryptografické hashovací funkce k zajištění integrity dat.
*   **Open source:** Git je open source a zdarma k použití.
*   **Široká podpora:**  Git je podporován mnoha nástroji a službami (GitHub, GitLab, Bitbucket, atd.).

## Základní pojmy

*   **Repozitář (Repository):**  Repozitář je adresář, který obsahuje všechny soubory projektu a celou jeho historii verzí.  V Gitu je repozitář reprezentován skrytým adresářem `.git` uvnitř kořenového adresáře projektu.
*   **Commit:**  Commit je snímek (snapshot) stavu projektu v určitém okamžiku.  Každý commit má unikátní identifikátor (hash), zprávu (commit message) popisující provedené změny a odkaz na předchozí commit (nebo commity).
*   **Větev (Branch):**  Větev je pojmenovaná linie vývoje.  Ve výchozím stavu má každý repozitář jednu hlavní větev (obvykle nazvanou `main` nebo `master`).  Můžete vytvářet další větve pro vývoj nových funkcí nebo opravy chyb, aniž byste ovlivnili hlavní větev.
*   **Ukazatel HEAD:**  HEAD je speciální ukazatel, který ukazuje na aktuální commit (tj. na commit, na kterém právě pracujete).
*   **Pracovní adresář (Working Directory):**  Pracovní adresář je váš lokální adresář, kde máte soubory projektu, se kterými pracujete.
*   **Staging Area (Index):**  Staging area je mezistupeň mezi pracovním adresářem a repozitářem.  Přidáváte do ní soubory (nebo změny v souborech), které chcete zahrnout do příštího commitu.  Je to jako "přípravná zóna" pro commit.
*   **Vzdálený repozitář (Remote Repository):**  Vzdálený repozitář je repozitář, který je uložen na jiném počítači (např. na serveru GitHubu).  Slouží ke sdílení kódu s ostatními a k zálohování.
*   **Klonování (Cloning):**  Klonování je proces vytvoření lokální kopie vzdáleného repozitáře.
*   **Push:**  Push je odeslání vašich lokálních commitů do vzdáleného repozitáře.
*   **Pull:**  Pull je stažení změn ze vzdáleného repozitáře do vaší lokální kopie.
*   **Fetch:** Fetch stáhne metadata o změnách ve vzdáleném repozitáři, ale *neaplikuje* je na vaši lokální pracovní kopii.
*   **Merge:**  Merge je sloučení změn z jedné větve do druhé.
*   **Konflikt (Conflict):**  Konflikt nastane, když se dva vývojáři pokusí změnit stejnou část souboru různým způsobem.  Git nedokáže automaticky rozhodnout, která verze je správná, a konflikt musí vyřešit ručně vývojář.
* **.gitignore:** Soubor, který specifikuje soubory a adresáře, které má Git ignorovat (tj. nesledovat jejich změny). Typicky se do .gitignore přidávají dočasné soubory, soubory generované build systémem, soubory s hesly, atd.

## Instalace Gitu

**Windows:**

1.  **Stáhněte si instalační program** z oficiálních stránek: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2.  **Spusťte instalační program** a postupujte podle instrukcí.  Většinou můžete ponechat výchozí nastavení.  Doporučuji ale vybrat si editor, který znáte (např. Notepad++, VS Code), pokud se vás na to instalátor zeptá.
3.  **Ověřte instalaci:** Otevřete příkazový řádek (Command Prompt nebo PowerShell) a zadejte příkaz `git --version`. Měla by se vypsat verze Gitu.

**macOS:**

*   **Pomocí Homebrew (doporučeno):**
    1.  Pokud nemáte Homebrew, nainstalujte ho: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    2.  Nainstalujte Git: `brew install git`
*   **Pomocí instalačního programu:**
    1.  Stáhněte si instalační program z oficiálních stránek: [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
    2.  Spusťte instalační program a postupujte podle instrukcí.
* **Xcode Command Line Tools**: Obsahují git, ale je dobré mít aktuální verzi.

**Linux:**

*   **Použijte správce balíčků vaší distribuce.**
    *   **Debian/Ubuntu:** `sudo apt update && sudo apt install git`
    *   **Fedora:** `sudo dnf install git`
    *   **CentOS/RHEL:** `sudo yum install git`
    *   **Arch Linux:** `sudo pacman -S git`
    *   **(Další distribuce):**  Použijte příslušný příkaz pro vaši distribuci.

**Ověření instalace (všechny platformy):**

Otevřete terminál (nebo příkazový řádek) a zadejte:

```bash
git --version
```

Měla by se vypsat nainstalovaná verze Gitu.

## Základní konfigurace

Po instalaci je dobré nastavit své jméno a e-mailovou adresu. Git tyto informace používá pro identifikaci autora commitů.

```bash
git config --global user.name "Vaše Jméno"
git config --global user.email "[e-mailová adresa byla odstraněna]"
```

*   `--global`:  Toto nastavení platí pro všechny vaše repozitáře.  (Můžete mít i specifická nastavení pro jednotlivé repozitáře, ale to teď nepotřebujeme.)

Můžete si také nastavit výchozí textový editor, který bude Git používat pro editaci commit zpráv:

```bash
git config --global core.editor "code --wait"  # Pro VS Code
# NEBO
git config --global core.editor "nano -w"       # Pro Nano
# NEBO
git config --global core.editor "vim"          # Pro Vim
```
Pokud tento krok přeskočíte, Git použije výchozí systémový editor (což může být Vim, a ten nemusí být pro začátečníky úplně intuitivní).

## Základní workflow

1.  **Inicializace repozitáře:**
    *   Vytvořte nový adresář pro váš projekt (nebo přejděte do existujícího).
    *   Otevřete terminál a přejděte do tohoto adresáře.
    *   Spusťte příkaz `git init`.  Tím vytvoříte nový, prázdný Git repozitář (skrytý adresář `.git`).

    ```bash
    mkdir muj-projekt
    cd muj-projekt
    git init
    ```

2.  **Přidání souborů do staging area:**
    *   Vytvořte nebo upravte soubory ve vašem pracovním adresáři.
    *   Přidejte soubory (nebo změny v souborech) do staging area pomocí příkazu `git add`.

    ```bash
    # Přidání jednoho souboru:
    git add soubor.txt

    # Přidání všech změněných souborů:
    git add .

    # Přidání všech souborů v určitém adresáři:
    git add adresar/
    ```

3.  **Vytvoření commitu:**
    *   Uložte změny ze staging area do repozitáře pomocí příkazu `git commit`.
    *   Přidejte smysluplnou zprávu k commitu (commit message), která popisuje provedené změny.

    ```bash
    git commit -m "Přidán soubor soubor.txt"
    # NEBO (otevře se textový editor):
    git commit
    ```
    Použití `-m` je rychlejší pro krátké zprávy. Pokud nepoužijete `-m`, Git otevře váš výchozí textový editor, kde můžete napsat delší zprávu.  Dobrá commit zpráva by měla být stručná, výstižná a popisovat *proč* byly změny provedeny, ne jen *co* bylo změněno.

4.  **Prohlížení historie:**
    *   Zobrazte historii commitů pomocí příkazu `git log`.

    ```bash
    git log
    git log --oneline  # Zobrazí každý commit na jednom řádku
    git log --graph --oneline --all #Zobrazí graf historie všech větví
    git log -p #Zobrazí diff (rozdíl) pro každý commit
    ```

5.  **Vytvoření větve:**

     ```bash
      git branch nova-funkce #Vytvoří větev
      git checkout nova-funkce #Přepne do dané větve
      #NEBO
      git checkout -b nova-funkce #Vytvoří a rovnou přepne do nové větve
     ```

6. **Přepnutí zpět do main:**
    ```bash
    git checkout main
    ```

7.  **Sloučení (Merge):**
    ```bash
    git merge nova-funkce #Sloučí změny z větve nova-funkce do aktuální větve
    ```

8. **Práce se vzdáleným repozitářem (GitHub, GitLab, atd.):**

    *   **Klonování:**
        ```bash
        git clone <URL_REPOZITARE>
        ```

    *   **Přidání vzdáleného repozitáře:**
        ```bash
        git remote add origin <URL_REPOZITARE>  # 'origin' je obvyklý název pro vzdálený repozitář
        ```

    * **Odeslání změn (push):**
        ```bash
        git push origin main  # Odešle commity z lokální větve main do vzdálené větve main
        ```

    *   **Stažení změn (pull):**
        ```bash
        git pull origin main # Stáhne a sloučí změny ze vzdálené větve main do lokální větve main
        ```

## Příklady

V adresáři `priklady` naleznete několik jednoduchých příkladů, které ilustrují základní použití Gitu.

*   **`01-zaklady`:**  Inicializace repozitáře, přidání souborů, commit, prohlížení historie.
*   **`02-vetveni`:**  Vytvoření větve, přepínání mezi větvemi, sloučení.
*   **`03-vzdaleny-repozitar`:** Klonování, push, pull (tento příklad bude vyžadovat účet na GitHubu nebo podobné službě).

Projděte si tyto příklady a vyzkoušejte si je.