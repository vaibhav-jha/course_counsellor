FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "__main__.py"]
