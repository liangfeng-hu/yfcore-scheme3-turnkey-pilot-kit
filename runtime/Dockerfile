FROM python:3.11-slim

WORKDIR /app
COPY . /app

EXPOSE 8787 9001 8080

# Default runs sidecar; docker-compose overrides for gateway/upstream.
CMD ["python", "reference-impl/python/sidecar_service.py"]
