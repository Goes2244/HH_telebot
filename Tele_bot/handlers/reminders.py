from telebot.types import Message
from database.db import add_reminder, get_reminders

def register_handlers(bot):
    @bot.message_handler(commands=["schedule_interview"])
    def interview_handler(message: Message):
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return bot.reply_to(message, "❗ Формат: /schedule_interview [ФИО] [Дата время]")
        _, name, dt = parts
        add_reminder(name, dt, "interview")
        bot.send_message(message.chat.id, f"📆 Собеседование назначено:\n📌 Кандидат: {name}\n📅 Дата: {dt}")

    @bot.message_handler(commands=["schedule_onetoone"])
    def onetoone_handler(message: Message):
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return bot.reply_to(message, "❗ Формат: /schedule_onetoone [ФИО] [Дата время]")
        _, name, dt = parts
        add_reminder(name, dt, "onetoone")
        bot.send_message(message.chat.id, f"📆 One-to-one встреча назначена:\n📌 Сотрудник: {name}\n📅 Дата: {dt}")

    @bot.message_handler(commands=["scheduled_interviews"])
    def list_interviews(message: Message):
        reminders = get_reminders()
        text = "📆 Предстоящие собеседования и встречи:\n"
        for candidate, dt, r_type in reminders:
            text += f"- {candidate} | {dt} ({r_type})\n"
        bot.send_message(message.chat.id, text)
