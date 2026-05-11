# Python-ның ресми бейнесін қолданамыз
FROM python:3.10

# Контейнер ішіндегі жұмыс папкасын орнатамыз
WORKDIR /app

# Керекті кітапханаларды көшіріп, орнатамыз
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Проектің барлық кодын контейнерге көшіреміз
COPY . .

# Django-ны іске қосамыз
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]