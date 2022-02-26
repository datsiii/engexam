from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("voice.webm")
sound.export("voice.wav", format="wav", codec="pcm_s16le", parameters=["-ar", "16000"])
