FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  
COPY . .
ENV LANGCHAIN_TRACING_V2=true
ENV LANGCHAIN_PROJECT=verizon_counsellor_2024
EXPOSE 5000
CMD ["python3", "__main__.py"]
