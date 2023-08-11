# use librosa to slice wav file into VAD segments
# usage: python3 slice.py <directory> <output directory>
# output: npy file in the output directory

import os
import sys
import librosa
import numpy as np
import soundfile as sf

ONE_OVER_GAP = 10  # 1/ONE_OVER_GAP of a second

MERGE_GAP_THRESHOLD = 1
LENGTH_THRESHOLD = 10
TOP_DB = 30


def merge_intervals(intervals, sr):
    merged_intervals = []
    for interval in intervals:
        if len(merged_intervals) == 0:
            merged_intervals.append(interval)
        else:
            if interval[1] - merged_intervals[-1][
                    0] < sr * LENGTH_THRESHOLD and interval[
                        0] - merged_intervals[-1][1] < sr * MERGE_GAP_THRESHOLD:
                merged_intervals[-1][1] = interval[1]
            else:
                merged_intervals.append(interval)
    for interval in merged_intervals:
        interval[0] = max(interval[0] - sr // ONE_OVER_GAP * 2, 0)
    merged_intervals = np.array(merged_intervals)
    return merged_intervals


def slicing(y, sr, ONE_OVER_GAP):
    intervals = librosa.effects.split(y,
                                      top_db=TOP_DB,
                                      frame_length=sr // ONE_OVER_GAP,
                                      hop_length=sr // (ONE_OVER_GAP * 2))
    print(np.array(intervals).shape)
    intervals = merge_intervals(intervals, sr)
    print(np.array(intervals).shape)
    return intervals


def slicing_directory(directory, output_directory, ONE_OVER_GAP):
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            print("slicing " + filename)
            y, sr = librosa.load(directory + "/" + filename, sr=None)
            intervals = slicing(y, sr, ONE_OVER_GAP)
            np.save(output_directory + "/" + filename[:-4] + ".npy", intervals)
            # for sliced in intervals:
            #     sliced_filename = filename[:-4] + "_" + str(
            #         sliced[0]) + "_" + str(sliced[1]) + ".wav"
            #     sf.write(output_directory + "/" + sliced_filename,
            #              y[sliced[0]:sliced[1]], sr)
        else:
            continue


if __name__ == "__main__":

    print("Usage: python3 slice.py <directory> <output directory>")

    if len(sys.argv) - 1 == 0:
        directory = "input"
        output_directory = "output"
    else:
        directory = sys.argv[1]
        output_directory = sys.argv[2]

    slicing_directory(directory, output_directory, ONE_OVER_GAP)