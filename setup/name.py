import sys
import json

args = sys.argv
locale = args[1]

if locale == 'EN':
    path1 = './pageEx_info_en.json'
    path2 = './name_info_en.txt'
elif locale == 'JA':
    path1 = './pageEx_info_ja.json'
    path2 = './name_info_ja.txt'
with open(path1, 'r', encoding='utf-8') as f1:
    apps_en = json.load(f1)
f2 = open(path2, 'w', encoding='utf-8')

for k in apps_en:
    app = apps_en[k]
    name = app['Name']
    f2.write(name + '\n')

f2.close()
