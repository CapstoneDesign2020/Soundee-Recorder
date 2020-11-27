#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import audio_preprocess
import audio_record

import configparser
from config import request_source
config = configparser.ConfigParser()
config.read('./config/settings.conf')

from pyfiglet import Figlet

import requests
import getpass

from time import gmtime, strftime

## for S3
import boto3
import os
BASE_DIR = os.getcwd()
IMAGE_DIR = os.path.join(BASE_DIR, 'model_image')
AWS_ACCESS_KEY_ID = config['AWS_ACCESS']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = config['AWS_ACCESS']['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = config['AWS_ACCESS']['AWS_DEFAULT_REGION']
AWS_BUCKET_NAME = config['AWS_ACCESS']['AWS_BUCKET_NAME']

######
## for request
import requests

########
## for insert DB
import pymysql.cursors
# connection 정보
conn = pymysql.connect(
    host = config['DB']['HOST'],
    user = config['DB']['USER'],
    password = config['DB']['PASSWORD'],
    db = config['DB']['DB'],
    charset = config['DB']['CHARSET']
)


url = request_source.URL
payload = request_source.PAYLOAD
headers = request_source.HEADER

######
client = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION
                      )
s3 = boto3.resource('s3')

buckets = s3.Bucket(name=AWS_BUCKET_NAME)
file_path = os.path.join(IMAGE_DIR, 'test.png')
# 저장될 데이터의 이름 -> key로 사용
key_name = "test.png"


userIdx = 0

def LOGIN():
    global userIdx
    email = input("◻︎ Enter Your email : ")
    password = getpass.getpass("◻︎ Enter Your password : ")
    data = {'email':email, 'password':password}
    result = requests.post("http://13.125.146.172/user/signin",data=data)
    if result.status_code == 200:
        userIdx = result.json()["data"]["userIdx"] # userIdx
        print("\033[1m"+"\033[32m"+"✦ ✧ Login Success-! ✧ ✦"+"\033[0m")
        return
    else:
        print("\033[1m"+"\033[31m"+"Login failed... Please check email or password"+"\033[0m")
        LOGIN()
    


if __name__ == "__main__":
    f = Figlet(font='small')
    print(f.renderText('------------------'))
    print(f.renderText('           Hello-!  This is '))
    print(f.renderText('               * Soundee *\n                * Recorder *'))
    print(f.renderText('------------------'))
    LOGIN()
    while True:
        audio_preprocess.audio_preprocessing(audio_record.record("test"),"test")
        # upload_file(image파일 주소, 저장될 파일 이름)
        # buckets.upload_file(file_path, 'mcpro.png')
        # temp = getpass.getpass(" ")
        with open(file_path, 'rb') as data:
            buckets.upload_file(data.name, key_name)
        
        # request
        response = requests.request("POST", url, headers=headers, data = payload)

        current_sound_class = response.text
        if current_sound_class == 'no_class':
            print("Not in class.")
        print("This is",current_sound_class,"sound~!")
        # insert DB
        curs = conn.cursor()
        sql = f"insert into sound(class,eventdate,sound_userIdx) values({current_sound_class},NOW(),{userIdx});"
        curs.execute(sql)
        conn.commit()
