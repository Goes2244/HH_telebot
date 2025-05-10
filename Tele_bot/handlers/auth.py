from telebot.types import Message
from config import HH_CLIENT_ID, REDIRECT_URI

def register_handlers(bot):
    @bot.message_handler(commands=["auth"])
    def auth_handler(message: Message):
        url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={HH_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        bot.send_message(message.chat.id, f"🔐 Авторизуйтесь через HH:\n{url}")
