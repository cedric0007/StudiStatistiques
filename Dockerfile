FROM python:3.9

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Télécharger et installer ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Installer les dépendances Python
COPY Modules/ /OrisonCaptain/Modules/
COPY requirements.txt /OrisonCaptain/requirements.txt
WORKDIR /OrisonCaptain
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /Modules

# CMD ["/usr/local/bin/python", "app.py"]
