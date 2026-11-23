"""Telegram bot for English–Russian translation."""

from __future__ import annotations

import logging
import os

from deep_translator import GoogleTranslator, MyMemoryTranslator
from dotenv import load_dotenv
from langdetect import DetectorFactory, LangDetectException, detect
from telebot import TeleBot, types

LOGGER = logging.getLogger(__name__)
SUPPORTED_LANGUAGES = {"en", "ru"}
DetectorFactory.seed = 0
TRANSLATION_PROVIDERS = (
    ("Google", GoogleTranslator),
    ("MyMemory", MyMemoryTranslator),
)


def detect_language(text: str) -> str:
    """Detect the source language and limit translation to English and Russian."""
    if any("\u0400" <= character <= "\u04ff" for character in text):
        return "ru"

    try:
        language = detect(text)
    except LangDetectException as error:
        if text.isascii() and any(character.isalpha() for character in text):
            return "en"
        raise ValueError("Could not detect the text language.") from error

    if language not in SUPPORTED_LANGUAGES:
        if text.isascii() and len(text.split()) == 1:
            return "en"
        raise ValueError("Only English and Russian texts are supported.")
    return language


def translate_variants(text: str, source: str, target: str) -> list[tuple[str, str]]:
    """Collect distinct translations, keeping the providers that succeed."""
    variants: list[tuple[str, str]] = []
    seen: set[str] = set()

    for provider_name, provider in TRANSLATION_PROVIDERS:
        try:
            translation = provider(source=source, target=target).translate(text)
        except Exception as error:  # Network/provider errors should not stop the bot.
            LOGGER.warning(
                "%s translation provider failed (%s)",
                provider_name,
                type(error).__name__,
            )
            continue

        if not translation:
            continue

        translation = translation.strip()
        normalized = translation.casefold()
        if translation and normalized not in seen:
            variants.append((provider_name, translation))
            seen.add(normalized)

    return variants


def create_bot(token: str) -> TeleBot:
    """Create the bot and register its message handlers."""
    bot = TeleBot(token)
    active_users: set[tuple[int, int]] = set()

    @bot.message_handler(commands=["start", "help", "cancel"])
    def handle_command(message: types.Message) -> None:
        if message.from_user is None or message.text is None:
            return

        user_key = (message.chat.id, message.from_user.id)
        command = message.text.split(maxsplit=1)[0].split("@", maxsplit=1)[0].lower()

        if command == "/start":
            active_users.add(user_key)
            bot.reply_to(
                message,
                "Привет! Я перевожу между английским и русским и показываю "
                "варианты от нескольких сервисов. Пришли текст для перевода.\n\n"
                "Команды: /help — помощь, /cancel — завершить перевод.",
            )
        elif command == "/help":
            bot.reply_to(
                message,
                "Пришли текст на английском или русском — я определю язык и "
                "попробую получить варианты перевода. Чтобы остановить режим, "
                "напиши /cancel.",
            )
        else:
            active_users.discard(user_key)
            bot.reply_to(
                message,
                "Режим перевода завершён. Напиши /start, чтобы начать.",
            )

    @bot.message_handler(content_types=["text"])
    def translate_message(message: types.Message) -> None:
        if message.from_user is None or not message.text:
            return

        user_key = (message.chat.id, message.from_user.id)
        if message.text.startswith("/"):
            return
        if user_key not in active_users:
            bot.reply_to(message, "Напиши /start, чтобы начать перевод.")
            return

        try:
            source = detect_language(message.text)
        except ValueError as error:
            bot.reply_to(message, str(error))
            return

        target = "ru" if source == "en" else "en"
        variants = translate_variants(message.text, source, target)
        if not variants:
            bot.reply_to(
                message,
                "Сервисы перевода сейчас недоступны. Попробуй ещё раз позже.",
            )
            return

        lines = [f"Варианты перевода ({source} → {target}):"]
        lines.extend(
            f"{index}. {provider}: {translation}"
            for index, (provider, translation) in enumerate(variants, start=1)
        )
        bot.reply_to(message, "\n\n".join(lines))

    return bot


def main() -> None:
    """Load configuration and start long polling."""
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and set it."
        )

    LOGGER.info("Starting translation bot")
    create_bot(token).infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
