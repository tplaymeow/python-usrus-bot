FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

# install google chrome
RUN apt update && apt install -y gnupg2 && apt install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

RUN mkdir app
WORKDIR app

RUN apt update && apt install -y ffmpeg

ENV POETRY_VERSION 1.6.1
RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false  \
    && poetry install --only main --no-interaction --no-ansi

COPY python_usrus_bot /app/python_usrus_bot/

ENTRYPOINT python python_usrus_bot/main.py