from telegram import Update
from telegram.ext import ContextTypes


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для админа: показывает базовую статистику."""
    await update.message.reply_text("Админ-статистика пока в разработке.")
