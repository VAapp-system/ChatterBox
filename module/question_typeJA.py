import questionJA

left_list = ['「', '『', '`']
right_list = ['」', '』', '」']
cite_list = ['・', '[1]']
delete_list = ['。', '(', ')', '《', '》', '【', '】']
example_parse = [
    [
        "形副名詞",
        "時間",
        "外の関係",
        "ハ",
        "助詞",
        "体言",
        "係:未格",
        "提題"
    ],
    [
        "形副名詞",
        "外の関係",
        "ハ",
        "助詞",
        "体言",
        "修飾",
        "係:未格",
        "提題"
    ],
    [
        "形副名詞",
        "外の関係",
        "ニ",
        "ハ",
        "ニハ",
        "助詞",
        "体言",
        "修飾",
        "係:ニ格"
    ],
    [
        "形副名詞",
        "外の関係",
        "体言",
        "係:連用",
        "修飾"
    ],
    [
        "形副名詞",
        "時間",
        "外の関係",
        "体言",
        "係:連用",
        "修飾"
    ],
    [
        "形副名詞",
        "外の関係",
        "ハ",
        "助詞",
        "体言",
        "一文字漢字",
        "係:未格",
        "提題"
    ],
    [
        "カラ",
        "ハ",
        "助詞",
        "体言",
        "係:カラ格",
        "並列タイプ:OTHER"
    ],
    [
        "正規化代表表記:例えば/たとえば"
    ],
    [
        "ID:～ば"
    ],
    [
        "ID:～なら"
    ],
    [
        "ID:～たら"
    ],
    [
        "ID:～ので"
    ],
    [
        "ID:～には"
    ]
]

def Meishi(bnst, midasi):
    flag4 = False
    temp_kuten = None
    for mrph in reversed(bnst.mrph_list()):
        if temp_kuten and mrph.bunrui != '数詞':
            flag4 = True
            break
        if mrph.bunrui == '数詞':
            if temp_kuten:
                midasi = mrph.midasi + temp_kuten + midasi
                temp_kuten = None
            else:
                midasi = mrph.midasi + midasi
        elif mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
            midasi = mrph.midasi + midasi
        elif mrph.bunrui == '句点':
            temp_kuten = mrph.midasi
        else:
            flag4 = True
            break
    return flag4, midasi

def NEextract(bnst_dic, NE_list):
    NE_extract = {}
    for q_dic in NE_list:
        type_id = q_dic['type']
        index_list = q_dic['index']
        n = len(index_list)
        temp = []
        if type_id == 1 or type_id == 2 or type_id == 3 or type_id == 9:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    temp = []
                    break
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''

        elif type_id == 5 or type_id == 21:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[2]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    temp = []
                    break
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''

        elif type_id == 10 or type_id == 50:
            midasi = ''
            for i in range(int(index_list[0]), int(index_list[n - 1]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    temp = []
                    break
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
        
        elif type_id == 4 or type_id == 6 or type_id == 7 or type_id == 11 or type_id == 12 or type_id == 13 or type_id == 14 or type_id == 16 or type_id == 17 or type_id == 18 or type_id == 46 or type_id == 51 or type_id == 54:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break

            if flag1:
                if type_id == 11 or type_id == 12 or type_id == 16 or type_id == 46:
                    feature = bnst_dic[index_list[0]]['feature']
                    b = '|'.join(feature)
                    if 'カウンタ:' in b:
                        midasi = ''
                        j = int(index_list[0]) - 1
                        while 1 <= j:
                            bnst = bnst_dic[str(j)]['bnst']
                            if not(bnst):
                                break
                            flag4, midasi = Meishi(bnst, midasi)
                            if flag4:
                                break             
                            j -= 1
                        midasi += bnst_dic[index_list[0]]['midasi']
                        temp.append(midasi)
                else:
                    midasi = ''
                    j = int(index_list[0]) - 1
                    while 1 <= j:
                        bnst = bnst_dic[str(j)]['bnst']
                        if not(bnst):
                            break
                        flag4, midasi = Meishi(bnst, midasi)
                        if flag4:
                            break             
                        j -= 1
                    midasi += bnst_dic[index_list[0]]['midasi']
                    temp.append(midasi)

        elif type_id == 15 or type_id == 19 or type_id == 52:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[1]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[1]]['midasi']
                temp.append(midasi)
        
        elif type_id == 25 or type_id == 26:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break

            if flag1:
                midasi = ''
                j = int(index_list[2]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[2]]['midasi']
                temp.append(midasi)

        elif type_id == 8 or type_id == 23:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break

            if flag1:
                if type_id == 8:
                    feature = bnst_dic[index_list[2]]['feature']
                    b = '|'.join(feature)
                    if 'カウンタ:' not in b:
                        midasi = ''
                        j = int(index_list[0]) - 1
                        while 1 <= j:
                            bnst = bnst_dic[str(j)]['bnst']
                            if not(bnst):
                                break
                            flag4, midasi = Meishi(bnst, midasi)
                            if flag4:
                                break             
                            j -= 1
                        midasi += bnst_dic[index_list[0]]['midasi']
                        temp.append(midasi)

                        midasi = ''
                        j = int(index_list[1]) - 1
                        while 1 <= j:
                            bnst = bnst_dic[str(j)]['bnst']
                            if not(bnst):
                                break
                            flag4, midasi = Meishi(bnst, midasi)
                            if flag4:
                                break             
                            j -= 1
                        midasi += bnst_dic[index_list[1]]['midasi']
                        temp.append(midasi)
                else:
                    midasi = ''
                    j = int(index_list[0]) - 1
                    while 1 <= j:
                        bnst = bnst_dic[str(j)]['bnst']
                        if not(bnst):
                            break
                        flag4, midasi = Meishi(bnst, midasi)
                        if flag4:
                            break             
                        j -= 1
                    midasi += bnst_dic[index_list[0]]['midasi']
                    temp.append(midasi)

                    midasi = ''
                    j = int(index_list[1]) - 1
                    while 1 <= j:
                        bnst = bnst_dic[str(j)]['bnst']
                        if not(bnst):
                            break
                        flag4, midasi = Meishi(bnst, midasi)
                        if flag4:
                            break             
                        j -= 1
                    midasi += bnst_dic[index_list[1]]['midasi']
                    temp.append(midasi)
        
        elif type_id == 21 or type_id == 22 or type_id == 24 or type_id == 53:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
                
            if flag1:
                midasi = ''
                j = int(index_list[1]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[1]]['midasi']
                temp.append(midasi)

                midasi = ''
                j = int(index_list[2]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[2]]['midasi']
                temp.append(midasi)

        elif type_id == 27 or type_id == 35 or type_id == 37 or type_id == 39 or type_id == 41 or type_id == 42 or type_id == 45:
            start = 1
            for start in reversed(range(1, int(index_list[0]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[0]) + 1):
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if type_id == 35:
                if 1 < len(temp):
                    temp = temp[-1:]
            if type_id == 27 or type_id == 39 or type_id == 45:
                if 2 < len(temp):
                    temp = temp[-2:]
        elif type_id == 47:
            start = 1
            for start in reversed(range(1, int(index_list[1]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[1]) + 1):
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if type_id == 47:
                if len(temp) < 2:
                    temp = []

        elif type_id == 34 or type_id == 43:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    temp = []
                    break
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.hinsi == '名詞' or mrph.bunrui == '名詞形態指示詞' or mrph.bunrui == '名詞接頭辞' or mrph.bunrui == 'イ形容詞接頭辞' or mrph.bunrui == 'ナ形容詞接頭辞' or mrph.bunrui == '名詞性名詞接尾辞' or mrph.bunrui == '名詞性述語接尾辞' or mrph.bunrui == '名詞性名詞助数辞' or mrph.bunrui == '名詞性特殊接尾辞' or mrph.bunrui == '記号':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
        
        elif type_id == 44:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[0]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[0]]['midasi']
                temp.append(midasi)

        elif type_id == 33:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[2]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[2]]['midasi']
                temp.append(midasi)

        elif type_id == 28 or type_id == 29 or type_id == 30 or type_id == 31 or type_id == 32 or type_id == 36 or type_id == 40:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[0]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[0]]['midasi']
                temp.append(midasi)

                midasi = ''
                j = int(index_list[1]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[1]]['midasi']
                temp.append(midasi)

        elif type_id == 38:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[0]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[0]]['midasi']
                midasi = midasi[:-2]
                temp.append(midasi)

                midasi = ''
                j = int(index_list[1]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[1]]['midasi']
                midasi = midasi[:-1]
                temp.append(midasi)

                midasi = ''
                j = int(index_list[2]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[2]]['midasi']
                temp.append(midasi)

        elif type_id == 48:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                j = int(index_list[0]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[0]]['midasi']
                midasi = midasi[:-2]
                temp.append(midasi)

                midasi = ''
                j = int(index_list[1]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[1]]['midasi']
                midasi = midasi[:-2]
                temp.append(midasi)

                midasi = ''
                j = int(index_list[3]) - 1
                while 1 <= j:
                    bnst = bnst_dic[str(j)]['bnst']
                    if not(bnst):
                        break
                    flag4, midasi = Meishi(bnst, midasi)
                    if flag4:
                        break             
                    j -= 1
                midasi += bnst_dic[index_list[3]]['midasi']
                midasi = midasi[:-1]
                temp.append(midasi)

        elif type_id == 49:
            midasi = ''
            j = int(index_list[1]) - 1
            while 1 <= j:
                bnst = bnst_dic[str(j)]['bnst']
                if not(bnst):
                    break
                flag4, midasi = Meishi(bnst, midasi)
                if flag4:
                    break             
                j -= 1
            midasi += bnst_dic[index_list[1]]['midasi']
            midasi = midasi[:-1]
            temp.append(midasi)

            midasi = ''
            j = int(index_list[3]) - 1
            while 1 <= j:
                bnst = bnst_dic[str(j)]['bnst']
                if not(bnst):
                    break
                flag4, midasi = Meishi(bnst, midasi)
                if flag4:
                    break             
                j -= 1
            midasi += bnst_dic[index_list[3]]['midasi']
            midasi = midasi[:-1]
            temp.append(midasi)

            midasi = ''
            j = int(index_list[4]) - 1
            while 1 <= j:
                bnst = bnst_dic[str(j)]['bnst']
                if not(bnst):
                    break
                flag4, midasi = Meishi(bnst, midasi)
                if flag4:
                    break             
                j -= 1
            midasi += bnst_dic[index_list[4]]['midasi']
            midasi = midasi[:-1]
            temp.append(midasi)

        if temp:
            if str(type_id) in NE_extract:
                NE_extract[str(type_id)] += temp
            else:
                NE_extract[str(type_id)] = temp
            NE_extract[str(type_id)] = list(dict.fromkeys(NE_extract[str(type_id)]))

    return NE_extract

def INSTextract(bnst_dic, INST_list):
    INST_extract = {}
    for q_dic in INST_list:
        type_id = q_dic['type']
        index_list = q_dic['index']
        n = len(index_list)
        temp = []

        if (1 <= type_id and type_id <= 23) or (25 <= type_id and type_id <= 36):
            start = 1
            for start in reversed(range(1, int(index_list[0]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
            midasi = ''
            kakko_flag = False
            sento_joshi_flag = False
            for i in range(start + 1, int(index_list[0]) + 1):
                bnst = bnst_dic[str(i)]['bnst']
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    midasi = ''
                    kakko_flag = False
                    sento_joshi_flag = False
                    continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and mrph.bunrui != '括弧始' and mrph.bunrui != '括弧終' and (mrph.midasi != 'など' or mrph.hinsi != '助詞' or mrph.bunrui != '副助詞') and ((mrph.midasi != 'や' and mrph.midasi != 'か') or mrph.hinsi != '助詞' or mrph.bunrui != '接続助詞'):
                        if midasi == '' and mrph.hinsi =='助詞':
                            sento_joshi_flag = True
                        midasi += mrph.midasi
                        if mrph.hinsi == '助詞' and (mrph.midasi != 'と' and mrph.midasi != 'を') and (mrph.bunrui == '格助詞' or mrph.bunrui == '副助詞'):
                            joshi_flag = True
                            kaku_joshi_flag = False
                        elif mrph.hinsi == '助詞' and (mrph.midasi == 'と' or mrph.midasi == 'を') and mrph.bunrui == '格助詞':
                            joshi_flag = False
                            kaku_joshi_flag = True
                        else:
                            joshi_flag = False
                            kaku_joshi_flag = False
                    else:
                        if mrph.bunrui == '括弧終':
                            kakko_flag = False
                        elif mrph.bunrui == '読点' and kakko_flag:
                            midasi += mrph.midasi
                            joshi_flag = False
                            kaku_joshi_flag = False
                            continue
                        elif mrph.bunrui == '括弧始':
                            kakko_flag = True
                        if midasi != '':
                            if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                                if not(joshi_flag) and not(sento_joshi_flag):
                                    if kaku_joshi_flag:
                                        midasi = midasi[:-1]
                                    temp.append(midasi)
                            sento_joshi_flag = False
                            midasi = ''
            if midasi != '':
                if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                    if (1 <= type_id and type_id <= 13) or type_id == 20 or type_id == 23 or type_id == 27 or type_id == 36:
                        midasi = midasi[:-1]
                    if midasi != '':
                        if not(sento_joshi_flag):
                            temp.append(midasi)

        if type_id == 24:
            flag1 = True
            for i in range(int(index_list[0]) + 1, int(index_list[n - 1])):
                flag2 = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag2 = True
                        break
                if flag2:
                    flag1 = False
                    break
            if flag1:
                midasi = ''
                kakko_flag = False
                sento_joshi_flag = False
                bnst = bnst_dic[index_list[0]]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and mrph.bunrui != '括弧始' and mrph.bunrui != '括弧終' and (mrph.midasi != 'など' or mrph.hinsi != '助詞' or mrph.bunrui != '副助詞') and ((mrph.midasi != 'や' and mrph.midasi != 'か') or mrph.hinsi != '助詞' or mrph.bunrui != '接続助詞'):
                        if midasi == '' and mrph.hinsi =='助詞':
                            sento_joshi_flag = True
                        midasi += mrph.midasi
                        if mrph.hinsi == '助詞' and (mrph.midasi != 'と' and mrph.midasi != 'を') and (mrph.bunrui == '格助詞' or mrph.bunrui == '副助詞'):
                            joshi_flag = True
                            kaku_joshi_flag = False
                        elif mrph.hinsi == '助詞' and (mrph.midasi == 'と' or mrph.midasi == 'を') and mrph.bunrui == '格助詞':
                            joshi_flag = False
                            kaku_joshi_flag = True
                        else:
                            joshi_flag = False
                            kaku_joshi_flag = False
                    else:
                        if mrph.bunrui == '括弧終':
                            kakko_flag = False
                        elif mrph.bunrui == '読点' and kakko_flag:
                            midasi += mrph.midasi
                            joshi_flag = False
                            kaku_joshi_flag = False
                            continue
                        elif mrph.bunrui == '括弧始':
                            kakko_flag = True
                        if midasi != '':
                            if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                                if not(joshi_flag) and not(sento_joshi_flag):
                                    if kaku_joshi_flag:
                                        midasi = midasi[:-1]
                                    temp.append(midasi)
                            sento_joshi_flag = False
                            midasi = ''
                if midasi != '':
                    if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                        if not(sento_joshi_flag):
                            temp.append(midasi)
                    midasi = ''

                kakko_flag = False
                sento_joshi_flag = False
                bnst = bnst_dic[index_list[1]]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and mrph.bunrui != '括弧始' and mrph.bunrui != '括弧終' and (mrph.midasi != 'など' or mrph.hinsi != '助詞' or mrph.bunrui != '副助詞') and ((mrph.midasi != 'や' and mrph.midasi != 'か') or mrph.hinsi != '助詞' or mrph.bunrui != '接続助詞'):
                        if midasi == '' and mrph.hinsi =='助詞':
                            sento_joshi_flag = True
                        midasi += mrph.midasi
                        if mrph.hinsi == '助詞' and (mrph.midasi != 'と' and mrph.midasi != 'を') and (mrph.bunrui == '格助詞' or mrph.bunrui == '副助詞'):
                            joshi_flag = True
                            kaku_joshi_flag = False
                        elif mrph.hinsi == '助詞' and (mrph.midasi == 'と' or mrph.midasi == 'を') and mrph.bunrui == '格助詞':
                            joshi_flag = False
                            kaku_joshi_flag = True
                        else:
                            joshi_flag = False
                            kaku_joshi_flag = False
                    else:
                        if mrph.bunrui == '括弧終':
                            kakko_flag = False
                        elif mrph.bunrui == '読点' and kakko_flag:
                            midasi += mrph.midasi
                            joshi_flag = False
                            kaku_joshi_flag = False
                            continue
                        elif mrph.bunrui == '括弧始':
                            kakko_flag = True
                        if midasi != '':
                            if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                                if not(joshi_flag) and not(sento_joshi_flag):
                                    if kaku_joshi_flag:
                                        midasi = midasi[:-1]
                                    temp.append(midasi)
                            sento_joshi_flag = False
                            midasi = ''
                if midasi != '':
                    if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                        if not(sento_joshi_flag):
                            temp.append(midasi)
        
        if type_id == 29:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1])):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    midasi = ''
                    kakko_flag = False
                    sento_joshi_flag = False
                    continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and mrph.bunrui != '括弧始' and mrph.bunrui != '括弧終' and (mrph.midasi != 'など' or mrph.hinsi != '助詞' or mrph.bunrui != '副助詞') and ((mrph.midasi != 'や' and mrph.midasi != 'か') or mrph.hinsi != '助詞' or mrph.bunrui != '接続助詞'):
                        if midasi == '' and mrph.hinsi =='助詞':
                            sento_joshi_flag = True
                        midasi += mrph.midasi
                        if mrph.hinsi == '助詞' and (mrph.midasi != 'と' and mrph.midasi != 'を') and (mrph.bunrui == '格助詞' or mrph.bunrui == '副助詞'):
                            joshi_flag = True
                            kaku_joshi_flag = False
                        elif mrph.hinsi == '助詞' and (mrph.midasi == 'と' or mrph.midasi == 'を') and mrph.bunrui == '格助詞':
                            joshi_flag = False
                            kaku_joshi_flag = True
                        else:
                            joshi_flag = False
                            kaku_joshi_flag = False
                    else:
                        if mrph.bunrui == '括弧終':
                            kakko_flag = False
                        elif mrph.bunrui == '読点' and kakko_flag:
                            midasi += mrph.midasi
                            joshi_flag = False
                            kaku_joshi_flag = False
                            continue
                        elif mrph.bunrui == '括弧始':
                            kakko_flag = True
                        if midasi != '':
                            if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                                if not(joshi_flag) and not(sento_joshi_flag):
                                    if kaku_joshi_flag:
                                        midasi = midasi[:-1]
                                    temp.append(midasi)
                            sento_joshi_flag = False
                            midasi = ''
            if midasi != '':
                if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                    if midasi != '':
                        if not(sento_joshi_flag):
                            midasi = midasi[:-1]
                            temp.append(midasi)

        if type_id == 35:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    midasi = ''
                    kakko_flag = False
                    sento_joshi_flag = False
                    continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and mrph.bunrui != '括弧始' and mrph.bunrui != '括弧終' and (mrph.midasi != 'など' or mrph.hinsi != '助詞' or mrph.bunrui != '副助詞') and ((mrph.midasi != 'や' and mrph.midasi != 'か') or mrph.hinsi != '助詞' or mrph.bunrui != '接続助詞'):
                        if midasi == '' and mrph.hinsi =='助詞':
                            sento_joshi_flag = True
                        midasi += mrph.midasi
                        if mrph.hinsi == '助詞' and (mrph.midasi != 'と' and mrph.midasi != 'を') and (mrph.bunrui == '格助詞' or mrph.bunrui == '副助詞'):
                            joshi_flag = True
                            kaku_joshi_flag = False
                        elif mrph.hinsi == '助詞' and (mrph.midasi == 'と' or mrph.midasi == 'を') and mrph.bunrui == '格助詞':
                            joshi_flag = False
                            kaku_joshi_flag = True
                        else:
                            joshi_flag = False
                            kaku_joshi_flag = False
                    else:
                        if mrph.bunrui == '括弧終':
                            kakko_flag = False
                        elif mrph.bunrui == '読点' and kakko_flag:
                            midasi += mrph.midasi
                            joshi_flag = False
                            kaku_joshi_flag = False
                            continue
                        elif mrph.bunrui == '括弧始':
                            kakko_flag = True
                        if midasi != '':
                            if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                                if not(joshi_flag) and not(sento_joshi_flag):
                                    if kaku_joshi_flag:
                                        midasi = midasi[:-1]
                                    temp.append(midasi)
                            sento_joshi_flag = False
                            midasi = ''
            if midasi != '':
                if midasi != 'か' and midasi != 'や' and midasi != 'と' and midasi != 'を' and midasi != 'も' and midasi != 'で' and midasi != 'の' and midasi != 'とか' and midasi != 'などの' and 'のように' not in midasi and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも' and midasi != 'それでは':
                    if midasi != '':
                        if not(sento_joshi_flag):
                            temp.append(midasi)

        temp = [s for s in temp if s != 'Google' and s != 'OKGoogle']
        if temp:
            if str(type_id) in INST_extract:
                INST_extract[str(type_id)] += temp
            else:
                INST_extract[str(type_id)] = temp
            INST_extract[str(type_id)] = list(dict.fromkeys(INST_extract[str(type_id)]))
    
    return INST_extract

def SELECTextract(bnst_dic, SELECT_list):
    SELECT_extract = {}
    for q_dic in SELECT_list:
        type_id = q_dic['type']
        index_list = q_dic['index']
        n = len(index_list)
        temp = []
        if type_id == 11 or type_id == 12 or type_id == 16:
            start = 1
            for start in reversed(range(1, int(index_list[0]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[0])):
                bnst = bnst_dic[str(i)]['bnst']
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if type_id == 1 or type_id == 2 or type_id == 3 or type_id == 4 or type_id == 5 or type_id == 6 or type_id == 7 or type_id == 8 or type_id == 10 or type_id == 13 or type_id == 14 or type_id == 15:
            start = 1
            for start in reversed(range(1, int(index_list[0]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[0]) + 1):
                bnst = bnst_dic[str(i)]['bnst']
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    midasi = ''
                    temp = []
                    continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点' and not(mrph.midasi == 'か' and mrph.hinsi == '助詞' and mrph.bunrui == '接続助詞'):
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または' and midasi != 'もしくは' and midasi != 'それとも':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                if type_id == 2 or type_id == 3 or type_id == 4 or type_id == 6:
                    if 0 < len(temp):
                        temp = []
                    midasi = midasi[:-1]
                    temp.append(midasi)
                elif type_id == 8:
                    midasi = midasi[:-1]
                    temp.append(midasi)
                elif type_id == 10:
                    if midasi[-2:] == 'から':
                        midasi = midasi[:-2]
                        if midasi != '':
                            temp.append(midasi)
            elif midasi == '':
                if (type_id == 2 or type_id == 3 or type_id == 4 or type_id == 5 or type_id == 6) and temp:
                    if 1 < len(temp):
                        temp = temp[-1:]
                    
        if type_id == 1 or type_id == 14 or type_id == 15:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1])):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if type_id == 2 or type_id == 3 or type_id == 4 or type_id == 5 or type_id == 6 or type_id == 9 or type_id == 13 or type_id == 17:
            midasi = ''
            for i in range(int(index_list[0]) + 1, int(index_list[1]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    midasi = ''
                    continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                if type_id == 4 or type_id == 5 or type_id == 6 or type_id == 9 or type_id == 13 or type_id == 17:
                    midasi = midasi[:-1]
                    if midasi[-1] == 'か':
                        midasi = midasi[:-1]
                temp.append(midasi)
            else:
                if (type_id == 4 or type_id == 5 or type_id == 6 or type_id == 9 or type_id == 13) or temp:
                    temp[-1] = temp[-1][:-1]
                    if temp[-1][-1] == 'か':
                        temp[-1] = temp[-1][:-1]

        if type_id == 13:
            midasi = ''
            for i in range(int(index_list[1]) + 1, int(index_list[2]) + 1):
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if type_id == 17 and temp:
            if str(type_id) in SELECT_extract:
                SELECT_extract[str(type_id)] += temp
            else:
                SELECT_extract[str(type_id)] = temp
            SELECT_extract[str(type_id)] = list(dict.fromkeys(SELECT_extract[str(type_id)]))
        elif temp and 2 <= len(temp):
            if str(type_id) in SELECT_extract:
                SELECT_extract[str(type_id)] += temp
            else:
                SELECT_extract[str(type_id)] = temp
            SELECT_extract[str(type_id)] = list(dict.fromkeys(SELECT_extract[str(type_id)]))
    return SELECT_extract

def LINKextract(bnst_dic, LINK_list):
    LINK_extract = {}
    for q_dic in LINK_list:
        type_id = q_dic['type']
        index_list = q_dic['index']
        n = len(index_list)
        temp = []
        if type_id == 9 or type_id == 11:
            start = 1
            for start in reversed(range(1, int(index_list[0]) - 1)):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[0]) - 1):
                bnst = bnst_dic[str(i)]['bnst']
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if type_id == 1 or type_id == 2 or type_id == 3 or type_id == 7 or type_id == 8:
            start = 1
            for start in reversed(range(1, int(index_list[0]))):
                b = bnst_dic[str(start)]['feature']
                if not(b):
                    break
            midasi = ''
            for i in range(start + 1, int(index_list[0]) + 1):
                bnst = bnst_dic[str(i)]['bnst']
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                if type_id == 1 or type_id == 2 or type_id == 3:
                    midasi = midasi[:-1]
                temp.append(midasi)

        if type_id == 3:
            midasi = ''
            for i in range(int(index_list[0]) + 2, int(index_list[1]) + 1):
                b = bnst_dic[str(i)]['feature']
                if not(b):
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                midasi = midasi[:-1]
                temp.append(midasi)

        if type_id == 1 or type_id == 2:
            midasi = ''
            for i in range(int(index_list[1]) + 1, int(index_list[2]) + 1):
                b = bnst_dic[str(i)]['feature']
                if not(b):
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                midasi = midasi[:-1]
                temp.append(midasi)

        if type_id == 4:
            midasi = ''
            for i in range(int(index_list[3]) + 1, int(index_list[4]) + 1):
                b = bnst_dic[str(i)]['feature']
                if not(b):
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if type_id == 5 or type_id == 10:
            midasi = ''
            for i in range(int(index_list[2]) + 2, int(index_list[3]) + 1):
                b = bnst_dic[str(i)]['feature']
                if not(b):
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            if midasi != 'や' and midasi != 'と' and midasi != 'または':
                                temp.append(midasi)
                            midasi = ''
            if midasi != '':
                midasi = midasi[:-1]
                temp.append(midasi)
            if type_id == 5 and len(temp) < 2:
                temp = []

        if type_id == 6:
            midasi = ''
            for i in range(int(index_list[1]) + 2, int(index_list[2]) + 1):
                b = bnst_dic[str(i)]['feature']
                if not(b):
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                flag = False
                for f in example_parse:
                    f_n = len(f)
                    b = bnst_dic[str(i)]['feature']
                    b_n = len(b)
                    fb = set(f) & set(b)
                    fb_n = len(fb)
                    if f_n == fb_n:
                        flag = True
                        break
                if flag:
                    if midasi != '':
                        temp.append(midasi)
                        midasi = ''
                        continue
                bnst = bnst_dic[str(i)]['bnst']
                for mrph in bnst.mrph_list():
                    if mrph.bunrui != '読点':
                        midasi += mrph.midasi
                    else:
                        if midasi != '':
                            temp.append(midasi)
                            midasi = ''
            if midasi != '':
                temp.append(midasi)

        if temp:
            if str(type_id) in LINK_extract:
                LINK_extract[str(type_id)] += temp
            else:
                LINK_extract[str(type_id)] = temp
            LINK_extract[str(type_id)] = list(dict.fromkeys(LINK_extract[str(type_id)]))
    return LINK_extract
    
def type_get(res, parse_rule):
    extract_dic = {}
    sentence_list, bnst_dic, type_dic = questionJA.question(res, parse_rule)
    print(bnst_dic)
    print(type_dic)
    if 'YESNO' in type_dic:
        if 'SELECT' in type_dic:
            YESNO_list = type_dic['YESNO']['question']
            SELECT_list = type_dic['SELECT']['question']
            for y_dic in YESNO_list:
                flag = True
                s1_id = y_dic['sentence_id']
                for s_dic in SELECT_list:
                    s2_id = s_dic['sentence_id']
                    if s1_id == s2_id:
                        flag = False
                        break
                if not(flag):
                    continue
                extract_dic['YESNO'] = {}
                break
        if 'NE' in type_dic:
            YESNO_list = type_dic['YESNO']['question']
            NE_list = type_dic['NE']['question']
            for y_dic in YESNO_list:
                flag = True
                s1_id = y_dic['sentence_id']
                for n_dic in NE_list:
                    s2_id = n_dic['sentence_id']
                    if s1_id == s2_id:
                        flag = False
                        break
                if not(flag):
                    continue
                extract_dic['YESNO'] = {}
                break
        if 'LINK' in type_dic:
            LINK_list = type_dic['LINK']['question']
            flag = True
            for l_dic in LINK_list:
                type_id = l_dic['type']
                if type_id in [1, 3, 4, 10]:
                    flag = False
                    break
            if flag:
                extract_dic['YESNO'] = {}
        if 'NE' not in type_dic and 'SELECT' not in type_dic and 'LINK' not in type_dic:
            extract_dic['YESNO'] = {}
    if 'NE' in type_dic:
        NE_extract = NEextract(bnst_dic, type_dic['NE']['question'])
        if NE_extract:
            extract_dic['NE'] = NE_extract
    if 'INST' in type_dic:
        if 'NE' in type_dic:
            INST_list = type_dic['INST']['question']
            NE_list = type_dic['NE']['question']
            INST_n = len(INST_list)
            for i_id in range(INST_n):
                i_dic = INST_list[i_id]
                flag = True
                s1_id = i_dic['sentence_id']
                for s_dic in NE_list:
                    type_id = s_dic['type']
                    if (27 <= type_id and type_id <= 42) or type_id == 45 or type_id == 47 or type_id == 48:
                        continue
                    s2_id = s_dic['sentence_id']
                    if s1_id == s2_id:
                        s1_index = i_dic['index']
                        s2_index = s_dic['index']
                        for idx in range(int(s2_index[0]), int(s2_index[-1]) + 1):
                            if str(idx) in s1_index:
                                flag = False
                                break
                        if not(flag):
                            break
                if not(flag):
                    INST_list[i_id] = None
            INST_list = [s for s in INST_list if s]
            type_dic['INST']['question'] = INST_list
        INST_extract = INSTextract(bnst_dic, type_dic['INST']['question'])
        if INST_extract:
            extract_dic['INST'] = INST_extract
    if 'SELECT' in type_dic:
        SELECT_extract = SELECTextract(bnst_dic, type_dic['SELECT']['question'])
        if SELECT_extract:
            extract_dic['SELECT'] = SELECT_extract
    if 'LINK' in type_dic:
        LINK_extract = LINKextract(bnst_dic, type_dic['LINK']['question'])
        if LINK_extract:
            extract_dic['LINK'] = LINK_extract
    if 'OTHER' in type_dic:
        extract_dic['OTHER'] = {}
            
    return extract_dic
