#!/usr/bin/env bash
cd /app/www || exit 1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Build Ledger server..."

python3 -u /app/server.py 2>&1 | while IFS= read -r line; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line"
done