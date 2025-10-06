# Stage 1 - Build Go binary
FROM golang:1.20 as builder
WORKDIR /app
COPY core-go/ .
RUN go mod tidy && go build -o wvs-core main.go

# Stage 2 - Final image with Python + Go binary
FROM python:3.11-slim
WORKDIR /app

# Install Python deps
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Go binary
COPY --from=builder /app/wvs-core /usr/local/bin/wvs-core

# Copy Python package and templates
COPY pywvs/ pywvs/
COPY templates/ templates/

ENTRYPOINT ["python", "-m", "pywvs"]

