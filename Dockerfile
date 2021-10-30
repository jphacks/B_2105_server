FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app

ENV PORT 8080
ENV HOST 0.0.0.0
ENV PYTHONPATH=/app
RUN apt update -y && apt upgrade -y
RUN apt-get install -y libgl1-mesa-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]