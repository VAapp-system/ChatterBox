import sentenceJA
import re
from pyknp import KNP

joshi = ["ガ", "ヲ", "ニ", "デ", "カラ", "ヨリ", "ヘ", "マデ", "ニテ", "ハ", "デハ", "ニハ", "ニモ", "トハ", "トモ", "デモ", "モ", "ト", "タリ", "テモ", "カ"]
bunmatsu = ["否定表現", "準否定表現", "態:受動", "係:連格", "係:連用", "係:NONE", "体言止", "連体修飾", "時制-過去", "～たい", "複合辞", "二重否定"]
bunmatsu_dousi = ["答え", "教えて", "指定", "並べて", "命令して", "言って", "おっしゃって", "仰って", "入力", "話", "声", "選", "質問", "回答して", "解答して", "いって", "終了して", "探してみて", "尋ねて", "当てて", "呼", "タップ", "聞", "お願い", "ログイン", "検索"]
bunmatsu_meirei = ['呼', '続', '言', 'いった', '話', '問', '教', 'いえ', '感謝して', 'タップ']
bunmatsu_sentaku = ['教', '選', '指定', '言']
gimonshi = ["どんな", "どのような", "どういった", "どういう", 'どう']

def NE(temp_dic, bnst_dic, sentence_list):
    type_id = temp_dic['type']
    index_list = temp_dic['index']
    s_id = temp_dic['sentence_id']
    if type_id == 35:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        if midasi != 'どうぞ':
            return False
    if type_id == 36:
        count = index_list[2]
        midasi = bnst_dic[count]['midasi']
        if midasi != 'どうぞ':
            return False
    if type_id == 51:
        count = index_list[0]
        b = bnst_dic[count]['feature']
        if '体言止' in b:
            return False
    if type_id == 54:
        sentence = sentence_list[s_id] + '？'
        sentence = sentence.strip()
        knp = KNP()
        try:
            result = knp.parse(sentence)
        except:
            return False
        bnst = result.bnst_list()[-1]
        feature = bnst.fstring
        if '疑問' not in feature:
            return False
    return True

def INST(temp_dic, bnst_dic):
    type_id = temp_dic['type']
    index_list = temp_dic['index']
    if type_id == 5 or type_id == 21:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        if '言うと' not in midasi and 'いうと' not in midasi:
            return False
    if (4 <= type_id and type_id <= 9) or type_id == 11 or type_id == 13 or type_id == 18 or type_id == 19:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        for meirei in bunmatsu_meirei:
            if meirei in midasi:
                return True
        return False
    if type_id == 20:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        if '教' in midasi or '答' in midasi or '選択' in midasi:
            return False
    if type_id == 28:
        count = index_list[2]
        b = bnst_dic[count]['feature']
        if '否定表現' in b:
            return False
        count = index_list[0]
        midasi = bnst_dic[count]['midasi']
        if 'などの' not in midasi:
            return False
    if type_id == 29:
        count = index_list[0]
        b = bnst_dic[str(int(count) - 1)]['feature']
        if not(b):
            return False
    if type_id == 32:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        if 'いずれか' not in midasi:
            return False
    return True

def SELECT(temp_dic, bnst_dic):
    type_id = temp_dic['type']
    index_list = temp_dic['index']
    if type_id == 3 or type_id == 10:
        count = index_list[1]
        midasi = bnst_dic[count]['midasi']
        flag = True
        for sentaku in bunmatsu_sentaku:
            if sentaku in midasi:
                flag = False
        if flag:
            return False
    if type_id == 4:
        count = index_list[2]
        midasi = bnst_dic[count]['midasi']
        flag = True
        for sentaku in bunmatsu_sentaku:
            if sentaku in midasi:
                flag = False
        if flag:
            return False
    if type_id == 8:
        count = index_list[3]
        midasi = bnst_dic[count]['midasi']
        flag = True
        for sentaku in bunmatsu_sentaku:
            if sentaku in midasi:
                flag = False
        if flag:
            return False
    if type_id == 17:
        count = index_list[0]
        b = bnst_dic[str(int(count) - 1)]['feature']
        if b:
            return False
    return True

def YESNO(temp_dic, bnst_dic, sentence_list):
    type_id = temp_dic['type']
    index_list = temp_dic['index']
    index_start = index_list[0]
    s_id = temp_dic['sentence_id']
    for count in reversed(range(1, int(index_start))):
        count = str(count)
        b = bnst_dic[count]['feature']
        if not(b):
            break
        if '疑問詞' in b:
            return False
    if 'どちら' in sentence_list[s_id] or 'それとも' in sentence_list[s_id] or 'または' in sentence_list[s_id]:
        return False
    if type_id == 8:
        count = index_list[1]
        b = bnst_dic[count]['feature']
        if '文末' not in b:
            return False
    if type_id == 12 or type_id == 13 or type_id == 14:
        count = index_list[0]
        b = bnst_dic[count]['feature']
        if '文末' not in b:
            return False
    if type_id != 8 or type_id != 12 or type_id != 13 or type_id != 14:
        count = index_list[0]
        b = bnst_dic[count]['feature']
        if '疑問詞' in b:
            return False
    if type_id == 11:
        sentence = sentence_list[s_id] + '？'
        sentence = sentence.strip()
        knp = KNP()
        try:
            result = knp.parse(sentence)
        except:
            return False
        bnst = result.bnst_list()[-1]
        feature = bnst.fstring
        if '疑問' not in feature:
            return False
    return True

def LINK(temp_dic, bnst_dic, sentence_list):
    type_id = temp_dic['type']
    index_list = temp_dic['index']
    if type_id == 1 or type_id == 2 or type_id == 3:
        b1_id = bnst_dic[index_list[0]]['sentence_id']
        b2_id = bnst_dic[index_list[1]]['sentence_id']
        if b1_id != b2_id - 1:
            return False
        if sentence_list[b1_id] in sentence_list[b2_id] or sentence_list[b2_id] in sentence_list[b1_id]:
            return False
    if type_id == 5:
        b1_id = bnst_dic[index_list[2]]['sentence_id']
        b2_id = bnst_dic[index_list[3]]['sentence_id']
        if b1_id != b2_id - 1:
            return False
    if type_id == 6:
        b1_id = bnst_dic[index_list[1]]['sentence_id']
        b2_id = bnst_dic[index_list[2]]['sentence_id']
        if b1_id != b2_id - 1:
            return False   
    return True

def question(res, parse_rule):
    sentence_list = sentenceJA.split(res)
    count = 1
    s_i = 0
    bnst_dic = {}
    bnst_dic[str(count)] = {
        "feature": [],
        "midasi": None,
        "bnst": None,
        "sentence_id": s_i
    }
    count += 1
    for sentence in sentence_list:
        sentence = sentence.strip('.')
        sentence = sentence.strip()
        try:
            knp = KNP()
            result = knp.parse(sentence)
        except:
            continue
        for bnst in result.bnst_list():
            feature = bnst.fstring
            feature = feature.replace('〜', '～')
            midasi = "".join(mrph.midasi for mrph in bnst.mrph_list())
            feature_list = re.split('<|><|>', feature)
            feature_list = [f for f in feature_list if f != '']
            bnst_dic[str(count)] = {
                "feature": feature_list,
                "midasi": midasi,
                "bnst": bnst,
                "sentence_id": s_i
            }
            count += 1
        s_i += 1
        bnst_dic[str(count)] = {
            "feature": [],
            "midasi": None,
            "bnst": None,
            "sentence_id": s_i
        }
        count += 1

    type_dic = {}
    rule = parse_rule["NE"]
    r_n = len(rule)
    for i in range(r_n):
        feature_list = rule[i]
        index_list = ['-1']
        stack1 = list(reversed(feature_list))
        stack2 = []
        f_count = 0
        feature_n = len(feature_list)
        count_d = '-1'
        while True:
            f = stack1[-1]
            f_n = len(f)
            flag2 = False
            flag4 = False
            for count in bnst_dic:
                if int(count) <= int(count_d):
                    continue
                b = bnst_dic[count]["feature"]
                if not(b):
                    flag4 = True
                    break
                f_and_b = set(f) & set(b)
                fb_n = len(f_and_b)
                if f_n == fb_n:
                    if stack2 and ('用言:動' in f or '用言:形' in f) and ('助詞' in stack2[-1] and 'カ' not in stack2[-1]):
                        if int(count_d) + 1 != int(count):
                            continue
                    if f_n == 1 and f[0] == '用言:動':
                        if len(bnst_dic[count]["midasi"]) == 1:
                            continue
                        joshi_icci = set(joshi) & set(b)
                        if 0 < len(joshi_icci):
                            continue
                        bnmatsu_icci = set(bunmatsu) & set(b)
                        if 0 < len(bnmatsu_icci):
                            continue
                        m = bnst_dic[count]["midasi"]
                        if ('ました' in m) or ('ます' in m) or ('でした' in m) or ('です' in m) or ('ている' in m) or ('しょう' in m):
                            continue
                        flag3 = True
                        for dousi in bunmatsu_dousi:
                            if dousi in m:
                                flag3 = False
                                break
                        if flag3:
                            continue
                        if int(count_d) + 1 != int(count):
                            continue
                    flag2 = True
                    break

            if flag4:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    count_d = count
                continue

            if flag2:
                f_count += 1
                count_d = count
                index_list.append(count)
                stack2.append(stack1.pop())
                if f_count == feature_n:
                    if "NE" not in type_dic:
                        type_dic["NE"] = {
                            "question": []
                        }
                    line = ''
                    for index in index_list[1:]:
                        line += bnst_dic[index]['midasi']
                    temp_dic = {
                        "midasi": line,
                        "type": i + 1,
                        "index": index_list[1:],
                        "sentence_id": bnst_dic[index_list[1]]['sentence_id']
                    }
                    if NE(temp_dic, bnst_dic, sentence_list):
                        type_dic["NE"]["question"].append(temp_dic)
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
            else:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    break

    rule = parse_rule["SELECT"]
    r_n = len(rule)
    for i in range(r_n):
        feature_list = rule[i]
        index_list = ['-1']
        stack1 = list(reversed(feature_list))
        stack2 = []
        f_count = 0
        feature_n = len(feature_list)
        count_d = '-1'
        while True:
            f = stack1[-1]
            f_n = len(f)
            flag2 = False
            flag4 = False
            for count in bnst_dic:
                if int(count) <= int(count_d):
                    continue
                b = bnst_dic[count]["feature"]
                if not(b):
                    flag4 = True
                    break
                f_and_b = set(f) & set(b)
                fb_n = len(f_and_b)
                if f_n == fb_n:
                    if stack2 and ('用言:動' in f or '用言:形' in f) and ('助詞' in stack2[-1] and ('カ' not in stack2[-1] and '並列タイプ:OR' not in stack2[-1])):
                        if int(count_d) + 1 != int(count):
                            continue
                    if f_n == 1 and f[0] == '用言:動':
                        if len(bnst_dic[count]["midasi"]) == 1:
                            continue
                        joshi_icci = set(joshi) & set(b)
                        if 0 < len(joshi_icci):
                            continue
                        bnmatsu_icci = set(bunmatsu) & set(b)
                        if 0 < len(bnmatsu_icci):
                            continue
                        m = bnst_dic[count]["midasi"]
                        if ('ました' in m) or ('ます' in m) or ('でした' in m) or ('です' in m) or ('ている' in m) or ('しょう' in m):
                            continue
                        if int(count_d) + 1 != int(count):
                            continue
                    flag2 = True
                    break

            if flag4:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    count_d = count
                continue

            if flag2:
                f_count += 1
                count_d = count
                index_list.append(count)
                stack2.append(stack1.pop())
                if f_count == feature_n:
                    if "SELECT" not in type_dic:
                        type_dic["SELECT"] = {
                            "question": []
                        }
                    line = ''
                    for index in index_list[1:]:
                        line += bnst_dic[index]['midasi']
                    temp_dic = {
                        "midasi": line,
                        "type": i + 1,
                        "index": index_list[1:],
                        "sentence_id": bnst_dic[index_list[1]]['sentence_id']
                    }
                    if SELECT(temp_dic, bnst_dic):
                        type_dic["SELECT"]["question"].append(temp_dic)
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
            else:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    break

    rule = parse_rule["INST"]
    r_n = len(rule)
    for i in range(r_n):
        feature_list = rule[i]
        index_list = ['-1']
        stack1 = list(reversed(feature_list))
        stack2 = []
        f_count = 0
        feature_n = len(feature_list)
        count_d = '-1'
        while True:
            f = stack1[-1]
            f_n = len(f)
            flag2 = False
            flag4 = False
            for count in bnst_dic:
                if int(count) <= int(count_d):
                    continue
                b = bnst_dic[count]["feature"]
                if not(b):
                    flag4 = True
                    break
                f_and_b = set(f) & set(b)
                fb_n = len(f_and_b)
                if f_n == fb_n:
                    if stack2 and ('用言:動' in f or '用言:形' in f) and ('助詞' in stack2[-1] and 'カ' not in stack2[-1]):
                        if int(count_d) + 1 != int(count):
                            continue
                    if f_n == 1 and f[0] == '用言:動':
                        if len(bnst_dic[count]["midasi"]) == 1:
                            continue
                        joshi_icci = set(joshi) & set(b)
                        if 0 < len(joshi_icci):
                            continue
                        bnmatsu_icci = set(bunmatsu) & set(b)
                        if 0 < len(bnmatsu_icci):
                            continue
                        m = bnst_dic[count]["midasi"]
                        if ('ました' in m) or ('ます' in m) or ('でした' in m) or ('です' in m) or ('ている' in m) or ('しょう' in m):
                            continue
                        if i != 2:
                            flag3 = True
                            for dousi in bunmatsu_dousi:
                                if dousi in m:
                                    flag3 = False
                                    break
                            if flag3:
                                continue
                        if int(count_d) + 1 != int(count):
                            continue
                    flag2 = True
                    break

            if flag4:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    count_d = count
                continue

            if flag2:
                f_count += 1
                count_d = count
                index_list.append(count)
                stack2.append(stack1.pop())
                if f_count == feature_n:
                    if "INST" not in type_dic:
                        type_dic["INST"] = {
                            "question": []
                        }
                    line = ''
                    for index in index_list[1:]:
                        line += bnst_dic[index]['midasi']
                    temp_dic = {
                        "midasi": line,
                        "type": i + 1,
                        "index": index_list[1:],
                        "sentence_id": bnst_dic[index_list[1]]['sentence_id']
                    }
                    if INST(temp_dic, bnst_dic):
                        type_dic["INST"]["question"].append(temp_dic)
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
            else:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    break
    
    rule = parse_rule["YESNO"]
    r_n = len(rule)
    for i in range(r_n):
        feature_list = rule[i]
        index_list = ['-1']
        stack1 = list(reversed(feature_list))
        stack2 = []
        f_count = 0
        feature_n = len(feature_list)
        count_d = '-1'
        while True:
            f = stack1[-1]
            f_n = len(f)
            flag2 = False
            flag4 = False
            for count in bnst_dic:
                if int(count) <= int(count_d):
                    continue
                b = bnst_dic[count]["feature"]
                if not(b):
                    flag4 = True
                    break
                f_and_b = set(f) & set(b)
                fb_n = len(f_and_b)
                if f_n == fb_n:
                    if stack2 and ('用言:動' in f or '用言:形' in f) and (('助詞' in stack2[-1] and 'カ' not in stack2[-1]) or '修飾' in stack2[-1]):
                        if int(count_d) + 1 != int(count):
                            continue
                    flag2 = True
                    break
            if flag4:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    count_d = count
                continue

            if flag2:
                f_count += 1
                count_d = count
                index_list.append(count)
                stack2.append(stack1.pop())
                if f_count == feature_n:
                    if "YESNO" not in type_dic:
                        type_dic["YESNO"] = {
                            "question": []
                        }
                    line = ''
                    for index in index_list[1:]:
                        line += bnst_dic[index]['midasi']
                    temp_dic = {
                        "midasi": line,
                        "type": i + 1,
                        "index": index_list[1:],
                        "sentence_id": bnst_dic[index_list[1]]['sentence_id']
                    }
                    if YESNO(temp_dic, bnst_dic, sentence_list):
                        type_dic["YESNO"]["question"].append(temp_dic)
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
            else:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    break
    f1 = [
        "カ",
        "助詞",
        "用言:動"
    ]
    f2 = [
        "カ",
        "助詞",
        "用言:形"
    ]
    f3 = [
        "カ",
        "助詞",
        "用言:判"
    ]
    f1_n = len(f1)
    f2_n = len(f2)
    f3_n = len(f3)
    for count in bnst_dic:
        b = bnst_dic[count]["feature"]
        if not(b):
            continue
        f1_and_b = set(f1) & set(b)
        f2_and_b = set(f2) & set(b)
        f3_and_b = set(f3) & set(b)
        f1b_n = len(f1_and_b)
        f2b_n = len(f2_and_b)
        f3b_n = len(f3_and_b)
        if f1_n == f1b_n:
            line = bnst_dic[count]["midasi"]
            if "YESNO" not in type_dic:
                type_dic["YESNO"] = {
                    "question": []
                }
            temp_dic = {
                "midasi": line,
                "type": 12,
                "index": [count],
                "sentence_id": bnst_dic[count]['sentence_id']
            }
            if YESNO(temp_dic, bnst_dic, sentence_list):
                type_dic["YESNO"]["question"].append(temp_dic)
        elif f2_n == f2b_n:
            line = bnst_dic[count]["midasi"]
            if "YESNO" not in type_dic:
                type_dic["YESNO"] = {
                    "question": []
                }
            temp_dic = {
                "midasi": line,
                "type": 13,
                "index": [count],
                "sentence_id": bnst_dic[count]['sentence_id']
            }
            if YESNO(temp_dic, bnst_dic, sentence_list):
                type_dic["YESNO"]["question"].append(temp_dic)
        elif f3_n == f3b_n:
            line = bnst_dic[count]["midasi"]
            if "YESNO" not in type_dic:
                type_dic["YESNO"] = {
                    "question": []
                }
            temp_dic = {
                "midasi": line,
                "type": 14,
                "index": [count],
                "sentence_id": bnst_dic[count]['sentence_id']
            }
            if YESNO(temp_dic, bnst_dic, sentence_list):
                type_dic["YESNO"]["question"].append(temp_dic)

    rule = parse_rule["LINK"]
    r_n = len(rule)
    for i in range(r_n):
        feature_list = rule[i]
        index_list = ['-1']
        stack1 = list(reversed(feature_list))
        stack2 = []
        f_count = 0
        feature_n = len(feature_list)
        count_d = '-1'
        while True:
            f = stack1[-1]
            f_n = len(f)
            flag2 = False
            for count in bnst_dic:
                if int(count) <= int(count_d):
                    continue
                b = bnst_dic[count]["feature"]
                midasi = bnst_dic[count]['midasi']
                if not(b):
                    continue
                f_and_b = set(f) & set(b)
                fb_n = len(f_and_b)
                if f_n == fb_n:
                    if stack2 and ('用言:動' in f or '用言:形' in f) and ('助詞' in stack2[-1] and 'カ' not in stack2[-1]):
                        if int(count_d) + 1 != int(count):
                            continue
                    if (f_n == 1 and f[0] == '用言:動') or (f_n == 2 and '文末' in f and '用言:動' in f):
                        if len(bnst_dic[count]["midasi"]) == 1:
                            continue
                        joshi_icci = set(joshi) & set(b)
                        if 0 < len(joshi_icci):
                            continue
                        bnmatsu_icci = set(bunmatsu) & set(b)
                        if 0 < len(bnmatsu_icci):
                            continue
                        m = bnst_dic[count]["midasi"]
                        if ('ました' in m) or ('でした' in m) or ('です' in m) or ('ている' in m) or ('しょう' in m):
                            continue
                        if int(count_d) + 1 != int(count):
                            continue
                    flag2 = True
                    break
            if flag2:
                f_count += 1
                count_d = count
                index_list.append(count)
                stack2.append(stack1.pop())
                if f_count == feature_n:
                    if "LINK" not in type_dic:
                        type_dic["LINK"] = {
                            "question": []
                        }
                    line = ''
                    for index in index_list[1:]:
                        line += bnst_dic[index]['midasi']
                    temp_dic = {
                        "midasi": line,
                        "type": i + 1,
                        "index": index_list[1:]
                    }
                    if LINK(temp_dic, bnst_dic, sentence_list):
                        type_dic["LINK"]["question"].append(temp_dic)
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
            else:
                if stack2:
                    f_count -= 1
                    count_d = index_list.pop()
                    stack1.append(stack2.pop())
                else:
                    break

    if "NE" in type_dic and not(type_dic["NE"]["question"]):
        type_dic.pop("NE")
    if "SELECT" in type_dic and not(type_dic["SELECT"]["question"]):
        type_dic.pop("SELECT")
    if "INST" in type_dic and not(type_dic["INST"]["question"]):
        type_dic.pop("INST")
    if "YESNO" in type_dic and not(type_dic["YESNO"]["question"]):
        type_dic.pop("YESNO")
    if "OTHER" in type_dic and not(type_dic["OTHER"]["question"]):
        type_dic.pop("OTHER")
    if "LINK" in type_dic and not(type_dic["LINK"]["question"]):
        type_dic.pop("LINK")
    return sentence_list, bnst_dic, type_dic
    