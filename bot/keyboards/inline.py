from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_inline_keyboard() -> InlineKeyboardMarkup:
    """Быстрая inline-навигация."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Рассчитать стоимость", callback_data="calc")]]
    )
