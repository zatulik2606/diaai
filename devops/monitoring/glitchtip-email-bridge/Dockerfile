FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV HOST=0.0.0.0 \
    PORT=8081

EXPOSE 8081

HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8081/health')" || exit 1

CMD ["python", "app.py"]
