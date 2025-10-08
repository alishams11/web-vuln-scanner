# DVWA (Damn Vulnerable Web App) — Quickstart with Docker Compose

This folder contains instructions to spin up DVWA locally for testing.

## Requirements
- Docker & Docker Compose

## Run DVWA
Create a `docker-compose.yml` with the following content (or copy-paste):

```yaml
version: '3.7'
services:
  dvwa:
    image: vulnerables/web-dvwa:latest
    ports:
      - "8081:80"
    environment:
      - MYSQL_DATABASE=dvwa
      - MYSQL_USER=dvwa
      - MYSQL_PASSWORD=dvwa
      - MYSQL_ROOT_PASSWORD=root
    restart: unless-stopped

  mysql:
    image: mysql:5.7
    environment:
      - MYSQL_DATABASE=dvwa
      - MYSQL_USER=dvwa
      - MYSQL_PASSWORD=dvwa
      - MYSQL_ROOT_PASSWORD=root
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
# then open http://localhost:8081
```

## Notes
- DVWA default credentials: admin/password (may require setup in the web UI).
- For security, run this only in an isolated environment (local VM).
