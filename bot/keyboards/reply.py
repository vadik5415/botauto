from telegram import KeyboardButton, ReplyKeyboardMarkup


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Reply-клавиатура для частых действий."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Подобрать авто"), KeyboardButton("Сравнить модели")]],
        resize_keyboard=True,
    )
