FROM python:3.10

WORKDIR /cart-api

COPY requirements/production.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "main:app" ]
