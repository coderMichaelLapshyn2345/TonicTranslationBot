from transformers import MarianMTModel, MarianTokenizer
import logging
import os
class ModelManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.cache_dir = "/root/.cache/huggingface/transformers"

    def load_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        model_path = os.path.join(self.cache_dir, f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
        if not os.path.exists(model_path):
            logging.debug(f"LOADING MODEL FOR {src_lang}-{tgt_lang}")
            model = MarianMTModel.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            tokenizer = MarianTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}")
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
        else:
            logging.debug(f"MODEL FOR {src_lang}-{tgt_lang} IS ALREADY AVAILABLE LOCALLY")
            self.models[model_key] = MarianMTModel.from_pretrained(model_path)
            self.tokenizers[model_key] = MarianTokenizer.from_pretrained(model_path)
    def get_model_and_tokenizer(self, src_lang, tgt_lang):
        model_key = f"{src_lang}-{tgt_lang}"
        if model_key not in self.models or model_key not in self.tokenizers:
            self.load_model_and_tokenizer(src_lang, tgt_lang)
        return self.models[model_key], self.tokenizers[model_key]
