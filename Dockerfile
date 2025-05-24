FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only=main

# Copy project
COPY . .

# Create directories and set permissions
RUN mkdir -p allstatic volumes/static volumes/media

# Set environment variables
ENV PYTHONPATH=/code/sc_backend
ENV DJANGO_SETTINGS_MODULE=djproject.settings.production

# Expose port
EXPOSE 8000

# Default command - updated path
CMD ["sh", "-c", "cd sc_backend && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]