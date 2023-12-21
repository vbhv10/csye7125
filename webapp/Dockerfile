FROM tiangolo/uvicorn-gunicorn:python3.9
RUN mkdir /webapp
COPY requirements.txt /webapp
WORKDIR /webapp

RUN pip install -r requirements.txt

COPY . /webapp
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


