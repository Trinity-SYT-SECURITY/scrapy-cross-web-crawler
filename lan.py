import os
import sys
#from easynmt import EasyNMT
from google_trans_new import google_translator
# 建立翻譯物件
nmt = google_translator()

import time
path = '/home/kali/Desktop/test2/test2/spiders/CVE-2/'
def read_text(file_path):

    with open(file_path, encoding="utf-8") as file:
        text = file.read()
    return text

to_lang = "zh-TW"
# 如果不存在目標文件夾，則創建目標文件夾
target_dir = os.path.join(path, to_lang)
if not os.path.exists(target_dir):
    os.makedirs(target_dir)



# 遍歷所有文件
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    if os.path.isfile(file_path):
        print('正在翻譯文件：', file_path)
        # 讀取文件內容
        text = read_text(file_path)
        # 翻譯文件內容
        time.sleep(10)
        result = nmt.translate(text,lang_tgt="zh-TW")
        
        # 將翻譯結果保存到目標文件夾中
        target_file_path = os.path.join(target_dir, filename)
        with open(target_file_path, 'w', encoding='utf-8') as target_file:
            target_file.write(result)
        print('已經將翻譯結果保存到：', target_file_path)
