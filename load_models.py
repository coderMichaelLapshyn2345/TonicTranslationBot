from transformers import MarianMTModel, MarianTokenizer


def download_models():
    languages = [
        ("uk", "en"), ("ru", "en"), ("en", "de"),
        ("es", "en"), ("fr", "en"), ("uk", "de"),
        ("de", "en"), ("de", "es"), ("de", "fr"),
        ("fr", "de"), ("es", "de"), ("es", "fr"),
        ("fr", "es"), ("es", "ru"), ("ru", "es"),
        ("uk", "fr"), ("fr", "uk"), ("ru", "fr"),
        ("fr", "ru"), ("uk", "es"), ("es", "uk"),
        ("en", "uk"), ("en", "es"), ("en", "fr"),
        ("uk", "ru"), ("ru", "uk"), ("en", "ru"),
        ("de", "uk")
    ]

    for src, tgt in languages:
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        print(f"Downloading {model_name}")
        MarianMTModel.from_pretrained(model_name)
        MarianTokenizer.from_pretrained(model_name)
        print(f"Model {model_name} downloaded successfully")
if __name__ == "__main__":
    download_models()