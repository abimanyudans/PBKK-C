FROM python:3.11-slim

WORKDIR /app

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh app
COPY . .

# Expose port (Railway akan override dengan $PORT)
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
