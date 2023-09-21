import json
import os
import subprocess

from vosk import KaldiRecognizer, Model


class STT:
    default_init = {
        "model_path": "/Users/mov4d/Desktop/python-usrus-bot/python_usrus_bot/stt/models/vosk/big_model",
        "sample_rate": 16000,
        "ffmpeg_path": "/Users/mov4d/Desktop/python-usrus-bot/python_usrus_bot/stt/models/vosk/ffmpeg"
    }

    def __init__(
            self,
            model_path=None,
            sample_rate=None,
            ffmpeg_path=None
    ) -> None:
        """
        :arg model_path:  str  путь до модели Vosk
        :arg sample_rate: int  частота выборки, обычно 16000
        :arg ffmpeg_path: str  путь к ffmpeg
        """
        self.model_path = model_path if model_path else STT.default_init["model_path"]
        self.sample_rate = sample_rate if sample_rate else STT.default_init["sample_rate"]
        self.ffmpeg_path = ffmpeg_path if ffmpeg_path else STT.default_init["ffmpeg_path"]

        # self._check_model()

        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)

    def _check_model(self):
        if not os.path.exists(self.model_path):
            raise Exception(
                "Vosk: сохраните папку model в папку vosk\n"
                "Скачайте модель по ссылке https://alphacephei.com/vosk/models"
            )

        isffmpeg_here = False
        for file in os.listdir(self.ffmpeg_path):
            if file.startswith('ffmpeg'):
                isffmpeg_here = True

        if not isffmpeg_here:
            raise Exception(
                "Ffmpeg: сохраните ffmpeg.exe в папку ffmpeg\n"
                "Скачайте ffmpeg.exe по ссылке https://ffmpeg.org/download.html"
            )
        self.ffmpeg_path = self.ffmpeg_path + '/ffmpeg'

    def audio_to_text(self, audio_file_name=None) -> str:
        if audio_file_name is None:
            raise Exception("Укажите путь и имя файла")
        if not os.path.exists(audio_file_name):
            raise Exception("Укажите правильный путь и имя файла")

        # Конвертация аудио в wav и результат в process.stdout
        process = subprocess.Popen(
            [self.ffmpeg_path,
             "-loglevel", "quiet",
             "-i", audio_file_name,  # имя входного файла
             "-ar", str(self.sample_rate),  # частота выборки
             "-ac", "1",  # кол-во каналов
             "-f", "s16le",  # кодек для перекодирования, у нас wav
             "-"  # имя выходного файла нет, тк читаем из stdout
             ],
            stdout=subprocess.PIPE
        )

        # Чтение данных кусками и распознование через модель
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass

        # Возвращаем распознанный текст в виде str
        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)
        return result_dict["text"]
