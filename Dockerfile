FROM python:3.9

WORKDIR /app

COPY requirements/* requirements/

RUN pip3 install -r requirements/development.txt

COPY . .

ENV FLASK_ENV ${FLASK_ENV}
ENV FLASK_DEBUGGER ${FLASK_DEBUGGER}
ENV FLASK_PORT ${FLASK_PORT}
ENV FLASK_DEBUG_PORT ${FLASK_DEBUG_PORT}

ENV MONGODB_NAME ${MONGODB_NAME}
ENV MONGODB_URL ${MONGODB_URL}

ENV X-API ${X-API}
ENV X-API-KEY ${X-API-KEY}

CMD python3 ./main.py
