import easyocr
from googletrans import Translator
import os

# List of language codes (ISO 639-1)
language_codes = {
    "af": "Afrikaans", "sq": "Albanian", "ar": "Arabic", "hy": "Armenian", "bn": "Bengali", 
    "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan", "hr": "Croatian", "cs": "Czech", 
    "da": "Danish", "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian", 
    "tl": "Filipino", "fi": "Finnish", "fr": "French", "de": "German", "el": "Greek", 
    "gu": "Gujarati", "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian", "it": "Italian", 
    "ja": "Japanese", "jw": "Javanese", "km": "Khmer", "ko": "Korean", "la": "Latin", 
    "lv": "Latvian", "lt": "Lithuanian", "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali", 
    "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian", "ru": "Russian", 
    "sr": "Serbian", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "es": "Spanish", 
    "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "ta": "Tamil", "te": "Telugu", 
    "th": "Thai", "tr": "Turkish", "uk": "Ukrainian", "vi": "Vietnamese", "cy": "Welsh", 
    "zu": "Zulu"
}

def image_to_text_translator(image_path):
    """
    Extracts text from an image and translates it to the specified target language.
    
    Args:
        image_path: Path to the image file.
    
    Returns:
        Translated text.
    """
    # Check if the image path exists
    if not os.path.exists(image_path):
        return "Error: Image file not found."

    try:
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=False)  # English for testing
        result = reader.readtext(image_path)

        # Check if result is empty
        if result is None or len(result) == 0:
            return "Error: No text detected in the image. Please check the image quality."
        
        # Extract text from result
        text = " ".join([item[1] for item in result])
        
        if not text.strip():
            return "Error: No readable text found in the image."

        # Detect the language of the text using googletrans
        translator = Translator()
        detected_language = translator.detect(text).lang  # Detect source language

        print(f"\nDetected language: {language_codes.get(detected_language, 'Unknown')}")

        # Provide the user with available languages to translate to
        print("\nAvailable target languages:")
        for code, language in language_codes.items():
            print(f"{code}: {language}")

        # Get user input for target language
        target_language = input("\nEnter the target language code (e.g., 'fr' for French, 'de' for German): ")

        # Validate the input
        if target_language not in language_codes:
            return f"Invalid target language code. Please choose from the following valid codes: {list(language_codes.keys())}"

        # Translate the extracted text using Google Translate
        translation = translator.translate(text, src=detected_language, dest=target_language)

        # Return the translated text
        return f"Detected language: {language_codes.get(detected_language, 'Unknown')}\nTranslated text: {translation.text}"

    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error: {str(e)}"


# Main loop to keep asking for images to translate
def main():
    while True:
        # Ask user for image path
        image_path = input("Enter the path to the image you want to translate (or 'exit' to quit): ")

        if image_path.lower() == 'exit':
            print("Exiting the program.")
            break

        # Call the function to extract and translate text
        translated_text = image_to_text_translator(image_path)
        print(translated_text)

        # Ask if the user wants to translate another image
        continue_choice = input("Do you want to translate another image? (yes/no): ").lower()
        if continue_choice != 'yes':
            print("Exiting the program.")
            break

# Run the main program
if __name__ == "__main__":
    main()
