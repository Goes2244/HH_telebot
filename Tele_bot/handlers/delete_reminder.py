from telebot.types import Message
from database.db import get_reminders, delete_reminder

def register_handlers(bot):
    @bot.message_handler(commands=["delete_reminder"])
    def delete_reminder_handler(message: Message):
        try:
            reminder_id = int(message.text.split()[1])
        except (IndexError, ValueError):
            return bot.reply_to(message, "❗ Формат: /delete_reminder [ID_напоминания]")

        reminders = get_reminders()
        if not any(reminder[0] == reminder_id for reminder in reminders):
            return bot.reply_to(message, "❌ Напоминание с таким ID не найдено.")

        delete_reminder(reminder_id)
        bot.reply_to(message, "✅ Напоминание удалено.")