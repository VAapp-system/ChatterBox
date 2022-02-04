import sys
import json

args = sys.argv
locale = args[1]

if locale == 'EN':
    path1 = './pageEx_info_en.json'
    path2 = './description_info_en.json'
elif locale == 'JA':
    path1 = './pageEx_info_ja.json'
    path2 = './description_info_ja.json'


with open(path1, 'r', encoding='utf-8') as f1:
    apps = json.load(f1)
f2 = open(path2, 'w', encoding='utf-8')

dic = {}

number = 1
for k in apps:
    app = apps[k]
    descript = app['Description']
    des_n = len(descript)
    start_1 = -1
    end_1 = -1
    start_2 = -1
    end_2 = -1
    example_req = {}
    for index in range(des_n):
        if locale == 'EN':
            if descript[index] == '\'':
                if start_1 == -1:
                    start_1 = index + 1
                else:
                    end_1 = index
                    temp_str = descript[start_1:end_1]
                    example_req[temp_str] = True
                    start_1 = -1
                    end_1 = -1
            if descript[index] == '"':
                if start_2 == -1:
                    start_2 = index + 1
                else:
                    end_2 = index
                    temp_str = descript[start_2:end_2]
                    example_req[temp_str] = True
                    start_2 = -1
                    end_2 = -1
        elif locale == 'JA':
            if descript[index] == '「':
                start_1 = index + 1
            elif descript[index] == '」':
                end_1 = index
                if start_1 != -1:
                    temp_str = descript[start_1:end_1]
                    example_req[temp_str] = True
                start_1 = -1
                end_1 = -1
            if descript[index] == '『':
                start_2 = index + 1
            elif descript[index] == '』':
                end_2 = index
                if start_2 != -1:
                    temp_str = descript[start_2:end_2]
                    example_req[temp_str] = True
                
                start_2 = -1
                end_2 = -1
    dic[str(number)] = example_req
    number += 1

json.dump(dic, f2, indent=4, ensure_ascii=False)
f2.close()
