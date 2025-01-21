# Use Python slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /wallet_app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    python3-dev \
    python3-venv \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /wallet_app/venv

# Activate virtual environment and update PATH
ENV VIRTUAL_ENV=/wallet_app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better cache usage
COPY requirements.txt requirements.txt

# Install dependencies in virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Set environment variables
ENV FLASK_APP=app.run
ENV FLASK_ENV=development
ENV PYTHONPATH=/wallet_app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]