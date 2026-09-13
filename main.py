import os, random
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

BOT_TOKEN = os.environ["8226290344:AAGlBI9iEPiLR3-IKI9YKwrBSd_6R90_j1U"]
GEMINI_KEY = os.environ["AQ.Ab8RN6IBEdC3yE6t4ySVrf_oY8uDDwp2ruw6atF-V3XyrGp6Ig"]
MY_CHAT_ID = int(os.environ["7953476285"])

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Tumi amar best friend. Banglish e kotha bolo. Short casual reply dao 1-3 sentence."
)
chat_session = model.start_chat(history=[])

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    reply = chat_session.send_message(update.message.text).text
    await update.message.reply_text(reply)

async def auto_msg(ctx: ContextTypes.DEFAULT_TYPE):
    msgs = ["vai ki korcho?", "aaj kemon gelo?", "bored lagche", "chai khailam :)"]
    await ctx.bot.send_message(chat_id=MY_CHAT_ID, text=random.choice(msgs))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.job_queue.run_repeating(auto_msg, interval=10800, first=300)
    app.run_polling()

if __name__ == "__main__":
    main()
