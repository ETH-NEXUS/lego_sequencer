FROM python:3.12-slim

RUN pip install pipenv

WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --deploy --ignore-pipfile

COPY . /app/

EXPOSE 5000
CMD ["pipenv", "run", "./run_alpine_site.sh"]