import os
import logging
import phonenumbers
from phonenumbers import geocoder, carrier, number_type
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "8156543278:AAEl5zqF8deAD7Qs7W1mZLRaRiiqb6wg_Yc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Бот на связи в облаке Render! Отправь номер в формате +7...")

async def search_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw_phone = update.message.text.strip()
    try:
        parsed_number = phonenumbers.parse(raw_phone, None)
        if not phonenumbers.is_valid_number(parsed_number):
            await update.message.reply_text("❌ Некорректный номер.")
            return

        country = geocoder.description_for_number(parsed_number, "ru") or "Не определено"
        supplier = carrier.name_for_number(parsed_number, "ru") or "Не определен"
        n_type = number_type(parsed_number)
        type_str = "Мобильный" if n_type == phonenumbers.PhoneNumberType.MOBILE else "Другой"
        formatted_num = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        response_text = (
            f"🔍 **Результат из облака:**\n\n"
            f"📱 `{formatted_num}`\n"
            f"🌍 Регион: {country}\n"
            f"📡 Оператор: {supplier}\n"
            f"📞 Тип: {type_str}"
        )
        await update.message.reply_text(response_text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Ошибка: отправляй номер обязательно с плюсом (+7...)")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_number))
    
    print("[+] Бот запущен в облаке Render!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
