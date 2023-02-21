FROM python:3.10 AS cart-api.development

WORKDIR /cart-api

COPY requirements/* requirements/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/development.txt

COPY . .

FROM cart-api.development AS cart-api.production

WORKDIR /cart-api
RUN pip3 install -r requirements/production.txt

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "main:app" ]

FROM cart-api.development AS cart-api.tests

WORKDIR /cart-api
RUN pip3 install -r requirements/tests.txt
