import sys
import random
import json
from decimal import Decimal, ROUND_HALF_UP

args = sys.argv
locale = args[1]

sample_rate = 1.0 #edit

if locale == 'EN':
    dir_path = './setup/category_groupEN'
    path1 = './setup/pageTEMP_info_en.json'
elif locale == 'JA':
    dir_path = './setup/category_groupJA'
    path1 = './setup/pageTEMP_info_ja.json'

dic1 = {}
count = 1
for i in range(18):
    path3 = dir_path + '/cate' + str(i + 1) + '.json'
    with open(path3, 'r', encoding='utf-8') as f3:
        dic = json.load(f3)
        n = len(dic)
        limit = Decimal(str(n * sample_rate)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
        app_list = random.sample(list(dic.values()), int(limit))
        for app in app_list:
            dic1[str(count)] = app
            count += 1
            
with open(path1, 'w', encoding='utf-8') as f1:
    json.dump(dic1, f1, indent=4, ensure_ascii=False)