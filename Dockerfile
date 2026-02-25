# Используем официальный образ Python
FROM python:3.14.2-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt сначала (для кэширования слоя)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта (включая вашу БД и конфиг)
COPY . .

# Команда для запуска бота
CMD ["python", "main.py"]
