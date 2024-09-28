import torch
from transformers import MarianMTModel, MarianTokenizer

class ModelManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
    def load_all_models_and_tokenizers(self):
        language_pairs = [
            ('en', 'de'), ('de', 'en'), ('en', 'fr'), ('fr', 'en'),
            ('en', 'es'), ('es', 'en'), ('en', 'uk'), ('uk', 'en'),
            ('en', 'ru'), ('ru', 'en'), ('de', 'uk'), ('uk', 'de'),
            ('de', 'ru'), ('ru', 'de'), ('de', 'fr'), ('fr', 'de'),
            ('de', 'es'), ('es', 'de'), ('uk', 'fr'), ('fr', 'uk'),
            ('es', 'uk'), ('uk', 'es'), ('es', 'fr'), ('fr', 'es'),
            ('es', 'ru'), ('ru', 'es'), ('fr', 'ru'), ('ru', 'fr'),
            ('uk', 'ru'), ('ru', 'uk')
        ]
        for src_lang, tgt_lang in language_pairs:
            self.load_model_and_tokenizer(src_lang, tgt_lang)
    def load_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models:
            model = MarianMTModel.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.models[model_key] = model
            tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.tokenizers[model_key] = tokenizer
    def get_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models or model_key not in self.tokenizers:
            self.load_model_and_tokenizer(src_lang, tgt_lang)
        return self.models[model_key], self.tokenizers[model_key]
