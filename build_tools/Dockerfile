FROM ubuntu:18.04
MAINTAINER Nadav Ruskin "ruskin.nadav@gmail.com"

RUN apt-get update -y && \
    apt-get install -y curl python3-pip python3-dev gunicorn3 unzip xvfb libxi6 libgconf-2-4 && \
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chown root:root /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver 

WORKDIR /emailvalidator
COPY build_tools/emailvalidator_requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY emailvalidator .
COPY build_tools/entrypoint.sh .
CMD ["./entrypoint.sh"]
