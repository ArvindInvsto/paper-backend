FROM python:3.11

WORKDIR /sharksigma-backend-main

COPY requirements.txt .

RUN apt-get update && apt-get install -y git && pip install --no-cache-dir -r requirements.txt

COPY . .
  
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]