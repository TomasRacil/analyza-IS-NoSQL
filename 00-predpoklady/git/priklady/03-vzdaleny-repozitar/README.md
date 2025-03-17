# Příklad 03: Vzdálený repozitář (GitHub)

Tento příklad ukazuje, jak pracovat se vzdáleným repozitářem na GitHubu.  Budete potřebovat účet na GitHubu (nebo podobné službě, např. GitLab, Bitbucket).

## Postup

1.  **Vytvořte nový repozitář na GitHubu.**
    *   Přihlaste se do svého účtu na GitHubu.
    *   Klikněte na tlačítko "New" (nebo "+" a "New repository").
    *   Zadejte název repozitáře (např. `muj-git-projekt`).  Můžete přidat i popis.
    *   Zvolte, zda má být repozitář veřejný (Public) nebo soukromý (Private).
    *   *Nezaškrtávejte* možnost "Initialize this repository with a README". Chceme naklonovat *prázdný* repozitář.
    *   Klikněte na tlačítko "Create repository".

2.  **Zkopírujte URL adresu repozitáře.**  Na stránce nově vytvořeného repozitáře najdete URL adresu (HTTPS nebo SSH).  Bude vypadat nějak takto: `https://github.com/<váš_uživatelské_jméno>/muj-git-projekt.git` (HTTPS) nebo `git@github.com:<váš_uživatelské_jméno>/muj-git-projekt.git` (SSH).

3.  **Naklonujte repozitář do svého počítače.**  Otevřete terminál a přejděte do adresáře, kde chcete mít lokální kopii repozitáře.  Pak spusťte:

    ```bash
    git clone <URL_REPOZITARE>
    ```

    (Nahraďte `<URL_REPOZITARE>` skutečnou URL adresou.)

4.  **Přejděte do naklonovaného adresáře:**

    ```bash
    cd muj-git-projekt
    ```

5.  **Vytvořte soubor (nebo zkopírujte soubory z předchozích příkladů), přidejte ho do staging area a commitněte:**

    ```bash
    echo "# Můj Git projekt" > README.md
    git add README.md
    git commit -m "Přidán README.md"
    ```

6.  **Odešlete změny na GitHub (push):**

    ```bash
    git push origin main  # Nebo 'master', pokud je vaše hlavní větev 'master'
    ```

    Git vás může požádat o zadání uživatelského jména a hesla (nebo jiného ověření, pokud používáte SSH).  Po úspěšném push byste měli vidět soubor `README.md` na GitHubu.

7. **Udělejte další změny lokálně, commitněte je a odešlete (push):**
   * Upravte `README.md`
   * `git add README.md`
   * `git commit -m "Update README"`
   * `git push origin main`

8. **Simulace práce jiného uživatele (nebo práce na jiném počítači):**
    *  *Přímo na GitHubu* upravte soubor `README.md` (klikněte na soubor, pak na ikonu tužky).  Přidejte nějaký text a commitněte změnu přímo na GitHubu.

9. **Stáhněte změny z GitHubu do vaší lokální kopie (pull):**

    ```bash
    git pull origin main
    ```

    Tento příkaz stáhne změny ze vzdálené větve `main` (na GitHubu) a sloučí je s vaší lokální větví `main`.  Nyní byste měli mít lokálně stejnou verzi `README.md`, jaká je na GitHubu.

**Důležité poznámky:**

*   **`origin`:**  `origin` je *výchozí* název pro vzdálený repozitář.  Můžete mít více vzdálených repozitářů s různými názvy, ale `origin` je konvence.
*   **`main` (nebo `master`):**  Toto je název hlavní větve.  Nové repozitáře na GitHubu používají `main`, starší mohou používat `master`.  Vždy se ujistěte, že používáte správný název.
*   **SSH vs. HTTPS:**  Pro klonování a push můžete použít buď HTTPS URL, nebo SSH URL.  SSH je bezpečnější a pohodlnější (nemusíte zadávat heslo při každém push), ale vyžaduje nastavení SSH klíčů.
* **Pull Request:** V reálných projektech se změny obvykle neposílají přímo do `main`. Místo toho se vytvoří *Pull Request* (žádost o začlenění) z vaší větve do `main`. To umožňuje ostatním vývojářům zkontrolovat vaše změny a schválit je před sloučením.

Tento příklad pokrývá základní workflow pro práci se vzdáleným repozitářem. V praxi je práce s Gitem a GitHubem mnohem komplexnější, ale toto je dobrý začátek.