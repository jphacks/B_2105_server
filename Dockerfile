FROM python:3.9-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
CMD ["python3", "main.py"]