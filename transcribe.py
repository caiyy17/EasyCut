# use whisper to transcribe wav files in a directory
# usage: python3 transcribe.py <directory> <output directory>
# output: srt files in the output directory

import datetime
import os
import time
import sys
import numpy as np

import srt
import whisper
import librosa


def process(whisper_model, audio, seg, lang, prompt):
    r = whisper_model.transcribe(
        audio[int(seg["start"]):int(seg["end"])],
        task="transcribe",
        language=lang,
        initial_prompt=prompt,
    )
    r["origin_timestamp"] = seg
    return r


class Transcribe:
    def __init__(self, lang, prompt, sampling_rate, whisper_model_name, device,
                 encoding):
        self.lang = lang  # choices=["JA", "EN", "ZH"],
        self.prompt = prompt
        self.sampling_rate = sampling_rate
        self.device = device
        self.whisper_model_name = whisper_model_name
        self.encoding = encoding
        self.whisper_model = None

    def run(self, input, npy, output):
        if os.path.isdir(input):
            for filename in os.listdir(input):
                if filename.endswith(".wav"):
                    print("transcribing " + filename)
                    self._transcribe_file(
                        os.path.join(input, filename),
                        os.path.join(npy, filename[:-4] + ".npy"),
                        os.path.join(output, filename[:-4] + ".srt"))
                else:
                    continue
        else:
            self._transcribe_file(input, npy, output)

    def _transcribe_file(self, input, npy, output):
        speech_timestamps = np.load(npy)
        audio, sr = librosa.load(input, sr=None)
        self.sampling_rate = sr
        # print("sampling rate: " + str(sr))
        # print("speech timestamps: " + str(speech_timestamps.shape))
        audio = whisper.load_audio(input, sr=self.sampling_rate)
        transcribe_results = self._transcribe(audio, speech_timestamps)
        self._save_srt(output, transcribe_results)

    def _transcribe(self, audio, speech_timestamps):
        tic = time.time()
        if self.whisper_model is None:
            self.whisper_model = whisper.load_model(self.whisper_model_name,
                                                    self.device)

        res = []
        for seg in speech_timestamps:
            # print(seg)
            r = self.whisper_model.transcribe(
                audio[int(seg[0]):int(seg[1])],
                task="transcribe",
                language=self.lang,
                initial_prompt=self.prompt,
                verbose=False if len(speech_timestamps) == 1 else None,
            )
            r["origin_timestamp"] = seg
            res.append(r)
        print(f"Done transcription in {time.time() - tic:.1f} sec")
        return res

    def _save_srt(self, output, transcribe_results):
        subs = []

        def _add_sub(start, end, text):
            subs.append(
                srt.Subtitle(
                    index=0,
                    start=datetime.timedelta(seconds=start),
                    end=datetime.timedelta(seconds=end),
                    content=text.strip(),
                ))

        prev_end = 0
        for r in transcribe_results:
            origin = r["origin_timestamp"]
            for s in r["segments"]:
                start = s["start"] + origin[0] / self.sampling_rate
                end = min(
                    s["end"] + origin[0] / self.sampling_rate,
                    origin[1] / self.sampling_rate,
                )
                if start > end:
                    continue
                # mark any empty segment that is not very short
                if start > prev_end + 3.0:
                    _add_sub(prev_end, start, "< No Speech >")
                _add_sub(start, end, s["text"])
                prev_end = end

        with open(output, "wb") as f:
            f.write(srt.compose(subs).encode(self.encoding, "replace"))


if __name__ == "__main__":
    print(
        "Usage: python3 transcribe.py <lang> <model> <device> <input> <npy> <output>"
    )

    if len(sys.argv) - 1 != 0:
        lang = sys.argv[1]
        model = sys.argv[2]
        device = sys.argv[3]
        input = sys.argv[4]
        npy = sys.argv[5]
        output = sys.argv[6]
    else:
        lang = "EN"
        model = "large-v2"
        device = "cuda"
        input = "input"
        npy = "output"
        output = "output"
    Transcribe(lang=lang,
               prompt="",
               sampling_rate=None,
               whisper_model_name=model,
               device=device,
               encoding="utf-8").run(input, npy, output)
