FROM python:3.9-slim

WORKDIR /app
RUN mkdir backend

COPY requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY . ./backend/

EXPOSE 5000

ENV PYTHONPATH=/app
CMD ["python", "-m", "backend.app"]
