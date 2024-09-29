from transformers import MarianMTModel, MarianTokenizer


def download_models():
    languages = [
        ("uk", "en"), ("ru", "en"), ("en", "de"),
        ("es", "en"), ("fr", "en")
    ]

    for src, tgt in languages:
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        print(f"Downloading {model_name}")
        MarianMTModel.from_pretrained(model_name)
        MarianTokenizer.from_pretrained(model_name)
        print(f"Model {model_name} downloaded successfully")
if __name__ == "__main__":
    download_models()