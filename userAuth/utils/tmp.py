# encoding: UTF-8 
import re

ro = {}

p_text = re.compile(r'text\': u\'(\S+)\'')
for i in p_text.findall(str(ro)):
    print i.decode('unicode_escape')

p_resourceid = re.compile(r'resource-id\': u\'(\S+)\'')
for i in p_resourceid.findall(str(ro)):
    print i
#
# #作者微信：2501902696
# from PIL import Image
# import pytesseract
# #上面都是导包，只需要下面这一行就能实现图片文字识别
# text=pytesseract.image_to_string(Image.open('denggao.jpeg'),lang='chi_sim')
# print(text)
#
# pip install PIL
# pip install pytesseract
# 安装识别引擎tesseract-ocr