FROM python:3.6-alpine

ADD ./api /api
ADD ./requirements.txt /api

EXPOSE 80

WORKDIR /api

RUN apk update
RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev
RUN cd /api && python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

CMD [ "python", "app.py" ]