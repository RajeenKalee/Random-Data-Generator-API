FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir requests
COPY ElasticShipper.py /app/ElasticShipper.py
CMD ["python", "/app/ElasticShipper.py"]