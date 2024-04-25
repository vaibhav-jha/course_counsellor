FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
ENV LANGCHAIN_TRACING_V2=true
ENV LANGCHAIN_API_KEY=ls__072b32f36eaf4a099cca7e29b8e28035
ENV LANGCHAIN_PROJECT=verizon_counsellor_2024
ENV PROJECT_ID=a92c8753-e724-4835-a415-ec0730333135
ENV WATSONX_APIKEY=b9n-3HqQTRSMvFhUry-awqN3ZLVIr_UzddSht6OQ6CyV
EXPOSE 5000
CMD ["python3", "__main__.py"]
