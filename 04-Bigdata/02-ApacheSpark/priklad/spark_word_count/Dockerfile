# Použijeme oficiální Python image jako základ
FROM python:3.10-slim

# Nainstalujeme Javu (potřebnou pro Spark) a procps (pro příkaz 'ps')
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk-headless procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Nastavíme JAVA_HOME environmentální proměnnou pro OpenJDK 17
# Přesná cesta se může lišit, ale toto je běžná cesta pro Debian-based systémy
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# Přidáme Javu do PATH, aby ji Spark našel
ENV PATH=$JAVA_HOME/bin:$PATH


# Nastavíme pracovní adresář
WORKDIR /app

# Nainstalujeme PySpark
# Je důležité, aby verze PySpark byla kompatibilní s verzí Sparku v clusteru
# Pro Spark 3.x.x je vhodná PySpark 3.x.x
RUN pip install pyspark==3.5.6

# Zkopírujeme adresář aplikace (obsahující skript a data)
COPY ./app /app

# Výchozí příkaz při spuštění kontejneru (nepotřebujeme, protože příkaz specifikujeme v docker-compose.yml)
# CMD ["python", "word_count.py"]