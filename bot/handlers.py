import os
from .file_processing import FileProcessor
from .translation import Translator
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from langdetect import detect
import logging
class BotHandlers:
    def __init__(self, bot, translator: Translator):
        self.bot = bot
        self.translator = translator
        self.user_language = {}
    def send_welcome(self, message):
        welcome_text = "Welcome to TonicTranslation AI! 🌟🌍\n\nPlease choose a language for translation:"
        self.bot.send_message(message.chat.id, welcome_text, reply_markup=self.language_selection_keyboard())
    def send_help(self, message):
        help_text = """
                🌟 *TonicTranslation AI - Help* 🌟

                Available Commands:
                - `/start`: Start the bot and choose a language.
                - `/help`: Display this help message.
                - `/info`: Get information about the bot and supported languages.
                - `/news`: Get the latest updates and features.
                - `/feedback`: Provide feedback about the bot (Coming soon).

                To translate, just type your message or upload a file. The bot will detect the input language and translate it into your chosen target language.
                """
        self.bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    def send_info(self, message):
        info_text = """
                TonicTranslation AI 🌐

                This bot is powered by AI models from MarianMT and supports translations between:
                - English 🇬🇧
                - German 🇩🇪
                - French 🇫🇷
                - Ukrainian 🇺🇦
                - Russian 🇷🇺
                - Spanish 🇪🇸

                Future features include:
                - More languages (Polish, Italian, Portuguese, etc.)
                - Voice-to-text for translating voice messages.
                - API support for businesses.
                """
        self.bot.send_message(message.chat.id, info_text)
    def send_news(self, message):
        news_text = """
                🌍 *Latest News* 🌍

                - Improved translation for formal documents.
                - Speech-to-Text translation coming soon.
                - New language support: Polish and Italian.
                """
        self.bot.send_message(message.chat.id, news_text, parse_mode='Markdown')
    def send_feedback(self, message):
        feedback_text = "We'd love to hear your feedback! Please send us your thoughts and suggestions."
        self.bot.send_message(message.chat.id, feedback_text)
    def handle_feedback(self, message):
        feedback = message.text
        # Coming soon
        self.bot.send_message(message.chat.id, "Thank you for your feedback! We appreciate it.")
    def language_selection_keyboard(self):
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(KeyboardButton('English'), KeyboardButton('German'), KeyboardButton('French'), KeyboardButton('Spanish'), KeyboardButton('Ukrainian'), KeyboardButton('Russian'))
        return markup
    def handle_language_selection(self, message):
        language_map = {'English': 'en',
                        'German': 'de',
                        'French': 'fr',
                        'Spanish': 'es',
                        'Ukrainian': 'uk',
                        'Russian': 'ru'}
        selected_language = language_map[message.text]
        self.user_language[message.chat.id] = selected_language
        self.bot.send_message(message.chat.id, f"{selected_language} is selected. Please write your text or attach a file of one of the formats: TXT, DOCX or PDF")
    def handle_file(self, message):
        file_info = self.bot.get_file(message.document.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        file_extension = os.path.splitext(file_name)[-1].lower()
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        if file_extension == ".txt":
            text = FileProcessor.process_txt(file_path)
        elif file_extension == ".docx":
            text = FileProcessor.process_docx(file_path)
        elif file_extension == ".pdf":
            text = FileProcessor.process_pdf(file_path)
        else:
            self.bot.send_message(message.chat.id, "Unsupported file format")
            return
        input_language = detect(text)
        target_language = self.user_language.get(message.chat.id, 'en')
        translated_text = self.translator.translate(text, input_language, target_language)
        self.bot.send_message(message.chat.id, translated_text)

    def handle_message(self, message):
        chat_id = message.chat.id
        text = message.text
        logging.debug(f"Handling from chat_id: {chat_id}, text: {text}")
        if chat_id not in self.user_language:
            self.user_language[chat_id] = 'en'
            logging.debug(f"Default language is set to 'en' for chat_id: {chat_id}")
        try:
            input_language = detect(text)
            logging.debug(f"Detected language for chat_id {chat_id}: {input_language}")
        except Exception as e:
            logging.error(f"Error detecting language for chat_id {chat_id}: {e}")
            self.bot.send_message(chat_id, "Sorry, I couldn't detect the language")
            return
        target_language = self.user_language[chat_id]
        logging.debug(f"Target language for chat_id: {chat_id}: {target_language}")
        try:
            translated_text = self.translator.translate(text, input_language, target_language)
            logging.debug(f"Translated text for chat_id {chat_id}: {translated_text}")
        except Exception as e:
            logging.error(f"Error translating text for chat_id: {chat_id}: {e}")
            self.bot.send_message(chat_id, "Sorry, an error occurred while translating the text")
            return
        self.bot.send_message(chat_id, translated_text)
        logging.debug(f"Sent translated message to chat_id: {chat_id}")