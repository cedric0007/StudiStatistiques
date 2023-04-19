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
WORKDIR /StudiStatistiques
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /Modules

EXPOSE 8001

# CMD ["/usr/local/bin/python", "app.py"]
