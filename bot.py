import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== TOKEN =====
TOKEN = os.environ.get("8734865573:AAF_UtHYh3YGQH32Dcvabh9GT5e-uEVn2YA")
if not TOKEN:
    raise ValueError("TOKEN not found")

# ===== DATA =====
DATA = {
    "1st year": {
        "Semester 1": [
            "Anatomy", "Genetics", "Colloid Chemistry", "Latin",
            "Philosophy", "Zoology", "Economics", "Bioethics",
            "History of Medicine", "History of Russia"
        ],
        "Semester 2": [
            "Anatomy", "Microscopic Anatomy", "Bioorganic",
            "Physics", "General Care", "Latin",
            "Molecular Biology", "Psychology"
        ]
    },
    # تقدر تزود باقي السنين هنا بنفس الشكل
}

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[y] for y in DATA.keys()]
    await update.message.reply_text(
        "Choose your year:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    context.user_data["state"] = "year"

# ===== HANDLE =====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("state")

    # ===== YEAR =====
    if state == "year" and text in DATA:
        context.user_data["year"] = text
        semesters = list(DATA[text].keys())
        keyboard = [[s] for s in semesters]

        await update.message.reply_text(
            "Choose semester:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        context.user_data["state"] = "semester"
        return

    # ===== SEMESTER =====
    if state == "semester":
        year = context.user_data.get("year")
        if year and text in DATA[year]:
            context.user_data["semester"] = text
            subjects = DATA[year][text]
            keyboard = [[s] for s in subjects]

            await update.message.reply_text(
                "Choose subject:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            context.user_data["state"] = "subject"
            return

    # ===== SUBJECT =====
    if state == "subject":
        await update.message.reply_text(
            f"You selected: {text}\n\nContent will be added soon 📚"
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()