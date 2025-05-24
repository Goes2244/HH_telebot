from datetime import datetime, timedelta
from telebot.types import Message
from database.db import add_reminder, get_reminders, delete_reminder
import pytz

def send_reminder(bot, chat_id, candidate, r_type):
    if r_type == "interview":
        text = f"🔔 Сейчас: собеседование с {candidate}!"
    elif r_type == "interview_24h":
        text = f"🔔 Через 24 часа: собеседование с {candidate}!"
    elif r_type == "interview_1h":
        text = f"🔔 Через 1 час: собеседование с {candidate}!"
    elif r_type == "onetoone":
        text = f"🔔 Сейчас: one-to-one встреча с {candidate}!"
    elif r_type == "onetoone_24h":
        text = f"🔔 Через 24 часа: one-to-one встреча с {candidate}!"
    elif r_type == "onetoone_1h":
        text = f"🔔 Через 1 час: one-to-one встреча с {candidate}!"
    else:
        text = f"🔔 Напоминание: {r_type}"
    bot.send_message(chat_id, text)

def register_handlers(bot, scheduler):
    @bot.message_handler(commands=["schedule_interview"])
    def interview_handler(message: Message):
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return bot.reply_to(message, "❗ Формат: /schedule_interview [ФИО] [Дата_время]")
        
        _, name, dt_str = parts
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            dt_utc = dt.astimezone(pytz.UTC)
            
            # Основное событие
            add_reminder(message.chat.id, name, dt_utc.isoformat(), "interview")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_utc,
                args=[bot, message.chat.id, name, "interview"]
            )
            
            # Напоминание за 24 часа
            dt_24h = dt_utc - timedelta(hours=24)
            add_reminder(message.chat.id, name, dt_24h.isoformat(), "interview_24h")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_24h,
                args=[bot, message.chat.id, name, "interview_24h"]
            )
            
            # Напоминание за 1 час
            dt_1h = dt_utc - timedelta(hours=1)
            add_reminder(message.chat.id, name, dt_1h.isoformat(), "interview_1h")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_1h,
                args=[bot, message.chat.id, name, "interview_1h"]
            )
            
            bot.send_message(message.chat.id, f"📆 Собеседование с {name} запланировано на {dt_str} с напоминаниями за 24 ч и 1 ч!")
        
        except ValueError:
            bot.reply_to(message, "❌ Неверный формат даты. Используйте: ГГГГ-ММ-ДД ЧЧ:ММ")

    @bot.message_handler(commands=["schedule_onetoone"])
    def onetoone_handler(message: Message):
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            return bot.reply_to(message, "❗ Формат: /schedule_onetoone [ФИО] [Дата_время]")
        
        _, name, dt_str = parts
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            dt_utc = dt.astimezone(pytz.UTC)
            
            # Основное событие
            add_reminder(message.chat.id, name, dt_utc.isoformat(), "onetoone")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_utc,
                args=[bot, message.chat.id, name, "onetoone"]
            )
            
            # Напоминание за 24 часа
            dt_24h = dt_utc - timedelta(hours=24)
            add_reminder(message.chat.id, name, dt_24h.isoformat(), "onetoone_24h")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_24h,
                args=[bot, message.chat.id, name, "onetoone_24h"]
            )
            
            # Напоминание за 1 час
            dt_1h = dt_utc - timedelta(hours=1)
            add_reminder(message.chat.id, name, dt_1h.isoformat(), "onetoone_1h")
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=dt_1h,
                args=[bot, message.chat.id, name, "onetoone_1h"]
            )
            
            bot.send_message(message.chat.id, f"📆 One-to-one встреча с {name} запланирована на {dt_str} с напоминаниями за 24 ч и 1 ч!")
        
        except ValueError:
            bot.reply_to(message, "❌ Неверный формат даты.")

    # Остальные функции (list_interviews, delete_reminder_handler) остаются без изменений

    @bot.message_handler(commands=["scheduled_interviews"])
    def list_interviews(message: Message):
        reminders = get_reminders()
        text = "📆 Предстоящие события (ID | Кандидат | Дата | Тип):\n"
        for reminder in reminders:
            reminder_id, chat_id, candidate, dt_str, r_type = reminder
            dt = datetime.fromisoformat(dt_str).strftime("%Y-%m-%d %H:%M")
            text += f"ID: {reminder_id} | {candidate} | {dt} ({r_type})\n"
        bot.send_message(message.chat.id, text)

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