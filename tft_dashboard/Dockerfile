# Basis-Image für Python
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# Python-Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Restliche Add-on-Dateien kopieren
COPY send_dashboard_data.py .
COPY run.sh .

# Run-Script ausführbar machen
RUN chmod +x run.sh

# Startkommando
CMD [ "/app/run.sh" ]