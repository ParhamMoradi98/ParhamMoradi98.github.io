# Use a small official Python base image
FROM python:3.10-slim

# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout/err to be unbuffered so logs show immediately
ENV PYTHONUNBUFFERED=1

# (Optional) if you need system-level packages, install them here. 
# Example: RUN apt-get update && apt-get install -y libgomp && rm -rf /var/lib/apt/lists/*

# Create a directory for your app’s source code
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt /app/

# Install Python deps (includes CPU-only PyTorch).
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your files (app.py, etc.)
COPY . /app

# Expose port 5000 to the Heroku environment
EXPOSE 5000

# Gunicorn is a production-ready WSGI server for Python web apps
RUN pip install --no-cache-dir gunicorn

# Start Gunicorn, telling it to run "app:app" 
#    - that means: from app.py, import the variable "app"
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
