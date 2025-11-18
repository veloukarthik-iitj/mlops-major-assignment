# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY . /app

# Expose port
EXPOSE 5000

# Recommended: use gunicorn in production, here simple flask run
CMD ["python", "app.py"]
