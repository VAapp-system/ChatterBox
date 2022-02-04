import sys
import json

args = sys.argv
locale = args[1]

if locale == 'EN':
    path1 = './setup/pageTEMP_info_en.json'
    path2 = './pageEx_info_en.json'
elif locale == 'JA':
    path1 = './setup/pageTEMP_info_ja.json'
    path2 = './pageEx_info_ja.json'
with open(path1, 'r', encoding='utf-8') as f1:
    apps = json.load(f1)

dic_en = {}

number = 1
for k in apps:
    app = apps[k]
    if not(app['Name']):
        continue
    if app['Developer'] == 'Google Inc.' or app['Developer'] == 'Google':
        continue
    if (locale == 'EN' and 'Smart home' in app['Category']) or (locale == 'JA' and 'スマートホーム' in app['Category']):
        continue
    try:
        command = app['Commands'][0]
        if not(command):
            continue
    except:
        continue
    dic_en[str(number)] = app
    number += 1

with open(path2, 'w', encoding='utf-8') as f2:
    json.dump(dic_en, f2, indent=4, ensure_ascii=False)