from core.translator import TranslatorService


translator = TranslatorService()


question = "रिट्रीवल ऑगमेंटेड जनरेशन क्या है?"


language = translator.detect_language(
    question
)

translated_question = translator.translate_to_english(
    question
)


print("\nDETECTED LANGUAGE:\n")

print(language)


print("\nTRANSLATED QUESTION:\n")

print(translated_question)