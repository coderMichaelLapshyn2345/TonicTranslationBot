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


RUN python -c "from transformers import MarianMTModel, MarianTokenizer; \
    languages = [('uk', 'en'), ('ru', 'en'), ('en', 'de'), ('es', 'en'), ('fr', 'en')]; \
    for pair in languages: \
        src, tgt = pair[0], pair[1]; \
        model_name = 'Helsinki-NLP/opus-mt-' + src + '-' + tgt; \
        MarianMTModel.from_pretrained(model_name); \
        MarianTokenizer.from_pretrained(model_name); \
        print('Model ' + model_name + ' downloaded')"


RUN pip install waitress
# Copy the rest of the app code
COPY . .

ENV PORT 8080
EXPOSE 8080

# Set the entry point for your application
CMD ["waitress-serve", "--port=8080", "main:app"]
