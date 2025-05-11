from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Sug'urta manzillari va havolalari
insurance_locations = {
    "Alskom": "https://maps.app.goo.gl/9s4dGMipoKq5Pwxy7",
    "Apex sug'urta": "https://yandex.ru/navi/org/apex_tower/126085454022?si=vd65g571rg8j3c60eytma4311w",
    "KAPITAL SUG'URTA": "https://yandex.uz/maps/-/CDWSiWjS",
    "ALFA INVEST": "https://yandex.uz/maps/-/CDWSi6Mg",
    "KAFOLAT SUG'URTA": "https://yandex.uz/maps/-/CDHjbKlM",
    "INSON SUG'URTA": "https://yandex.uz/maps/-/CDWSiAjD",
    "ISHONCH SUG'URTA": "https://yandex.uz/maps/-/CDWSeXO8",
    "O'ZBEK INVEST SUG'URTA": "https://yandex.uz/maps/-/CDWSeHKa",
    "O'Z AGRO SUG'URTA": "https://yandex.uz/maps/-/CDWSa2ms",
    "TEMIRYO'L SUG'URTA": "https://yandex.uz/maps/-/CDWSaP4V",
    "GROSS SUG'URTA": "https://yandex.uz/mCDWSaDzaaps/-/",
    "NEO SUG'URTA": "https://yandex.uz/maps/-/CDWSaBZ9",
    "EURO ASIA ISURANCE": "https://yandex.uz/maps/-/CDWSaU4r",
    "ASIA INSURANCE": "https://yandex.uz/maps/-/CDWSaENG",
    "KAFIL SUG'URTA": "https://yandex.uz/maps/-/CDWS4Xj2",
    "SQB SUG'URTA": "https://yandex.uz/maps/-/CDWS4DKw",
	"MY INSURANCE": "https://yandex.uz/maps/-/CDWS46-8",
    "PERFECT INSURANCE": "https://yandex.uz/maps/-/CDWS4R81",
    "KAPITAL SUG'URTA EVROPROTOCOL TOPSHIRISH": "https://yandex.uz/maps/-/CDWS4FIp",
    "NARKOLOGIYA": "https://yandex.uz/maps/-/CDWdAEKx",
    "INFINITY SUG'URTA": "https://yandex.uz/maps/-/CDcZRWI9",
    "IMPEX INSURANCE": "https://yandex.uz/maps/-/CDgjuZIK",
}

# Kanalga obuna bo'lish uchun havola
CHANNEL_LINK = 'https://t.me/eprotocol'

# Lokatsiya tugmalarini yaratish
def create_location_buttons():
    return [
        [InlineKeyboardButton(name, url=url)]
        for name, url in insurance_locations.items()
    ]

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id

    try:
        member = await context.bot.get_chat_member('@eprotocol', chat_id)
        if member.status not in ['member', 'administrator', 'creator']:
            keyboard = [
                [
                    InlineKeyboardButton("📢 Obuna bo'lish", url=CHANNEL_LINK),
                    InlineKeyboardButton("📍 Lokatsiyani olish", callback_data='get_location')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "Iltimos, kanalga obuna bo‘ling va yana /start buyrug‘ini yuboring.",
                reply_markup=reply_markup
            )
            return
    except Exception as e:
        print(f"Error during membership check: {e}")
        return

    # Obuna bo‘lsa, lokatsiyalarni yuborish
    keyboard = create_location_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📍 Sug'urta lokatsiyalari:", reply_markup=reply_markup)

# Lokatsiya olish tugmasi bosilganda
async def handle_location(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat.id

    try:
        member = await context.bot.get_chat_member('@eprotocol', chat_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = create_location_buttons()
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.edit_text("📍 Sug'urta manzillari:\nQuyidagilardan birini tanlang:", reply_markup=reply_markup)
        else:
            keyboard = [
                [
                    InlineKeyboardButton("📢 Obuna bo'lish", url=CHANNEL_LINK),
                    InlineKeyboardButton("📍 Lokatsiyani olish", callback_data='get_location')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.edit_text(
                "Iltimos, kanalga obuna bo‘ling va yana /start buyrug‘ini yuboring.",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error in handle_location: {e}")
        return

# Botni ishga tushirish
def main() -> None:
    application = Application.builder().token("7283569631:AAGA56_rEsp60_d4c0gyBRzzYE6VEi9TZN4").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_location, pattern="get_location"))

    print("✅ Bot ishga tushdi.")
    application.run_polling()

if __name__ == "__main__":
    main()
