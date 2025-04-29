import logging
import json
import random
import re
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv  # Novo

# Carrega variáveis do .env
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Setup de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Carrega dataset
with open("questions.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

# Armazenamento dos dados dos usuários
user_data = {}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 <b>Welcome to SASE Questions BOT</b>\n\n"
        "📌 <b>How to use:</b>\n"
        "1️⃣ Type <code>/quiz</code> to start a quiz.\n"
        "2️⃣ Enter how many questions you want (e.g., 3).\n"
        "3️⃣ Choose the correct answer from the options.\n"
        "4️⃣ You'll get explanations and a reference link for each question.\n\n"
        "🧠 Most questions are based on FortiSASE documentation and focus on concepts.\n"
        "💡 Use this as a tool to review your knowledge – not as a full training. Do the LABs!\n\n"
        "⚠️ <b>DISCLAIMER:</b>\n"
        "This is not a DUMP.\n"
        "All questions are generated using LLM (LLaMA) based on public documentation at https://docs.fortinet.com\n"
        "Each question includes the correct answer and a link to the official docs.\n"
        "Use this bot as a study assistant. Practical experience is essential.\n"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)

# Comando /quiz
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_data[user_id] = {"questions_left": 0, "current_question": None, "answered": 0}
    await update.message.reply_text(f"Quantas perguntas você quer responder? (Ex: 3)\nDisponíveis: {len(quiz_data)}")

# Handler para definir número de perguntas
async def set_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ Por favor, envie um número válido de perguntas.")
        return

    num = int(text)
    if num <= 0 or num > len(quiz_data):
        await update.message.reply_text(f"❌ Escolha um número entre 1 e {len(quiz_data)}.")
        return

    user_data[user_id]["questions_left"] = num
    await send_new_question(update, context)

# Função para enviar uma nova pergunta
async def send_new_question(update_or_query, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(update_or_query, Update):
        user_id = update_or_query.effective_user.id
        chat_id = update_or_query.effective_chat.id
    else:
        user_id = update_or_query.from_user.id
        chat_id = update_or_query.message.chat_id

    question = random.choice(quiz_data)
    options = list(question["options"].items())
    random.shuffle(options)
    correct_text = question["options"][question["correct_answer"]]

    shuffled_options = {}
    for idx, (key, value) in enumerate(options):
        letter = chr(65 + idx)
        shuffled_options[letter.lower()] = value

    user_data[user_id]["current_question"] = {
        "question": question["question"],
        "options": shuffled_options,
        "correct_text": correct_text,
        "explanation": question["explanation"],
        "reference": question.get("reference", "")
    }

    keyboard = [[InlineKeyboardButton(f"{letter}) {text}", callback_data=letter.lower())] for letter, text in shuffled_options.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"<b>Pergunta:</b>\n{question['question']}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

# Handler de resposta
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    selected = query.data
    state = user_data.get(user_id)

    if not state or not state.get("current_question"):
        await query.edit_message_text("⚠️ Nenhum quiz em andamento. Use /quiz para começar.")
        return

    q = state["current_question"]
    correct_letter = next((k.upper() for k, v in q["options"].items() if v == q["correct_text"]), "?")
    selected_text = q["options"].get(selected)
    result = "✅ <b>Correto!</b>" if selected_text == q["correct_text"] else f"❌ <b>Errado!</b> Resposta correta: <b>{correct_letter}</b>"

    explanation = re.sub(r':contentReference\[.*?\]\{.*?\}', '', q["explanation"]).replace("&#8203;", "").strip()
    link = q.get("reference", "")
    link_markdown = f'\n\n🔗 <a href="{link}">Documentação relacionada</a>' if link else ""

    full_response = (
        f"<b>Pergunta:</b>\n{q['question']}\n\n"
        f"{result}\n\n"
        f"📘 <b>Explicação:</b>\n<i>{explanation}</i>{link_markdown}"
    )

    await query.edit_message_text(full_response, parse_mode=ParseMode.HTML)

    state["questions_left"] -= 1
    state["answered"] += 1

    if state["questions_left"] > 0:
        await context.bot.send_message(chat_id=query.message.chat_id, text="⏭ Próxima pergunta:")
        await send_new_question(query, context)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"🏁 Quiz finalizado! Você respondeu {state['answered']} perguntas. 👏")
        del user_data[user_id]

# Execução do bot
if __name__ == '__main__':
    if not TELEGRAM_API_KEY:
        raise EnvironmentError("❌ TELEGRAM_API_KEY não encontrada no .env")
        
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_number))

    print("🚀 Bot iniciado. Pressione Ctrl+C para sair.")
    app.run_polling()
