FROM python:3.9.1

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python", "./__main__.py", "8080" ]
