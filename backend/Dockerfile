FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN useradd -m myuser
USER myuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]