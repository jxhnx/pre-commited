FROM continuumio/miniconda3

WORKDIR /app

ADD . /app

RUN pip install cookiecutter pre-commit pytest pytest-order

CMD [ "pytest", "-m", "default" ]
