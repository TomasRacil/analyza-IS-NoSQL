# Použijeme oficiální Node.js image jako základ.
# Doporučuje se používat konkrétní verzi LTS (Long Term Support) pro stabilitu.
FROM node:18-alpine

# Nastavíme pracovní adresář uvnitř kontejneru.
# Všechny následující příkazy (COPY, RUN, CMD) budou relativní k tomuto adresáři.
WORKDIR /usr/src/app

# Nainstalujeme express, který je závislost projektu pommocí 'npm i'.
RUN npm i express

# Zkopírujeme zbytek kódu aplikace do pracovního adresáře v kontejneru.
COPY . .

# Vystavíme port, na kterém aplikace naslouchá uvnitř kontejneru.
# Tento port pak mapujeme v docker-compose.yml na port hostitelského systému.
EXPOSE 3000

# Příkaz, který se spustí při startu kontejneru.
# Spustí Node.js aplikaci pomocí skriptu definovaného v package.json (obvykle "start").
CMD [ "node", "index.js" ]
