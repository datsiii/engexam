import wave
import os
from pydub import AudioSegment
from datetime import datetime

AUDIO_DIR = 'uploads'


class AudioFormatException(Exception):
    pass


class Converter:

    @staticmethod
    def get_wav_filename():
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.wav")
        return os.path.join(AUDIO_DIR, filename)

    def convert_to_wav(self, stream):
        sound = AudioSegment.from_file(stream)
        filename = self.get_wav_filename()
        sound.export(filename, format="wav", codec="pcm_s16le", parameters=["-ar", "16000"])
        wf = wave.open(filename, "rb")
        print('framerate', wf.getframerate())
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise AudioFormatException("Audio file must be WAV format mono PCM.")

        return wf


converter = Converter()
