FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run with Gunicorn: 4 workers x 2 threads = 8 concurrent requests
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "5", "--threads", "2", "--timeout", "300"]

