FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    jq \
    && rm -rf /var/lib/apt/lists/*

COPY www/server.py /app/server.py
COPY www/ /app/www/
COPY run.sh /run.sh

RUN sed -i 's/\r$//' /run.sh && chmod a+x /run.sh

EXPOSE 8099

CMD ["/run.sh"]