# Použijeme oficiální Python image
FROM python:3.9-slim

# Nastavíme pracovní adresář
WORKDIR /app

# Zkopírujeme soubor s požadavky a nainstalujeme je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme zbytek aplikace
COPY . .

# Příkaz pro spuštění aplikace
CMD ["flask", "run", "--host=0.0.0.0"]
