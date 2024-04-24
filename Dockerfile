FROM python:3.11-alpine3.18
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=__main__.py
CMD ["flask", "run", "--host", "0.0.0.0"]
