import deepl
import os
import sys

from authkey import auth_key


# translate srt file
def translate_srt(input_file,
                  output_file,
                  *,
                  source_lang='EN',
                  target_lang='ZH'):
    translator = deepl.Translator(auth_key)
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    i = 1
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            try:
                index = int(line)
            except:
                index = -1
            if (index == i):
                i += 1
                j = 0
            j += 1
            if (j == 3):
                f.write(
                    translator.translate_text(line.strip("\n"),
                                              source_lang=source_lang,
                                              target_lang=target_lang).text +
                    "\n")
                # f.write("trans:" + line.strip("\n") + "\n")
            else:
                f.write(line)


def translate(inputs, lang_from, lang_to):
    for input in inputs:
        print("Translating", input)
        name, _ = os.path.splitext(input)
        translate_srt(input,
                      name + f".{lang_to}.srt",
                      source_lang=lang_from,
                      target_lang=lang_to)


def translate_directory(directory, lang_from, lang_to):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            print("Translating", filename)
            translate_srt(directory + "/" + filename,
                          directory + "/" + filename[:-4] + f".{lang_to}.srt",
                          source_lang=lang_from,
                          target_lang=lang_to)
        else:
            continue


if __name__ == "__main__":
    print("Usage: python3 transcribe.py <input> <lang from> <lang to>")
    if len(sys.argv) - 1 != 0:
        input = sys.argv[1]
        lang_from = sys.argv[2]
        lang_to = sys.argv[3]
    else:
        input = "input"
        lang_from = "EN"
        lang_to = "ZH"
    translate_directory(input, lang_from, lang_to)