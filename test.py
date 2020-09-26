# -*- coding: utf-8 -*- 
import audio_preprocess
import audio_record

# for j in range(2):
#     audio_record.record(j)
#     audio_preprocess.audio_preprocessing()

while True:
    for j in range(5):
        audio_preprocess.audio_preprocessing(audio_record.record(j),j)
