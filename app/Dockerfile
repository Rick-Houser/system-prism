FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
EXPOSE 5000 8000
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--timeout=60", "app:app"]