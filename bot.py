import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8734865573:AAHynJhTAOrraVIwF-_H0XfB82d2R0lz0Mk")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1st year", "2nd year"],
        ["3rd year", "4th year"],
        ["5th year", "6th year"]
    ]
    context.user_data.clear()
    context.user_data["state"] = "year"

    await update.message.reply_text(
        "Choose your year:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW SEMESTER =================
async def show_semester(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Semester 1", "Semester 2"], ["🔙 Back", "🏠 Main Menu"]]
    context.user_data["state"] = "semester"

    await update.message.reply_text(
        "Choose semester:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW SUBJECT =================
async def show_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    semester = context.user_data.get("semester")

    semester1 = [
        "Anatomy", "Genetics", "Colloid chemistry", "Latin",
        "Philosophy", "Zoology", "Economics", "Bioethics",
        "History of Medicine", "History of Russia"
    ]

    semester2 = [
        "Anatomy", "Microscopic Anatomy", "Bioorganic",
        "Physics", "General Care", "Latin",
        "Molecular Biology", "Psychology"
    ]

    subjects = semester1 if semester == "Semester 1" else semester2

    keyboard = [subjects[i:i+2] for i in range(0, len(subjects), 2)]
    keyboard.append(["🔙 Back", "🏠 Main Menu"])

    context.user_data["state"] = "subject"

    await update.message.reply_text(
        "Choose subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW CONTENT =================
async def show_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Lectures", "Questions"],
        ["Text Book"],
        ["🔙 Back", "🏠 Main Menu"]
    ]
    context.user_data["state"] = "content"

    await update.message.reply_text(
        "Choose content:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("state")

    # MAIN MENU
    if text == "🏠 Main Menu":
        return await start(update, context)

    # BACK
    if text == "🔙 Back":
        if state == "semester":
            return await start(update, context)
        elif state == "subject":
            return await show_semester(update, context)
        elif state == "content":
            return await show_subject(update, context)

    # YEAR
    if "year" in text:
        context.user_data["year"] = text
        return await show_semester(update, context)

    # SEMESTER
    if text in ["Semester 1", "Semester 2"]:
        context.user_data["semester"] = text
        return await show_subject(update, context)

    # SUBJECT
    if state == "subject":
        context.user_data["subject"] = text
        return await show_content(update, context)

    # CONTENT
    if state == "content":
        await update.message.reply_text(f"Sending {text} 📂...")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()