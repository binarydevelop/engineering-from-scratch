FROM python:3.11-slim
WORKDIR /app
COPY app.py .

# EXPOSE is metadata documentation ONLY.
# It does NOT publish the port or configure host routing!
EXPOSE 8000

CMD ["python3", "app.py"]
