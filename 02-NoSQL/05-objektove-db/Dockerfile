FROM python:3.11-slim-buster  

WORKDIR /app

# Nainstalujeme ZODB a závislosti
RUN pip install --no-cache-dir ZODB zodbpickle persistent

# Zkopírujeme náš skript do kontejneru
COPY init_db.py .
COPY interactive.py .

RUN ["python", "/app/init_db.py"]

# Spustí inter
CMD ["python", "-i", "/app/interactive.py"] 