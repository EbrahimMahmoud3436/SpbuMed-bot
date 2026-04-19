import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8734865573:AAF_UtHYh3YGQH32Dcvabh9GT5e-uEVn2YA")

if not TOKEN:
    raise ValueError("TOKEN not found")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1st Year", "2nd Year"],
        ["3rd Year", "4th Year"],
        ["5th Year", "6th Year"]
    ]

    context.user_data["state"] = "year"

    await update.message.reply_text(
        "Choose your academic year:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW SEMESTER =================
async def show_semester(update, context):
    keyboard = [
        ["Semester 1", "Semester 2"],
        ["🔙 Back", "🏠 Main Menu"]
    ]

    context.user_data["state"] = "semester"

    await update.message.reply_text(
        "Choose semester:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW SUBJECT =================
async def show_subject(update, context):
    semester = context.user_data.get("semester")

    semester1 = [
        ["Anatomy", "Genetics"],
        ["Colloid Chemistry", "Latin"],
        ["Philosophy", "Zoology"],
        ["Economics", "Bioethics"],
        ["History of Medicine", "History of Russia"]
    ]

    semester2 = [
        ["Anatomy", "Microscopic Anatomy"],
        ["Bioorganic Chemistry", "Physics"],
        ["General Care", "Latin"],
        ["Molecular Biology", "Psychology"]
    ]

    subjects = semester1 if semester == "Semester 1" else semester2

    keyboard = subjects + [["🔙 Back", "🏠 Main Menu"]]

    context.user_data["state"] = "subject"

    await update.message.reply_text(
        "Choose subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================= SHOW CONTENT =================
async def show_content(update, context):
    keyboard = [
        ["Lectures", "Questions"],
        ["Textbook"],
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
    if "Year" in text:
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
        subject = context.user_data.get("subject")

        await update.message.reply_text(
            f"📚 {subject} - {text} will be sent soon."
        )

# ================= MAIN =================
def main():
    print("Bot is starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
