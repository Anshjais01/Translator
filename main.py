
# pyrefly: ignore [missing-import]
import sys
sys.stdout.reconfigure(encoding='utf-8')

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import ctypes
import tempfile
import os
from translate import Translator
from gtts import gTTS

# --- Setup ---
translator = Translator(from_lang="en", to_lang="hi")
recognizer = sr.Recognizer()

# Audio recording settings
SAMPLE_RATE = 16000  # Hz
RECORD_SECONDS = 5   # Default recording duration


def record_audio():
    """Record audio from microphone using sounddevice."""
    print("🎤 Listening... (speak now, recording for 5 seconds)")
    audio_data = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )
    sd.wait()  # Wait until recording is finished
    print("✅ Recording complete!")
    return audio_data


def speech_to_text(audio_data):
    """Convert recorded audio to text using Google Speech Recognition."""
    # Save to a temporary WAV file
    temp_file = os.path.join(tempfile.gettempdir(), "translator_input.wav")
    wav.write(temp_file, SAMPLE_RATE, audio_data)

    # Use SpeechRecognition to convert to text
    with sr.AudioFile(temp_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"❌ Speech Recognition service error: {e}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def play_mp3(file_path):
    """Play an MP3 file using Windows MCI (built-in, no extra packages needed)."""
    winmm = ctypes.windll.winmm
    # Use absolute path with forward slashes for MCI
    file_path = os.path.abspath(file_path).replace("\\", "/")
    winmm.mciSendStringW(f'open "{file_path}" type mpegvideo alias tts_audio', None, 0, 0)
    winmm.mciSendStringW('play tts_audio wait', None, 0, 0)
    winmm.mciSendStringW('close tts_audio', None, 0, 0)


def speak_hindi(text):
    """Speak Hindi text using Google TTS."""
    temp_file = os.path.join(tempfile.gettempdir(), "translator_output.mp3")
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save(temp_file)
        play_mp3(temp_file)
    except Exception as e:
        print(f"❌ TTS error: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


# --- Main Loop ---
print("🇮🇳 English to Hindi Translator (with Voice!)")
print("Commands:")
print("  Type text   → translate typed English")
print("  Type 'v'    → speak in English (voice input)")
print("  Type 'exit' → quit\n")

while True:
    user_input = input("Enter text or 'v' for voice: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye, bro! 👋")
        break

    # --- Voice Input Mode ---
    if user_input.lower() == "v":
        audio_data = record_audio()
        english_text = speech_to_text(audio_data)

        if english_text is None:
            print("❌ Could not understand the audio. Please try again.")
            continue

        print(f"🗣️  You said: {english_text}")

    # --- Text Input Mode ---
    else:
        english_text = user_input

    if not english_text:
        print("Please enter some text.")
        continue

    try:
        hindi_text = translator.translate(english_text)
        print(f"📝 Hindi translation: {hindi_text}")

        # Speak the Hindi translation using Google TTS
        print("🔊 Speaking translation...")
        speak_hindi(hindi_text)

        print("-" * 40)

    except Exception as e:
        print("Translation failed:", e)
