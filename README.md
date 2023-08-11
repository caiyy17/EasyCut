# EasyCut

这是一个 autocut 的简化版项目，可以完全在 cuda 上运行，一共包括：

1. 将 MP3 转成 WAV
2. 使用 librosa 提取说话部分（VAD）
3. 使用 whisper 转换成 srt
4. 使用 deepl 翻译为目标语言

请将 deepl 的 authkey 存在 authkey.py 中

# autocut

[autocut](https://github.com/mli/autocut)
