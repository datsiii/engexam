import json
from vosk import Model, KaldiRecognizer


class Recognizer:
    def __init__(self, frame_rate=16000):
        model = Model("model")
        self.rec = KaldiRecognizer(model, frame_rate)
        self.rec.SetWords(True)

    def _get_result(self):
        """
        Используется для получения распознанных слов после обнраружения паузы в разговоре

        :return:
        """
        res = self.rec.Result()
        return json.loads(res)

    def _get_final_result(self):
        """
        Используется для получения распознанных слов после достижения конца аудио-файла
        :return:
        """
        res = self.rec.FinalResult()
        return json.loads(res)

    def recognize(self, wf):
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                result = self._get_final_result()
                if result.get("text"):
                    print('final result:', result["text"])
                    results.append(result)
                break
            if self.rec.AcceptWaveform(data):
                result = self._get_result()
                if result.get("text"):
                    print('result:', result["text"])
                    results.append(result)
            else:
                # print('partial result', self.rec.PartialResult())
                pass

        return results


recognizer = Recognizer()
