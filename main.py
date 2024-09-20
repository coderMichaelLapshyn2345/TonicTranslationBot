import telebot
import spacy
import logging
from bot.models import ModelManager
from bot.translation import Translator
from bot.handlers import BotHandlers
from dotenv import load_dotenv
import os


spacy_models = {
    'en': spacy.load('en_core_web_sm'),
    'de': spacy.load('de_core_news_sm'),
    'fr': spacy.load('fr_core_news_sm'),
    'uk': spacy.load('uk_core_news_sm'),
    'ru': spacy.load('ru_core_news_sm'),
    'pl': spacy.load('pl_core_news_sm')
}
logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
if API_TOKEN:
    logging.info(f"API Token loaded: {API_TOKEN}")
else:
    logging.error("API Token not found")
mybot = telebot.TeleBot(API_TOKEN)


model_manager = ModelManager()
translator = Translator(model_manager=model_manager, spacy_models=spacy_models)


bot_handlers = BotHandlers(bot=mybot, translator=translator)


@mybot.message_handler(commands=['start'])
def welcome_handler(message):
    bot_handlers.send_welcome(message)

@mybot.message_handler(commands=['help'])
def help_handler(message):
    bot_handlers.send_help(message)

@mybot.message_handler(commands=['info'])
def info_handler(message):
    bot_handlers.send_info(message)

@mybot.message_handler(commands=['news'])
def news_handler(message):
    bot_handlers.send_news(message)

@mybot.message_handler(commands=['feedback'])
def feedback_handler(message):
    bot_handlers.send_feedback(message)

@mybot.message_handler(func=lambda message: message.text in ['English', 'German', 'French', 'Spanish', 'Ukrainian', 'Russian'])
def language_selection_handler(message):
    bot_handlers.handle_language_selection(message)

@mybot.message_handler(content_types=['document'])
def file_handler(message):
    bot_handlers.handle_file(message)
@mybot.message_handler(func=lambda message: True)
def handle_message(message):
    bot_handlers.handle_message(message)

mybot.infinity_polling()
