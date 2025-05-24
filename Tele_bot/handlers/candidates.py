from telebot.types import Message
from database.db import cursor, conn
from handlers.hh_parser import parse_hh_resume

def register_handlers(bot):
    @bot.message_handler(commands=["add_manual"])
    def add_manual_resume(message: Message):
        try:
            args = message.text.replace("/add_manual", "").strip().split(";")
            if len(args) != 5:
                raise ValueError("❌ Неверное количество параметров")

            full_name = args[0].strip()
            position = args[1].strip()
            city = args[2].strip()
            experience = args[3].strip()
            raw_link = args[4].strip()
            
            clean_link = raw_link.split("?")[0].split("#")[0]

            # if "hh.ru/resume/" not in clean_link:
            #     raise ValueError("❌ Ссылка должна содержать `hh.ru/resume/`")

            cursor.execute(
                "SELECT id FROM manual_resumes WHERE resume_link = ?", 
                (clean_link,)
            )
            if cursor.fetchone():
                return bot.reply_to(message, "⚠️ Это резюме уже есть в базе!")

            cursor.execute(
                "INSERT INTO manual_resumes (full_name, position, city, experience, resume_link, added_by) VALUES (?, ?, ?, ?, ?, ?)",
                (full_name, position, city, experience, clean_link, message.chat.id)
            )
            conn.commit()
            
            bot.reply_to(message, "✅ Резюме успешно добавлено!")

        except ValueError as ve:
            bot.reply_to(message, str(ve))
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.reply_to(message, "❌ Произошла внутренняя ошибка")


    @bot.message_handler(commands=["search_manual"])
    def search_manual_resumes(message: Message):
        query = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""
        
        cursor.execute(
            "SELECT * FROM manual_resumes WHERE full_name LIKE ? OR position LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        resumes = cursor.fetchall()
        
        if not resumes:
            return bot.reply_to(message, "❌ Ничего не найдено.")
        
        text = "🔍 Результаты поиска:\n\n"
        for resume in resumes:
            text += f"• {resume[1]} ({resume[2]}, {resume[3]})\nСсылка: {resume[5]}\n\n"
        
        bot.send_message(message.chat.id, text, disable_web_page_preview=True)

    @bot.message_handler(commands=["import_resume"])
    def import_resume_handler(message: Message):
        link = message.text.replace("/import_resume", "").strip()
        
        if "hh.ru/resume/" not in link:
            return bot.reply_to(message, "❌ Укажите корректную ссылку на резюме с HH.ru")
        
        data = parse_hh_resume(link)
        if not data:
            return bot.reply_to(message, "❌ Не удалось распарсить резюме")
        
        cursor.execute(
            "INSERT INTO manual_resumes (full_name, position, city, experience, resume_link, added_by) VALUES (?, ?, ?, ?, ?, ?)",
            (data["full_name"], data["position"], data["city"], data["experience"], link, message.chat.id)
        )
        conn.commit()
        
        bot.reply_to(message, f"✅ Резюме {data['full_name']} добавлено!")

    @bot.message_handler(commands=["search_candidate"])
    def search_candidate_handler(message: Message):
        query = message.text.replace("/search_candidate", "").strip()
        
        cursor.execute(
            "SELECT * FROM manual_resumes WHERE full_name LIKE ? OR position LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        resumes = cursor.fetchall()
        
        if resumes:
            text = "🔍 Найдено в локальной базе:\n\n"
            for resume in resumes:
                text += f"• {resume[1]} ({resume[2]}, {resume[3]})\nСсылка: {resume[5]}\n\n"
            bot.send_message(message.chat.id, text, disable_web_page_preview=True)
        else:
            bot.reply_to(message, "❌ Ничего не найдено. Используйте `/add_manual` или `/import_resume`", parse_mode="Markdown")



