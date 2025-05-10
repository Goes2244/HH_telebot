import os
from telebot.types import Message

FILES_DIR = "data/resumes"

def register_handlers(bot):
    @bot.message_handler(commands=["files"])
    def list_files(message: Message):
        files = os.listdir(FILES_DIR)
        if not files:
            bot.send_message(message.chat.id, "❌ Нет доступных файлов.")
        else:
            msg = "📂 Доступные файлы:\n" + "\n".join(f"⃣{f}" for f in files)
            bot.send_message(message.chat.id, msg)

    @bot.message_handler(commands=["get_file"])
    def get_file(message: Message):
        filename = message.text.replace("/get_file", "").strip()
        filepath = os.path.join(FILES_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, "❌ Файл не найден.")
