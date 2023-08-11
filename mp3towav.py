# use ffmpeg to convert mp3 to wav in a directory with sample rate 40k
# usage: python3 mp3towav.py <directory>
# output: wav files in the same directory

import os
import sys


def convert_mp3_to_wav(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            print("converting " + filename)
            # print("ffmpeg -i " + "\"" + directory + "/" + filename + "\" \"" +
            #       directory + "/" + filename[:-4] + ".wav"
            #       "\"" + "\n")
            os.system("ffmpeg -i " + "\"" + directory + "/" + filename +
                      "\" -ar 16000 \"" + directory + "/" + filename[:-4] +
                      ".wav"
                      "\"" + " -y")
        else:
            continue


if __name__ == "__main__":

    print("Usage: python3 mp3towav.py <directory>")

    if len(sys.argv) - 1 == 0:
        directory = "input"
    else:
        directory = sys.argv[1]

    convert_mp3_to_wav(directory)
