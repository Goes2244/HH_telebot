from telebot.types import Message
from database.db import add_note, get_notes

def register_handlers(bot):
    @bot.message_handler(commands=["add_note"])
    def add_note_handler(message: Message):
        parts = message.text.replace("/add_note", "").strip().split(" ", 1)
        if len(parts) < 2:
            return bot.reply_to(message, "❗ Укажите имя и заметку.")
        candidate, note = parts
        add_note(candidate, note)
        bot.send_message(message.chat.id, "✅ Заметка сохранена.")

    @bot.message_handler(commands=["notes"])
    def get_notes_handler(message: Message):
        candidate = message.text.replace("/notes", "").strip()
        notes = get_notes(candidate)
        if notes:
            text = f"📌 Заметки по {candidate}:\n" + "\n".join(f"- {n}" for n in notes)
        else:
            text = f"❌ Нет заметок по {candidate}."
        bot.send_message(message.chat.id, text)
