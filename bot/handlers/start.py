from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие и запуск сценария консультации."""
    await update.message.reply_text(
        "Привет! Я AI-консультант по подбору авто 🚗\n"
        "Помогу выбрать модель, рассчитать стоимость привоза и подготовить вас к покупке."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Справка по возможностям бота."""
    await update.message.reply_text("Напишите ваш бюджет, предпочтения и страну ввоза — и я начну подбор.")
