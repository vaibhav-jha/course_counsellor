FROM ubuntu

RUN \
    apt update && \
    apt upgrade -y && \
    apt install -y python && \
    apt clean && \
    rm -rf /var/lib/apt/lists/\* && \


COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install requirements.txt

ENTRYPOINT ["python3", "__main__.py"]