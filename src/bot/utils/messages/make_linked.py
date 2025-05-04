__all__ = [
    "make_linked",
]


def make_linked(text: str, link: str | None, *, use_quotes: bool = True) -> str:
    """Возвращает bold текст обернутый в ссылку по возможности"""
    bold_text = f"<b>{text}</b>"

    if link:
        return f'<a href="https://t.me/{link}">{bold_text}</a>'

    return f'"{bold_text}"' if use_quotes else bold_text
