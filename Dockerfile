# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do backend
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Cria pastas necessárias
RUN mkdir -p image sheets

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

