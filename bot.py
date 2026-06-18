import os
import logging
import datetime
from datetime import date as _real_date
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_MODE = False
TEST_START = datetime.datetime.now()

class date(_real_date):
    @classmethod
    def today(cls):
        if TEST_MODE:
            minutes_elapsed = int((datetime.datetime.now() - TEST_START).total_seconds() / 10)
            fake_date = _real_date(2026, 6, 30) - datetime.timedelta(days=5) + datetime.timedelta(days=minutes_elapsed)
            return cls(fake_date.year, fake_date.month, fake_date.day)
        return cls.fromordinal(_real_date.today().toordinal())


TARGET_DATE = date(2026, 6, 30)
START_DATE = _real_date(2026, 6, 18)

PLACEHOLDER_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFT4TocoCVPleYB55SzVry-k2Kz0G6IRBQ_g&s"
PLACEHOLDER_IMAGE_URL2 = "https://i2.wp.com/www.printableapplication.com/wp-content/uploads/2022/11/fillable-mcdonalds-application-form-printable-pdf-download-5.png"

ART_PAST = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⠒⠈⠉⣠⣤⣤⣄⠈⠁⠒⢤⣤⣤⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠀⠀⣠⣶⣿⣿⣶⣎⠁⠀⠀⠀⠀⠻⠋⠁⠈⠀⠀⠀⠈⠉⠻⡇⠀⠀⠀⠀⠛⠛⠛⠛⠛⢻⣿⣿⣿⠟⠁
⠀⣼⣿⡟⠉⡹⡿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠀⠀⠀⠑⢜⣆⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠋⠀⠀
⢠⣿⣿⣧⣶⣷⣦⣄⠀⠀⠀⠀⠀⣀⣠⢤⠤⠤⠤⣵⣤⣤⠐⢒⡏⡄⠀⠀⠀⠀⠀⣼⣿⣿⣿⠃⠀⠀⠀
⢸⣿⣿⡟⡍⠙⣿⣿⡆⠀⠀⠀⠸⡁⢿⣿⠇⠀⠀⣼⠿⠿⠀⢠⡟⡇⠀⠀⠀⠀⣰⣿⣿⣿⡇⠀⠀⠀⠀
⠈⣿⣿⡆⣇⢀⣿⣿⡇⠀⠀⠀⠀⠑⠤⣀⡀⠤⠊⠀⠑⠂⠰⠟⠁⡇⠀⠀⠀⢀⣿⣿⣿⣿⠁⠀⠀⠀⠀
⠀⠙⢿⣿⣾⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⢠⠁⡹⠋⠩⣭⣤⣤⡀⠀⠀
⠀⠀⠀⠉⢹⣏⡉⢦⠀⠀⠀⠀⠀⠀⢤⠄⣀⣀⣀⣀⣀⣀⡀⢀⠆⠀⠀⠀⣂⠒⠂⢉⠐⠚⠚⢲⠇⠀⠀
⠀⡔⠀⠏⠓⢷⣼⡿⡓⡦⡀⠀⠀⠀⠀⠀⣠⣀⣀⡀⠀⠀⢠⠎⠀⠀⠀⠀⠙⠛⠋⠉⠉⠉⠉⠁⠀⠀⠀
⠀⠈⠈⠑⠒⠛⢇⣨⣿⣼⣃⡀⠀⠀⠀⠀⠀⠉⠀⠀⣀⠴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠷⠶⠶⠶⠶⠶⢒⣉⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⠀⡟⢿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠁⠀⠀⡇⠀⢻⡿⣿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠟⠈⡻⣿⡿⣶⠤⢼⣧⣴⡅⠉⠋⡁⣀⣌⣹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣄⡜⠀⠘⠋⠀⣠⣆⣨⣯⠓⠯⠩⠭⠷⠛⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠺⠯⣛⣉⣭⠱⠤⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

ART_REVEAL = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀
⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠛⠛⠿⠿⢿⣿⣦⣠⣄⡀⣠⠿⣿⣿⣿⣿⠟⠛⠛⠛⠛⢿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠋⠀⣀⠀⠈⢻⡏⠀⢀⢤⣤⣤⡹⣿⣿⡇⠀⠀⠀⠀⠙
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⠺⣿⡆⢸⣷⠀⡼⠉⠙⢻⣟⠸⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡀⠀⣼⡗⣾⣿⣷⡿⣀⣀⡾⣻⣾⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣄⣨⣵⣾⣿⣿⣿⣿⣶⣶⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠠⡛⠿⠟⠋⠞⠻⠿⠿⢎⡉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⠀⢼⡄⠀⢀⣴⣿⡿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⣄⡀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠠⠶⠖⣪⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣸⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢀⣤⣶⣿⡿⠛⣀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⢸⡇⠀⠀⠛⠛⠋⢉⣤⣾⣿⣷⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠀⢸⡇⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⡎⡇⠀⢠⣿⣿⣿⣿⣿⣿⡿⠈⣿⡇⠀⠀⠀⠀⠀
⢿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⡇⣿⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⢻⣷⠀⠀⠀⠀⠀
⣽⣿⣿⣿⣿⣿⣿⣿⣿⡟⢄⡇⢹⠀⠈⢿⣿⣿⣿⣿⣿⣿⠀⢨⣿⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⡁⠸⠀⠀⣼⣿⣿⣿⣿⣿⣿⠀⣾⡏⠀⠀⠀⠀⠀
⣹⣯⣭⣭⣄⣸⣅⡀⠀⠀⢸⡇⠘⠀⠀⢻⣿⣿⣿⣿⣿⡿⢠⣿⠁⠀⠀⠀⠀⠀
⢹⣿⣿⣿⣿⣿⣿⡇⠀⠀⢸⣧⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⣼⡏⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⢀⠙⡎⠀⠀⠀⣿⣿⣿⣿⣿⠋⡽⠃⠀⠀⠀⠀⠀⠀
⠸⠿⠿⠿⠿⠿⠻⠃⠀⠀⢀⣵⠇⠀⠀⠀⠀⢾⣿⣿⠃⠔⠁⠀⠁⠛⠒⠷⠒⠒
"""


def build_progress_bar(days_left: int, total_days: int) -> str:
    BAR_LENGTH = 20
    elapsed = total_days - days_left
    filled = round((elapsed / total_days) * BAR_LENGTH)
    filled = max(0, min(BAR_LENGTH, filled))
    empty = BAR_LENGTH - filled
    bar = "█" * filled + "░" * empty
    percent = round((elapsed / total_days) * 100)
    return f"[{bar}] {percent}%"


def build_countdown_message(days_left: int) -> str:
    joke = ""
    total_days = (TARGET_DATE - START_DATE).days
    if days_left < 0:
        return None
    if days_left == 0:
        return None
    progress = build_progress_bar(days_left, total_days)
    if days_left == 11:
        joke = "what do you call a 2 time travelling ducks?\n a pair of ducks (paradox) im so funni wow"
    if days_left == 10:
        joke = "What do you call a smelly car?\n this car stink" 
    if days_left== 9:
        joke = "Can you imagine being stuck in norway?\n Help there is norway out, (yes i know this one suck, im tryinn)"
    if days_left == 8:
        joke = "why do british people say wah er instead of water?\n Cos they drank the t"
    if days_left == 7:
        joke = "Whats faster than a calculator?\n A calcu NOW (lowkey everytime i type a joke i wanna kms)"
    if days_left == 6:
        joke = "Did you know that currently lance isnt a very popular name?\n But in medieval times people were called lance alot"
    if days_left == 5:
        joke = "What do you call a cheap circumcision?\n a rip off"
    if days_left == 4:
        joke = "Why does the trans man eat a sald?\n Cos he was a her before"
    if days_left == 3:
        joke = "What would happen to my parents if i became trans?\n they would disappear cos they would be a trans-parent"
    if days_left == 2:
        joke = "Why can't you hear a Pterodactyl go to the bathroom?\n because their P is silent"
    if days_left == 1:
        joke = "i cant think of more lmfao BUT YIPEE 1 more day LMFAO"

    emoji = "⏳"
    hype = "shibal almost thr gang."
    return (
        f"{emoji} *COUNTDOWN TO JUNE 30* {emoji}\n\n"
        f"{progress}\n\n"
        f"📅 *{days_left} day{'s' if days_left != 1 else ''} remaining*\n\n"
        f"_{hype}_\n"
        f"_{joke}_"
    )


async def send_countdown(bot, chat_id: int):
    today = date.today()
    days_left = (TARGET_DATE - today).days

    if days_left < 0:
        return

    if days_left == 0:
        await bot.send_message(chat_id=chat_id, text="FREEDOMMM")
        await bot.send_message(chat_id=chat_id, text=f"```\n{ART_REVEAL.strip()}\n```", parse_mode="Markdown")
        await bot.send_photo(chat_id=chat_id, photo=PLACEHOLDER_IMAGE_URL, caption="yipeeeeee")
        await bot.send_photo(chat_id=chat_id, photo=PLACEHOLDER_IMAGE_URL2, caption="join me gng")
        return

    msg = build_countdown_message(days_left)
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")


async def scheduled_job(context: ContextTypes.DEFAULT_TYPE):
    await send_countdown(context.bot, context.job.chat_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Remove existing jobs for this chat to avoid duplicates
    for job in context.job_queue.get_jobs_by_name(str(chat_id)):
        job.schedule_removal()

    if TEST_MODE:
        context.job_queue.run_repeating(
            scheduled_job,
            interval=10,
            first=0,
            chat_id=chat_id,
            name=str(chat_id)
        )
        await update.message.reply_text("🧪 TEST MODE: sending countdown every minute!")
    else:
        context.job_queue.run_daily(
            scheduled_job,
            time=datetime.time(1, 0, 0),   # 9am SGT
            chat_id=chat_id,
            name=str(chat_id)
        )
        await update.message.reply_text("Onionhaseyaurrrr")
        # Send immediately on /start
        await send_countdown(context.bot, chat_id)


async def days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual check — doesn't re-subscribe"""
    await send_countdown(context.bot, update.effective_chat.id)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("days", days))

    logger.info("Bot is running... TEST_MODE=%s", TEST_MODE)
    app.run_polling()


if __name__ == "__main__":
    main()