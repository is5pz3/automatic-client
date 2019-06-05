FROM python:3.6
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . code
WORKDIR code

CMD python scripts/app.py 900 120 https://monitor-prodd.herokuapp.com https://monitor2-prodd.herokuapp.com
