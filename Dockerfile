FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/
RUN chmod +x src/healthcheck.py
RUN useradd --create-home --shell /bin/bash bot_user && \
    chown -R bot_user:bot_user /app
USER bot_user
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["python", "src/bot.py"]