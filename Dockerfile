FROM python:3.8

COPY src /src
WORKDIR /src
RUN pip install pyTelegramBotAPI==4.1.0 hdwallet==1.3.2
