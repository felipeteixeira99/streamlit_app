# Imagem base para execucao do projeto
FROM python:3.13.12-slim-trixie

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]