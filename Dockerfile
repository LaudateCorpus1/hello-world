FROM python:3.8.9

ENV PORT=8000

ADD main.py .
ADD requirements.txt .
COPY static/* static/
COPY templates/* templates/

RUN pip3 install -r requirements.txt

ENTRYPOINT gunicorn -b :${PORT} main:app