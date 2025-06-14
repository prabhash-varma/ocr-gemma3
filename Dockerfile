FROM python:3.11-alpine
RUN apk add --no-cache build-base
COPY . /ocr-gemma3
WORKDIR /ocr-gemma3
RUN pip install -r requirements.txt
ENV GOOGLE_API_KEY=""
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py"]