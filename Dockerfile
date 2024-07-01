FROM python:3.11-alpine
LABEL authors="Louis Gallet"
LABEL description="Make This Playlist is a web application that allows anyone to add music to a Spotify playlist without needing a Spotify account. The application is accessible at the following address: [Make This Playlist](https://makethisplaylist.louisgallet.fr)."


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 3000


ENTRYPOINT ["python", "main.py"]