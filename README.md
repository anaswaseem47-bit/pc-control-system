from __future__ import annotations

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None


class VoiceAssistant:
    def __init__(self) -> None:
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 is not installed")
        if sr is None:
            raise RuntimeError("speech_recognition is not installed")

        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine.setProperty("rate", 180)

    def speak(self, text: str) -> None:
        if text and self.engine is not None:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen_for_command(self) -> str:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

        try:
            return self.recognizer.recognize_google(audio).lower()
        except Exception:
            return ""


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.speak("Voice assistant is ready.")
