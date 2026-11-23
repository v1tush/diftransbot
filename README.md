# DifTransBot

A small Telegram bot that detects English or Russian text and returns distinct
translation options from Google Translate and MyMemory. If one provider is
unavailable, the other can still respond. Language detection runs locally; no
DetectLanguage API key is needed.

## Features

- English ↔ Russian translation;
- automatic source-language detection;
- distinct results from multiple translation providers;
- per-user translation mode with `/start`, `/help`, and `/cancel`;
- configuration through environment variables instead of credentials in code.

## Requirements

- Python 3.10 or newer;
- a Telegram bot token from [@BotFather](https://t.me/BotFather).

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Telegram bot token:

```env
TELEGRAM_BOT_TOKEN=your_token_from_botfather
```

Run the bot:

```bash
python bot.py
```

Send `/start` to the bot, then send an English or Russian text. Use `/cancel` to
leave translation mode.

Run the offline test suite with:

```bash
python -m unittest discover -s tests
```

Language detection is approximate. Cyrillic text is treated as Russian, while a
single short Latin-script word defaults to English so words such as “hello” are
not misclassified.

## Configuration and security

Never commit `.env` or paste bot tokens into source code. The repository ignores
`.env` by default. If a token or API key was previously committed, revoke it at
its provider; removing it from the current code does not invalidate the old key.

Translation providers require an internet connection and may rate-limit requests.
