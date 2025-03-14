FROM python:3.9

# Instala o FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Cria a pasta para uploads
RUN mkdir -p uploads

# Expõe a porta 5000
EXPOSE 5000

# Inicia o servidor
CMD ["python", "app.py"]

