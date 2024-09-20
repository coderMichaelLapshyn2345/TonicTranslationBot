import torch
from transformers import MarianMTModel, MarianTokenizer

class ModelManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
    def load_model(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models:
            model = MarianMTModel.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.models[model_key] = model
            self.tokenizers[model_key] = MarianTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
        return self.models[model_key], self.tokenizers[model_key]
