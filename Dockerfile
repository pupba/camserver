FROM python:3.11.0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# libGL.so.1 설치
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

COPY . .

CMD ["python", "client.py"]
