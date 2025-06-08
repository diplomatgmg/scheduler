import calendar
from datetime import datetime
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback  # type: ignore[import-untyped]
from aiogram_calendar.schemas import SimpleCalAct  # type: ignore[import-untyped]
from loguru import logger
from pydantic import BaseModel

from bot.callbacks.noop import NoopCallback


__all__ = ["CustomCalendar"]


def highlight(text: str | int) -> str:
    return f"🔸 {text}"


class RussianCalendarLabels(BaseModel):
    days_of_week: list[str] = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    months: list[str] = ["Янв", "Фев", "Мар", "Апр", "Май", "Июнь", "Июль", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    cancel_caption: str = "Назад"
    today_caption: str = "Сегодня"


class CustomCalendar(SimpleCalendar):  # type: ignore[misc]
    def __init__(self, locale: str | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if locale == "ru":
            self._labels = RussianCalendarLabels()

    async def start_calendar(
        self, year: int = datetime.now().year, month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        kb: list[list[InlineKeyboardButton]] = []

        today = datetime.now()
        now_year, now_month, now_day = today.year, today.month, today.day
        month_str = self._labels.months[month - 1]
        now_weekday = self._labels.days_of_week[today.weekday()]

        year_row: list[InlineKeyboardButton] = []

        if today.year <= now_year:
            year_row.append(InlineKeyboardButton(text=" ", callback_data=NoopCallback().pack()))
        else:
            year_row.append(
                InlineKeyboardButton(
                    text="←",
                    callback_data=SimpleCalendarCallback(act=SimpleCalAct.prev_y, year=year, month=month, day=1).pack(),
                )
            )

        year_row.append(  # noqa: FURB113
            InlineKeyboardButton(
                text=highlight(now_year) if now_year == today.year else str(now_year),
                callback_data=self.ignore_callback,
            )
        )
        year_row.append(
            InlineKeyboardButton(
                text="→",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.next_y, year=year, month=month, day=1).pack(),
            )
        )

        kb.append(year_row)

        month_row: list[InlineKeyboardButton] = []

        if today.month <= now_month:
            month_row.append(InlineKeyboardButton(text=" ", callback_data=NoopCallback().pack()))
        else:
            month_row.append(
                InlineKeyboardButton(
                    text="←",
                    callback_data=SimpleCalendarCallback(act=SimpleCalAct.prev_m, year=year, month=month, day=1).pack(),
                )
            )

        month_row.append(  # noqa: FURB113
            InlineKeyboardButton(  # noqa: FURB113
                text=highlight(month_str) if now_month == today.month else month_str, callback_data=self.ignore_callback
            )
        )
        month_row.append(
            InlineKeyboardButton(
                text="→",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.next_m, year=year, month=month, day=1).pack(),
            )
        )
        kb.append(month_row)

        week_days_labels_row = []

        def is_current_weekday(wd: str) -> bool:
            return now_year == today.year and now_month == today.month and wd == now_weekday

        for weekday in self._labels.days_of_week:
            week_days_labels_row.append(  # noqa: PERF401
                InlineKeyboardButton(
                    text=highlight(weekday) if is_current_weekday(weekday) else weekday,
                    callback_data=self.ignore_callback,
                )
            )

        kb.append(week_days_labels_row)

        def is_current_day(d: int) -> bool:
            return now_year == today.year and now_month == today.month and d == now_day

        def is_previous_day(d: int) -> bool:
            return now_year <= today.year and now_month <= today.month and d < now_day

        month_calendar = calendar.monthcalendar(today.year, today.month)

        for week in month_calendar:
            days_row = []
            for day in week:
                if day == 0 or is_previous_day(day):
                    days_row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
                    continue

                days_row.append(
                    InlineKeyboardButton(
                        text=highlight(day) if is_current_day(day) else str(day),
                        callback_data=SimpleCalendarCallback(act=SimpleCalAct.day, day=day).pack(),
                    )
                )
            kb.append(days_row)

        cancel_row = []
        cancel_row.append(  # noqa: FURB113
            InlineKeyboardButton(
                text=self._labels.cancel_caption,
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.cancel, year=year, month=month, day=day).pack(),
            )
        )
        cancel_row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
        cancel_row.append(
            InlineKeyboardButton(
                text=self._labels.today_caption,
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.today, year=year, month=month, day=day).pack(),
            )
        )
        kb.append(cancel_row)

        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)
