# Použijeme oficiální Python image
FROM python:3.9-slim

# Nastavíme pracovní adresář
WORKDIR /app

# Zkopírujeme soubor s požadavky a nainstalujeme je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme zbytek aplikace
COPY . .

# Vystavíme port, na kterém Flask aplikace naslouchá
EXPOSE 5000

# Příkaz pro spuštění Flask aplikace
# Použijeme 'flask run' s hostem 0.0.0.0, aby byla aplikace dostupná zvenčí kontejneru
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
