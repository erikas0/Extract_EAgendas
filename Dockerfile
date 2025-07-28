# Dockerfile
FROM python:3.9-slim
# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "get_compromissos.py"]