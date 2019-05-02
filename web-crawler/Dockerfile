FROM python:3.7-alpine

WORKDIR /src

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pip freeze > requirements.txt && \
    pip install -r ./requirements.txt

COPY . .

CMD python3 main.py