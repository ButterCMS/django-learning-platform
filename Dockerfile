
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./code/pyproject.toml ./code/poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./code /code/

CMD ["runserver", "localhost:8080"]
