FROM python:3.10 AS development

WORKDIR /cart-api

COPY requirements/* requirements/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/base.txt

COPY . .

ENTRYPOINT [ "flask", "run" ]

FROM python:3.10

WORKDIR /cart-api

COPY requirements/* requirements/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/production.txt

COPY . .

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.py", "main:app" ]
