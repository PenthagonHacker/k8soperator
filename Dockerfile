FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Emulate_k8s_logs.py .

CMD ["python", "Emulate_k8s_logs.py"]
