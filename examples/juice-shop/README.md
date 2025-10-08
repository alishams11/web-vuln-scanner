# OWASP Juice Shop — Quickstart with Docker

## Requirements
- Docker

## Run Juice Shop
Simple run:
```bash
docker run --rm -p 3000:3000 bkimminich/juice-shop
# then open http://localhost:3000
```

Or with docker-compose (create docker-compose.yml):
```yaml
version: '3'
services:
  juice-shop:
    image: bkimminich/juice-shop
    ports:
      - "3000:3000"
    restart: unless-stopped
```

## Notes
- Juice Shop is written in Node and includes many intentionally vulnerable flows.
- Use for local practice only.
