FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app
COPY ./meme_downloader.py /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "meme_downloader.py"]
