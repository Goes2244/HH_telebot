from telebot.types import Message
from hh_api.client import search_candidates, parse_resume_link

def register_handlers(bot):
    @bot.message_handler(commands=["search_candidate"])
    def search_candidate_handler(message: Message):
        query = message.text.replace("/search_candidate", "").strip()
        if not query:
            return bot.reply_to(message, "❗ Укажите запрос для поиска.")
        data = search_candidates(query)
        text = "🔍 Найдено несколько кандидатов:\n"
        for item in data.get("items", []):
            text += f"⃣{item.get('first_name', '')} {item.get('last_name', '')} | {item.get('title', '')}\n📜 [Резюме]({item.get('alternate_url')})\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    @bot.message_handler(commands=["import_resume"])
    def import_resume_handler(message: Message):
        link = message.text.replace("/import_resume", "").strip()
        resume_id = parse_resume_link(link)
        bot.send_message(message.chat.id, f"📜 Резюме {resume_id} добавлено в избранное.")
