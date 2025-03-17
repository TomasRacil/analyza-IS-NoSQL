# Použijeme oficiální Python image jako základ
FROM python:3.9-slim-buster

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Zkopírujeme soubor app.py do kontejneru
COPY app.py .

# Spustíme app.py při startu kontejneru
CMD ["python", "app.py"]