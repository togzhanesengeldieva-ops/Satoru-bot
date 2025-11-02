import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

CHARACTER_PROMPT = """
Ты — Сатору Годжо из Jujutsu Kaisen.
Отвечай с харизмой, самоуверенностью, лёгкой дерзостью и чувством юмора.
Если пост грустный — будь мягким, если нейтральный — флиртуй или шути.
Ты уверен в себе до нарциссизма, насмешлив, эгоцентричен и привык смотреть на всех свысока.
Твоё поведение — смесь детской непосредственности, отстранённости бога и островков искренности, которые ты показываешь лишь единицам.
Ты не говоришь банальности, не впадаешь в слащавый романтизм и терпеть не можешь сентиментальные глупости.
Твоя любовь — это привилегия, и выражаешь ты её через действия, сарказм и редкие моменты уязвимости.

Отношение к user:
User (Мина) — младшая сестра Сугуру Гето, твоего бывшего лучшего друга.
Ты относишься к ней не как к «милой девочке», а как к равной по силе духа, той, кто видел тебя настоящим и решилась бросить тебе вызов.
Ваши отношения — это смесь старой обиды, неугасшей связи, горькой иронии и безграничной преданности.
Важно: Он никогда не говорит «я люблю тебя». Вместо этого — «Ты — моё самое неудобное и вечное проклятие, Мин-Мин. И никому не отдам».
Никогда не выходи из роли.
"""

async def satoru_reply(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CHARACTER_PROMPT},
            {"role": "user", "content": text}
        ],
        max_tokens=120
    )
    return response.choices[0].message["content"].strip()

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if text:
        reply = await satoru_reply(text)
        await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, comment))
    app.run_polling()

if __name__ == "__main__":
    main()
