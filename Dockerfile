FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV BASE_URL=http://localhost:5151

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "api:app"]
