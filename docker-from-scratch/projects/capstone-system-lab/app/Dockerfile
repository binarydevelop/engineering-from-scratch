FROM python:3.11-slim

# Security best practice: non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -d /app appuser

WORKDIR /app
COPY app.py /app/app.py

RUN chown -R appuser:appgroup /app
USER appuser:appgroup

EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=3s --start-period=3s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" || exit 1

ENTRYPOINT ["python", "-u", "/app/app.py"]
