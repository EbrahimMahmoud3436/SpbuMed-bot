from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8734865573:AAFbq8bOupIyo_RnuNPx__6uKzTckfa8u1o"

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1st year", "2nd year"],
        ["3rd year", "4th year"],
        ["5th year", "6th year"]
    ]
    context.user_data["state"] = "year"
    await update.message.reply_text(
        "Choose your year:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== HANDLE =====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("state")

    # 🏠 Main Menu
    if text == "🏠 Main Menu":
        return await start(update, context)

    # 🔙 Back
    if text == "🔙 Back":
        if state == "semester":
            return await start(update, context)
        elif state == "subject":
            return await show_semester(update, context)
        elif state == "content":
            return await show_subject(update, context)

    # ===== YEAR =====
    if "year" in text:
        context.user_data["year"] = text
        return await show_semester(update, context)

    # ===== SEMESTER =====
    if text in ["Semester 1", "Semester 2"]:
        context.user_data["semester"] = text
        return await show_subject(update, context)

    # ===== SUBJECT =====
    semester = context.user_data.get("semester")

    semester1_subjects = [
        "Anatomy", "Genetics", "Colloid chemistry", "Latin",
        "Philosophy", "Zoology", "Economics", "Bioethics",
        "History of Medicine", "History of Russia"
    ]

    semester2_subjects = [
        "Anatomy",
        "Microscopic Anatomy",
        "Bioorganic",
        "Physics",
        "General Care",
        "Latin",
        "Molecular Biology",
        "Psychology"
    ]

    if text in semester1_subjects + semester2_subjects:
        context.user_data["subject"] = text
        return await show_content(update, context)

    # ===== CONTENT =====
    if text in [
        "Lectures", "Books", "Questions", "Summaries",
        "Labs", "Seminars", "Homework",
        "Practicals", "Checklist", "Mock Exams"
    ]:
        subject = context.user_data.get("subject")
        await update.message.reply_text(f"Sending {subject} {text} 📂")

# ===== SEMESTER MENU =====
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

# ===== SUBJECT MENU =====
async def show_subject(update, context):
    semester = context.user_data.get("semester")

    if semester == "Semester 1":
        keyboard = [
            ["Anatomy", "Genetics"],
            ["Colloid chemistry", "Latin"],
            ["Philosophy", "Zoology"],
            ["Economics", "Bioethics"],
            ["History of Medicine", "History of Russia"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    else:  # Semester 2
        keyboard = [
            ["Anatomy", "Microscopic Anatomy"],
            ["Bioorganic", "Physics"],
            ["General Care", "Latin"],
            ["Molecular Biology", "Psychology"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    context.user_data["state"] = "subject"
    await update.message.reply_text(
        "Choose subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== CONTENT MENU =====
async def show_content(update, context):
    subject = context.user_data.get("subject")

    # Semester 2 custom menus
    if subject == "General Care":
        keyboard = [
            ["Books", "Practicals"],
            ["Checklist"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    elif subject == "Psychology":
        keyboard = [
            ["Lectures", "Mock Exams"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    elif subject in ["Anatomy", "Microscopic Anatomy", "Physics"]:
        keyboard = [
            ["Books", "Lectures"],
            ["Labs", "Summaries"],
            ["Questions"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    elif subject == "Bioorganic":
        keyboard = [
            ["Books", "Questions"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    elif subject == "Latin":
        keyboard = [
            ["Lectures", "Books"],
            ["Summaries"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    else:
        keyboard = [
            ["Lectures", "Books"],
            ["Questions", "Summaries"],
            ["🔙 Back", "🏠 Main Menu"]
        ]

    context.user_data["state"] = "content"
    await update.message.reply_text(
        "Choose content:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== MAIN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot is running...")
app.run_polling()