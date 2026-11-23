import unittest
from unittest.mock import patch

import bot


class FakeTranslator:
    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target

    def translate(self, text: str) -> str:
        return "translated text"


class LanguageDetectionTests(unittest.TestCase):
    def test_detects_english_sentence(self) -> None:
        self.assertEqual(
            bot.detect_language("This is a clear English sentence."),
            "en",
        )

    def test_detects_russian_from_cyrillic_script(self) -> None:
        self.assertEqual(bot.detect_language("Привет"), "ru")

    def test_short_latin_word_defaults_to_english(self) -> None:
        self.assertEqual(bot.detect_language("hello"), "en")

    def test_rejects_unsupported_language(self) -> None:
        with self.assertRaises(ValueError):
            bot.detect_language("Bonjour, comment allez-vous aujourd'hui?")


class TranslationTests(unittest.TestCase):
    def test_duplicate_translations_are_removed(self) -> None:
        providers = (("First", FakeTranslator), ("Second", FakeTranslator))
        with patch.object(bot, "TRANSLATION_PROVIDERS", providers):
            variants = bot.translate_variants("hello", "en", "ru")

        self.assertEqual(variants, [("First", "translated text")])


if __name__ == "__main__":
    unittest.main()
