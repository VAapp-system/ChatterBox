import os
import sys
import json

args = sys.argv
locale = args[1]

if locale == 'EN':
    path1 = "./page_info_en.json"
    dir_path = './setup/category_groupEN'
    if not(os.path.exists(dir_path)):
        os.mkdir(dir_path)
elif locale == 'JA':
    path1 = "./page_info_ja.json"
    dir_path = './setup/category_groupJA'
    if not(os.path.exists(dir_path)):
        os.mkdir(dir_path)
    
with open(path1, 'r', encoding='utf-8') as f1:
    dic = json.load(f1)

category = {}
count = 0
cate_list = []
for k in dic:
    app = dic[k]
    if not(app['Name']):
        continue
    if not(app['Category'][0] in category):
        category[app['Category'][0]] = count
        cate_dic = {
            k: app
        }
        cate_list.append(cate_dic)
        count += 1
    else:
        number = category[app['Category'][0]]
        cate_dic = cate_list[number]
        cate_dic[k] = app

count = 1
for cate_dic in cate_list:
    path2 = dir_path + '/cate' + str(count) + '.json'
    with open(path2, 'w', encoding='utf-8') as f2:
        json.dump(cate_dic, f2, indent=4, ensure_ascii=False)
    count += 1
