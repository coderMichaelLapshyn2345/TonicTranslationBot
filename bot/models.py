import torch
from transformers import MarianMTModel, MarianTokenizer
import logging
class ModelManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}

    def load_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models:
            logging.debug(f"LOADING MODEL FOR {src_lang}-{tgt_lang}")
            model = MarianMTModel.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.models[model_key] = model
            tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.tokenizers[model_key] = tokenizer
        else:
            logging.debug(f"MODEL {src_lang}-{tgt_lang} IS ALREADY LOADED")
    def get_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models or model_key not in self.tokenizers:
            self.load_model_and_tokenizer(src_lang, tgt_lang)
        return self.models[model_key], self.tokenizers[model_key]
