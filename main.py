import os, asyncio, random
from telegram import Update
from telegram.ext import (
    Application, MessageHandler,
    filters, ContextTypes
)
import google.generativeai as genai

BOT_TOKEN = os.environ["8226290344:AAGlBI9iEPiLR3-IKI9YKwrBSd_6R90_j1U"]
GEMINI_KEY = os.environ["AQ.Ab8RN6IBEdC3yE6t4ySVrf_oY8uDDwp2ruw6atF-V3XyrGp6Ig"]
MY_CHAT_ID = int(os.environ["7953476285"])

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
Tumi amar best friend. Banglish e kotha bolo
(Bengali + English mix, Roman horf e).
Jemon: "ki koro vai?", "valo achi, tumi?"
Natural, casual, short reply dao — 1-3 sentence max.
Kabhi kabhi niche theme e message pathao:
weather, food, random kotha.
"""
)

history = []

async def chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    history.append({"role": "user", "parts": [user_msg]})
    if len(history) > 20:
        history.pop(0)
    resp = model.start_chat(history=history[:-1])
    reply = resp.send_message(user_msg).text
    history.append({"role": "model", "parts": [reply]})
    await update.message.reply_text(reply)

async def auto_msg(ctx: ContextTypes.DEFAULT_TYPE):
    msgs = [
        "vai ki korcho ekhon?",
        "aaj kemon gelo din ta?",
        "ektu bored lagche tomar kotha mone porlo",
        "chai khailam abhi :)",
        "random kotha: tumi ki valo acho?",
    ]
    await ctx.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=random.choice(msgs)
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )
    # Har 3 ghontay ekta message pathabe
    app.job_queue.run_repeating(
        auto_msg, interval=10800, first=300
    )
    app.run_polling()

if __name__ == "__main__":
    main()
