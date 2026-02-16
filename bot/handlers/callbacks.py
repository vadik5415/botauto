from telegram import Update
from telegram.ext import ContextTypes


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает callback от inline-кнопок."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Вы выбрали: {query.data}")
