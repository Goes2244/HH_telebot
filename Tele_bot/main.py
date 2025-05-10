from loader import bot
from handlers import start, auth, candidates, notes, reminders, files

start.register_handlers(bot)
auth.register_handlers(bot)
candidates.register_handlers(bot)
notes.register_handlers(bot)
reminders.register_handlers(bot)
files.register_handlers(bot)

if __name__ == "__main__":
    bot.polling(none_stop=True)
