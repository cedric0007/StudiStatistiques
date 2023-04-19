FROM python:3.9

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY Modules/ /StudiStatistiques/Modules/
COPY requirements.txt /StudiStatistiques/requirements.txt
COPY script.sh /StudiStatistiques/script.sh
WORKDIR /StudiStatistiques
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /Modules
ENTRYPOINT ["/bin/sh", "/StudiStatistiques/script.sh"]
EXPOSE 8000

# RUN docker network connect studistatistiques_default python_studi_statistiques

# CMD ["uvicorn", "/StudiStatistiques/Modules/apiStatistiques/app.py", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "apiStatistiques.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "Modules.apiStatistiques:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]]
CMD ["uvicorn", "Modules.apiStatistiques.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

# CMD ["/usr/local/bin/python", "app.py"]
