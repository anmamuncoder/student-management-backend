# Use official Python image
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# If Useing mysql 
# RUN apt-get update && apt-get install -y \
#     pkg-config \
#     default-libmysqlclient-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/
 
# Collect static files
# RUN python manage.py collectstatic --noinput

# Default command for web server
# For development: run Django's dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8020"]

# Optional commands (comment/uncomment when needed)
# For ASGI / WebSocket support with Daphne:
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8020", "engine.asgi:application"]

# For Celery worker:
# CMD ["celery", "-A", "engine", "worker", "--loglevel=info"]

# For Celery beat scheduler:
# CMD ["celery", "-A", "engine", "beat", "--loglevel=info"]