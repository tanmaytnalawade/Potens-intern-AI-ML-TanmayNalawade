from deep_translator import GoogleTranslator
from langdetect import detect


class TranslatorService:

    def detect_language(
        self,
        text
    ):

        try:

            language = detect(text)

            return language

        except:

            return "en"

    def translate_to_english(
        self,
        text
    ):

        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        return translated

    def translate_from_english(
        self,
        text,
        target_language
    ):

        translated = GoogleTranslator(
            source="en",
            target=target_language
        ).translate(text)

        return translated