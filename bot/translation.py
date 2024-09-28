import logging
from .models import ModelManager

class Translator:
    def __init__(self, model_manager: ModelManager, spacy_models):
        self.model_manager = model_manager
        self.spacy_models = spacy_models
    def detect_named_entities(self, text, language_code):
        if language_code in self.spacy_models:
            doc = self.spacy_models[language_code](text)
            entities = {ent.text: ent.label_ for ent in doc.ents}
            return entities
        return {}
    def mask_named_entities(self, text, entities):
        masked_text = text
        for entity, label in entities.items():
            masked_text = masked_text.replace(entity, f"[{label}]")
        return masked_text
    def unmask_named_entities(self, translated_text, entities):
        for entity, label in entities.items():
            translated_text = translated_text.replace(entity, f"[{label}]")
        return translated_text

    def translate_in_chunks(self, text, model, tokenizer, chunk_size=1024):
        tokens = tokenizer(text, return_tensors="pt", truncation=False, padding=True)
        input_ids = tokens["input_ids"]
        num_tokens = input_ids.size(1)


        if num_tokens > chunk_size:
            chunks = [input_ids[:, i:i + chunk_size] for i in range(0, num_tokens, chunk_size)]
            translated_chunks = []

            for chunk in chunks:
                # Generate translation for the chunk
                translated_chunk = model.generate(
                    chunk, max_length=512, num_beams=5, no_repeat_ngram_size=2, early_stopping=True
                )

                decoded_chunk = tokenizer.decode(translated_chunk[0], skip_special_tokens=True)
                translated_chunks.append(decoded_chunk)

            return ' '.join(translated_chunks)
        else:

            translated = model.generate(input_ids, max_length=512, num_beams=5, no_repeat_ngram_size=2,
                                        early_stopping=True)
            return tokenizer.decode(translated[0], skip_special_tokens=True)

    def translate_with_named_entities(self, text, src_lang, tgt_lang):
        """Detect and translate the text with named entity recognition."""

        model, tokenizer = self.model_manager.get_model_and_tokenizer(src_lang, tgt_lang)

        entities = self.detect_named_entities(text, src_lang)

        masked_text = self.mask_named_entities(text, entities)

        translated_text = self.translate_in_chunks(masked_text, model, tokenizer)

        final_translation = self.unmask_named_entities(translated_text, entities)

        return final_translation
    def translate(self, text, src_lang, tgt_lang):
        logging.debug(f"Starting translation from {src_lang} to {tgt_lang} for text: {text}")
        model, tokenizer = self.model_manager.get_model_and_tokenizer(src_lang, tgt_lang)
        logging.debug(f"MODEL AND TOKENIZER FOR {src_lang}-{tgt_lang} LOADED SUCCESSFULLY")
        translated_text = self.translate_in_chunks(text, model, tokenizer)
        logging.debug(f"TRANSLATION COMPLETED: {translated_text}")
        return self.translate_in_chunks(text, model, tokenizer)