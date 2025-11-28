FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and static files
COPY app.py .
COPY static ./static

EXPOSE 5000

# Run via gunicorn (production-style)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
