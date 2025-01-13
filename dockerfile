FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DB_PATH=/app/db/lab_exp_results.db \
    PYTHONPATH=/app/src

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/db

COPY . /app

RUN pip install --upgrade pip \
    && pip install openpyxl>=3.1.5 pandas>=2.2.3 pydantic>=2.10.5 pytest>=8.3.4 streamlit>=1.41.1

RUN python scripts/init_db.py

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py"]
