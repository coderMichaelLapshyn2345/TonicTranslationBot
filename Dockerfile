# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm \
    && python -m spacy download de_core_news_sm \
    && python -m spacy download fr_core_news_sm \
    && python -m spacy download uk_core_news_sm \
    && python -m spacy download ru_core_news_sm \
    && python -m spacy download pl_core_news_sm \
    && python -m spacy download es_core_news_sm

COPY . .

RUN python load_models.py


RUN pip install waitress



ENV PORT 8080
EXPOSE 8080

# Set the entry point for your application
CMD ["waitress-serve", "--port=8080", "main:app"]
