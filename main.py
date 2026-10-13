
from translate import Translator

translator = Translator(from_lang="en", to_lang="hi")

print("🇮🇳 English to Hindi Translator")
print("Type 'exit' to quit.\n")

while True:
    english_text = input("Enter English text: ").strip()

    if english_text.lower() == "exit":
        print("Goodbye, bro!")
        break

    if not english_text:
        print("Please enter some text.")
        continue

    try:
        hindi_text = translator.translate(english_text)
        print("Hindi translation:", hindi_text)
        print("-" * 40)

    except Exception as e:
        print("Translation failed:", e)
