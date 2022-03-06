FROM python:3.8

WORKDIR /app/

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY db/ /db/
COPY assets /assests/
COPY app.py /

CMD [ "python", "-m", "app" ]
