import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_ai(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 120}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"]
        return "Thinking..."
    except:
        return "Error from AI."

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = query_ai(user_msg)
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Alex is live...")
app.run_polling()
