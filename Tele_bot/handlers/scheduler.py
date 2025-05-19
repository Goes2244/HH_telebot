from apscheduler.schedulers.background import BackgroundScheduler
from database.db import get_reminders
from datetime import datetime
import pytz
from dateutil import parser

def init_scheduler(bot):
    scheduler = BackgroundScheduler(timezone=pytz.UTC)
    scheduler.start()
    
    reminders_data = get_reminders()
    for reminder in reminders_data:
        reminder_id, chat_id, candidate, dt_str, r_type = reminder
        
        try:
            dt = parser.isoparse(dt_str)
            scheduler.add_job(
                send_reminder_wrapper,
                'date',
                run_date=dt,
                args=[bot, chat_id, candidate, r_type]
            )
        except Exception as e:
            print(f"Ошибка восстановления напоминания: {e}")
    
    return scheduler

def send_reminder_wrapper(bot, chat_id, candidate, r_type):
    from handlers.reminders import send_reminder
    send_reminder(bot, chat_id, candidate, r_type)
