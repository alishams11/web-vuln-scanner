# ------------------------
# Stage 1: build Go core
# ------------------------
FROM golang:1.22 AS builder

WORKDIR /usr/src/wvs-core

# Copy go.mod / go.sum first for caching
COPY core-go/go.mod core-go/go.sum ./
RUN go mod download

# Copy source and build
COPY core-go/ ./

# Build single static binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -o /usr/local/bin/wvs-core main.go


# ------------------------
# Stage 2: runtime image
# ------------------------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/wvs

# Create non-root user
RUN groupadd -r wvs && useradd -r -g wvs -m -d /home/wvs wvs

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python package (includes templates)
COPY pywvs/ pywvs/

# Copy Go core binary
COPY --from=builder /usr/local/bin/wvs-core /usr/local/bin/wvs-core
RUN chmod +x /usr/local/bin/wvs-core

# Drop privileges
USER wvs

ENV PYTHONPATH=/opt/wvs
WORKDIR /opt/wvs


# Default entry
ENTRYPOINT ["python", "-m", "pywvs"]
CMD ["--help"]

