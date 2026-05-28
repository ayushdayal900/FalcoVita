FROM python:3.10-slim

WORKDIR /app

# Install dependencies first for caching
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend ./backend

# The app is run as a module so we need /app in PYTHONPATH
ENV PYTHONPATH=/app
ENV FLASK_APP=backend.app
ENV FLASK_ENV=development

EXPOSE 5000

# Default command for the backend API
CMD ["python", "-m", "backend.app"]
