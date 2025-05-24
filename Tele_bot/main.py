from loader import bot
from loader import bot
from handlers import start, auth, candidates, notes, reminders, files, scheduler, delete_note 

scheduler = scheduler.init_scheduler(bot)

start.register_handlers(bot)
auth.register_handlers(bot)
candidates.register_handlers(bot)
notes.register_handlers(bot)
reminders.register_handlers(bot, scheduler)  
files.register_handlers(bot)
delete_note.register_handlers(bot)

if __name__ == "__main__":
    bot.polling(none_stop=True)
