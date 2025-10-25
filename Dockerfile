# === 1. Використовуємо офіційний Python-образ ===
FROM python:3.11-slim

# === 2. Встановлюємо робочу директорію всередині контейнера ===
WORKDIR /app

# === 3. Копіюємо файли залежностей ===
COPY requirements.txt .

# === 4. Встановлюємо залежності ===
RUN pip install --no-cache-dir -r requirements.txt

# === 5. Копіюємо увесь код проєкту ===
COPY . .

# === 6. Відкриваємо порт (FastAPI стандартно слухає 8000) ===
EXPOSE 8000

# === 7. Запускаємо додаток через uvicorn ===
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
