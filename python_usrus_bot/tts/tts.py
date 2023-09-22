from gtts import gTTS


def text_to_speech(text: str, filename: str) -> None:
    tts = gTTS(text=text, lang='ru')
    tts.save(filename)
