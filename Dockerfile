FROM python:3.6-alpine

ADD ./ /api

EXPOSE 80

WORKDIR /api

RUN apk update
RUN apk add postgresql-libs libev-dev
RUN apk add --virtual .build-deps gcc g++ musl-dev postgresql-dev libffi-dev
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

CMD [ "python", "app.py" ]