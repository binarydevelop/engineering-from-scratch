FROM python:3.11-slim

# Set working directory inside container rootfs
WORKDIR /app

# Copy application source code from host build context into image layer
COPY app.py .

# Define default runtime environment variable
ENV SERVICE_NAME="dfs-microservice"

# Document intended network port (metadata only)
EXPOSE 8000

# Exec form of CMD: specifies executable and default arguments
CMD ["python3", "app.py"]
