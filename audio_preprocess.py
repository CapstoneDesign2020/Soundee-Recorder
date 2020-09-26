import librosa
import librosa.display
# import IPython.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import glob
from IPython import get_ipython

from PIL import Image

import re



def audio_preprocessing(data,test):


    # folder_list = glob.glob("audio_data/*") # 오디오 데이터 파일 위치 
    # print(folder_list)
    # print(len(folder_list))
    # index=0
    # for i in folder_list:
    frame_length = 0.025
    frame_stride = 0.010
    y, sr = librosa.load(data,sr=16000)
    win_length = int(np.ceil(frame_length*sr))
    window = 'hamming'
    nfft = int(round(sr*frame_length))
    hop_length = int(round(sr*frame_stride))
    plt.figure(figsize=(4,10))
    Si = librosa.feature.melspectrogram(y=y,sr=sr,n_mels=40, n_fft=nfft, hop_length=hop_length,win_length=win_length, window=window,
                                        center=True, pad_mode='reflect', fmin=0.0)
    DB = librosa.amplitude_to_db(Si, ref=np.max)
    
    librosa.display.specshow(DB.T, sr=sr, x_axis='linear', y_axis='time',hop_length=hop_length)
    plt.axis('off')


    # plt.xlabel("Time")
    # plt.ylabel("MFCC coefficients")
    # plt.colorbar()
    # plt.title("MFCCs")
    
    #save image
    fig = plt.gcf() 
    img_path = "./model_image/"+test+'.png'
    fig.savefig(img_path,bbox_inches='tight',pad_inches=0)
    plt.close()
    
    # resize
    img_size = (256, 256)
    image = Image.open(f'{img_path}')
    image = image.resize(img_size)
    image.save(f'{img_path}')
    # index+=1
    print("complete!")    