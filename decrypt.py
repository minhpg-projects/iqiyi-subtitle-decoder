import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import requests
from fastapi import FastAPI, Response
import re
import pysrt
import time

LICENSE = "AHEACgMAAAAAAAAAAAQCcgACATADcwAnAgAg6TANATF98aZ4AuZilQqtL+g8UGctvypPVE2y56vnyZUCAAAAA3QANwEAMDEQk5CrOfOzGxt3Oxdg/PRTOTfYgT6v4nTR/7xT9pHee6wj3KcjbIl5J60qHoFiYAEAAgD/dQAkAQAAILnE6ZeOl1KdOg148RmZhiYR6+OdRrP/gvG2ARqY7dTf"
nodejs_instance = os.popen('node libmonalisa-v3.0.6-python '+LICENSE)
DEVICE_KEY = nodejs_instance.read().strip()
nodejs_instance.close()


def decryptText(enc_text):
    print(enc_text)
    crypto = AES.new(key=bytes.fromhex(DEVICE_KEY), mode=AES.MODE_CBC, iv=bytes([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    raw_enc = base64.b64decode(enc_text.encode())
    decrypted = crypto.decrypt(raw_enc)
    return unpad(decrypted, AES.block_size).decode()

def decryptSubtitle(url):
    response = requests.get(url)
    filename = str(time.time())
    open(filename,'w').write(response.text)
    subs = pysrt.open(filename)
    for i,sub in enumerate(subs):
        subs[i].text = decryptText(sub.text)
    subs.save(filename, encoding='utf-8')
    return open(filename).read()
# decryptSubtitle('https://meta.video.iqiyi.com/20210227/07/92/afeb72e4b8a4542bc8f21b6965f4197d.srt?qd_sc=8acc1c9dcf4ac631aed1894cb0572936&qd_uid=30101840175&qd_vip=1&qd_src=01010031010021000000&qd_tm=1628603026236&qd_p=3b99fe36&qd_k=&qd_index=0&qd_tvid=3696881580114300')


app = FastAPI()

@app.get('/subtitle.srt')
async def main(url: str):
    return Response(content=decryptSubtitle(url), media_type="text/plain")