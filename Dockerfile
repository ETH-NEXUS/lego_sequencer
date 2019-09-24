FROM python:3.5-alpine

RUN pip install pipenv

WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install

COPY . /app/

EXPOSE 5000
CMD ./run_alpine_site.sh
