FROM python:3.10-slim
RUN mkdir /app
COPY app.py /app
COPY requirements.txt /app
COPY dataapi.py /app
COPY data.csv /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python /app/app.py
