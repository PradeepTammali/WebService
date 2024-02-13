FROM python:3.11.5-alpine

WORKDIR /app
ADD . /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    apk del .build-deps gcc musl-dev


HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
        CMD wget --quiet --tries=1 --spider http://localhost:8000/api/health_check || exit 1


EXPOSE 8000

CMD ["gunicorn", "run:app"]
