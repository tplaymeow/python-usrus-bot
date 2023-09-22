import json
import subprocess

from vosk import KaldiRecognizer, Model


class STT:
    def __init__(self) -> None:
        self.model = Model("./stt/models/vosk/model")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetWords(True)

    def run(self, file_path: str) -> str:
        with subprocess.Popen([
            "ffmpeg",
            "-loglevel", "quiet",
            "-i", file_path,
            "-ar", "16000",
            "-ac", "1",
            "-f", "s16le",
            "-"
        ], stdout=subprocess.PIPE) as process:
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                self.recognizer.AcceptWaveform(data)

        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)
        return result_dict["text"]
