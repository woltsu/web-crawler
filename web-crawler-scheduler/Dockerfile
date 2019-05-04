FROM python:3.7-alpine

ARG ROOT_URL

ENV ROOT_URL=$ROOT_URL

EXPOSE 65432

WORKDIR /src

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pip freeze > requirements.txt && \
    pip install -r ./requirements.txt

COPY . .

CMD python3 main.py $ROOT_URL