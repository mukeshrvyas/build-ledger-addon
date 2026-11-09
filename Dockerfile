FROM python:3.11-slim

WORKDIR /local_apps/build-ledger

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY www/ /local_apps/build-ledger/

EXPOSE 8099

CMD ["python3", "server.py"]