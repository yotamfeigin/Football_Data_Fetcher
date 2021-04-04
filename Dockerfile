FROM python:3.7


ADD CantContain.py .

RUN pip install psycopg2 fire

CMD ["python","./CantContain.py"]

