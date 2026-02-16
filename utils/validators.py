import re


def is_valid_phone(phone: str) -> bool:
    """Проверяет номер телефона в международном формате."""
    return bool(re.match(r"^\+?[1-9]\d{7,14}$", phone.strip()))
