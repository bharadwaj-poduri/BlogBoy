FROM python:3.7-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    python3-dev \
    gcc \
    supervisor \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Set up supervisor config
COPY ./Config/blogboy_supervisor.conf /etc/supervisor/conf.d/

# Set up working directory
WORKDIR /BlogBoy

# Install Python requirements
COPY ./requirements.txt /BlogBoy/requirements.txt
RUN pip install --upgrade "pip<21.0" "setuptools<46.0.0" "wheel"
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /BlogBoy

# Ensure logs directory exists
RUN mkdir -p /var/log/blogboy && chmod 777 /var/log/blogboy

# Start supervisor
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
