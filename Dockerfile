FROM python:3.11-slim


RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN mkdir -p /app/cache

RUN chown -R appuser:appgroup /app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY .env ./.env

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "src.bot"]
