from telebot.types import Message
from database.db import get_notes, delete_note

def register_handlers(bot):
    @bot.message_handler(commands=["delete_note"])
    def delete_note_handler(message: Message):
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return bot.reply_to(message, "❗ Формат: /delete_note [кандидат] [номер заметки]")
        
        _, candidate, note_num = parts
        try:
            note_num = int(note_num)
            notes = get_notes(candidate) 
            
            if not notes:
                return bot.reply_to(message, f"❌ Нет заметок по кандидату {candidate}")
            
            if 1 <= note_num <= len(notes):
                note_id = notes[note_num-1][0]  
                delete_note(note_id)
                bot.reply_to(message, f"✅ Заметка #{note_num} удалена")
            else:
                bot.reply_to(message, f"❌ Номер должен быть от 1 до {len(notes)}")
        except ValueError:
            bot.reply_to(message, "❌ Номер заметки должен быть числом")