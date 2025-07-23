FROM jrottenberg/ffmpeg:4.4-ubuntu

# Instalar Python e pip
RUN apt update && \
    apt install -y python3 python3-pip && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "server.py"]
