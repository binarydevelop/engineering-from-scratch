FROM python:3.11-slim
WORKDIR /app
COPY app_with_health.py .
EXPOSE 8080

# Configure periodic container health probe
HEALTHCHECK --interval=2s --timeout=1s --start-period=1s --retries=2 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')" || exit 1

CMD ["python3", "app_with_health.py"]
