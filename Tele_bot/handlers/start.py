from telebot.types import Message

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message: Message):
        bot.send_message(message.chat.id, "👋 Добро пожаловать! Вот доступные команды:\n\n"
                         "/auth (Авторизация)\n"
                         "/search_candidate\n"
                         "/import_resume\n"
                         "/files\n"
                         "/get_file\n"
                         "/add_note\n"
                         "/notes\n"
                         "/schedule_interview\n"
                         "/schedule_onetoone\n"
                         "/scheduled_interviews\n")
