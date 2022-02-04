import sys
import json

args = sys.argv
locale = args[1]

if locale == 'EN':
    path1 = './pageEx_info_en.json'
    path2 = './command_info_en.txt'
elif locale == 'JA':
    path1 = './pageEx_info_ja.json'
    path2 = './command_info_ja.txt'
with open(path1, 'r', encoding='utf-8') as f1:
    apps = json.load(f1)

f2 = open(path2, 'w', encoding='utf-8')

for k in apps:
    app = apps[k]
    command = app['Commands'][0]
    f2.write(command + '\n')

f2.close()