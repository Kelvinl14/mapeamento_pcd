# Usar uma imagem base Python oficial
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY app /app

# Define o caminho para que o Python reconheça a pasta streamlit_app como módulo
ENV PYTHONPATH="${PYTHONPATH}:/app/streamlit_app"

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
