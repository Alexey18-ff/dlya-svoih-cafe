# -*- coding: utf-8 -*-
"""
Телеграм-бот для построения графиков функций.

Пользователь присылает боту функцию вида:
    sin(x) + x**2
    x**3 - 3*x, -5, 5      (можно указать диапазон x через запятую)

Бот парсит выражение с помощью sympy (безопаснее, чем встроенный eval),
строит график через matplotlib и отправляет картинку в чат.

Запуск:
    pip install -r requirements.txt
    export TELEGRAM_BOT_TOKEN="ваш_токен_от_BotFather"
    python bot.py
"""

import io
import logging
import os

import matplotlib
matplotlib.use("Agg")  # без GUI, чтобы работало на сервере
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Токен бота: берём из переменной окружения, чтобы не хранить в коде.
TOKEN = os.environ.get("8942980741:AAFW4iEZ9hWdhGWUXTj0nrV5dHu5cBou3N4", "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН")

DEFAULT_X_MIN = -10
DEFAULT_X_MAX = 10
POINTS = 1000

# На всякий случай ограничим набор разрешённых имён, которые может
# использовать sympy.sympify, чтобы пользователь не мог передать
# что-то опасное (например __import__ и т.п.)
ALLOWED_FUNCS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "ln": sp.log,
    "sqrt": sp.sqrt, "abs": sp.Abs, "Abs": sp.Abs,
    "pi": sp.pi, "E": sp.E,
}


def parse_user_message(text: str):
    """
    Разбирает сообщение пользователя вида:
        "sin(x)+x**2"
        "x**3 - 3*x, -5, 5"
    Возвращает (expr_str, x_min, x_max).
    """
    parts = [p.strip() for p in text.split(",")]
    expr_str = parts[0]

    x_min, x_max = DEFAULT_X_MIN, DEFAULT_X_MAX
    if len(parts) == 3:
        try:
            x_min = float(parts[1])
            x_max = float(parts[2])
        except ValueError:
            raise ValueError(
                "Не удалось распознать границы диапазона. "
                "Пример: sin(x), -5, 5"
            )
        if x_min >= x_max:
            raise ValueError("Левая граница диапазона должна быть меньше правой.")

    return expr_str, x_min, x_max


def build_plot(expr_str: str, x_min: float, x_max: float) -> io.BytesIO:
    """Строит график функции и возвращает картинку в виде байтового потока."""
    x = sp.symbols("x")

    local_dict = dict(ALLOWED_FUNCS)
    local_dict["x"] = x

    try:
        expr = sp.sympify(expr_str, locals=local_dict)
    except Exception as e:
        raise ValueError(
            f"Не удалось распознать функцию «{expr_str}».\n"
            f"Проверьте синтаксис (например: sin(x)+x**2, x**3-3*x, sqrt(x)).\n"
            f"Техническая ошибка: {e}"
        )

    free_symbols = expr.free_symbols
    if free_symbols - {x}:
        raise ValueError(
            "В функции можно использовать только переменную x "
            f"(найдены лишние переменные: {free_symbols - {x}})."
        )

    f = sp.lambdify(x, expr, modules=["numpy"])

    xs = np.linspace(x_min, x_max, POINTS)
    with np.errstate(all="ignore"):
        ys = f(xs)

    ys = np.array(ys, dtype=float)
    ys = np.where(np.isfinite(ys), ys, np.nan)  # прячем разрывы (деление на 0 и т.п.)

    if np.all(np.isnan(ys)):
        raise ValueError(
            "Функция не определена ни в одной точке заданного диапазона."
        )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, color="#1f77b4", linewidth=2)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"f(x) = {sp.sstr(expr)}")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я строю графики функций.\n\n"
        "Просто отправь мне функцию от x, например:\n"
        "  sin(x) + x**2\n"
        "  x**3 - 3*x\n"
        "  sqrt(abs(x))\n\n"
        "Можно задать диапазон по x через запятую:\n"
        "  sin(x), -5, 5\n\n"
        "Поддерживаемые функции: sin, cos, tan, asin, acos, atan, "
        "sinh, cosh, tanh, exp, log, ln, sqrt, abs, а также pi и E."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    try:
        expr_str, x_min, x_max = parse_user_message(text)
        image_buf = build_plot(expr_str, x_min, x_max)
    except ValueError as e:
        await update.message.reply_text(f"⚠️ {e}")
        return
    except Exception as e:
        logger.exception("Неожиданная ошибка при построении графика")
        await update.message.reply_text(
            "⚠️ Произошла непредвиденная ошибка при построении графика. "
            "Попробуйте другую функцию."
        )
        return

    await update.message.reply_photo(
        photo=image_buf,
        caption=f"f(x) = {expr_str}\nx ∈ [{x_min}, {x_max}]",
    )


def main() -> None:
    if TOKEN == "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН":
        raise RuntimeError(
            "Не задан токен бота. Установите переменную окружения "
            "TELEGRAM_BOT_TOKEN или впишите токен прямо в код (не рекомендуется)."
        )

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()