# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt requirements.txt

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Download spaCy language models after installing spaCy
RUN python -m spacy download en_core_web_sm \
    && python -m spacy download de_core_news_sm \
    && python -m spacy download fr_core_news_sm \
    && python -m spacy download uk_core_news_sm \
    && python -m spacy download ru_core_news_sm \
    && python -m spacy download pl_core_news_sm \
    && python -m spacy download es_core_news_sm

# Copy the rest of the app code
COPY . .

EXPOSE 8080


# Set the entry point for your application
CMD ["python3", "main.py"]
