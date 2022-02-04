from nltk.tree import ParentedTree
import questionEN

w_tag = ['WHADJP', 'WHADVP', 'WHNP', 'WHPP', 'WDT', 'WP', 'WP$', 'WRB', 'WP-S']
i_tag = ['VB', 'VBG', 'VBP']
vb_words1 = ['ask', 'asking']
vb_words2 = ['say', 'saying']
vb_words3 = ['tell', 'telling']
wh_words = ['what', 'when', 'where', 'which', 'who', 'whom', 'whose', 'why', 'how']
sb_words = ['him', 'her', 'you', 'me', 'us', 'them']
kigo = ["``", "''", ",", ":"]


def INSTextract(temp_parse):
    INST_extract = {}
    for s_i in temp_parse:
        parse = temp_parse[s_i]
        flag1 = False
        flag2 = False
        R = 0
        temp_str = []
        subtrees = list(parse.subtrees(lambda parse: parse.height() == 2))
        t_n = len(subtrees)
        start_i = -1
        for i in range(t_n):
            subtree = subtrees[i]
            value_list = subtree.leaves()
            if not(flag1) and not(flag2) and value_list[0].lower() in vb_words1:
                flag1 = True
                start_i = i
                continue
            elif not(flag1) and not(flag2) and value_list[0].lower() in vb_words2:
                flag2 = True
                start_i = i
                continue

            if flag1:
                if R == 0 and i == start_i + 1 and subtree.label() in w_tag:
                    R = 1
                    start_i = i
                    break
                elif R == 0 and (value_list[0].lower() == 'like' or value_list[0].lower() == '…'):
                    R = 2
                    start_i = i + 1
                    break
                elif R == 0 and i == start_i + 1 and value_list[0].lower() == 'to':
                    R = 3
                    start_i = i + 1
                    break
                elif R == 0 and i == start_i + 1 and (value_list[0].lower() == 'about' or value_list[0].lower() == 'for'):
                    R = 4
                    start_i = i + 1
                    break
                elif R == 0 and i == start_i + 1 and value_list[0].lower() == 'that':
                    R = 5
                    start_i = i + 1
                    break
                elif R == 0 and i == start_i + 1 and (value_list[0] in sb_words or subtree.label == 'NNP' or subtree.label == 'NNPS'):
                    R = 6
                    start_i = i
                    continue
                elif R == 6 and i == start_i + 1 and subtree.label() in w_tag:
                    R = 1
                    start_i = i
                    break
                elif R == 6 and i == start_i + 1 and value_list[0].lower() == 'to':
                    R = 3
                    start_i = i + 1
                    break
                elif R == 6 and i == start_i + 1 and (value_list[0].lower() == 'about' or value_list[0].lower() == 'for'):
                    R = 4
                    start_i = i + 1
                    break

            if flag2:
                if R == 0 and i == start_i + 1 and subtree.label() in w_tag:
                    R = 1
                    start_i = i
                    break
                if R == 0 and (value_list[0].lower() == 'like' or value_list[0].lower() == '…'):
                    R = 2
                    start_i = i + 1
                    break
                if R == 0 and i < t_n - 1 and value_list[0].lower() == 'to' and subtrees[i + 1].label() == 'VB':
                    R = 3
                    end_i = i
                    break
                if R == 0 and i < t_n - 1 and value_list[0].lower() == 'for':
                    R = 4
                    end_i = i
                    break
                if R == 0 and i == start_i + 1 and value_list[0].lower() == 'that':
                    R = 5
                    start_i = i + 1
                    break
        if R == 0 and flag1:
            start_i += 1
            R = 4
        if R == 6 and flag1:
            start_i += 1
            R = 4
        if R == 0 and flag2:
            start_i += 1
            R = 5

        if flag1:
            for i in range(start_i, t_n):
                subtree = subtrees[i]
                value_list = subtree.leaves()
                temp_str += value_list
        elif flag2:
            if R == 1 or R == 2 or R == 5:
                for i in range(start_i, t_n):
                    subtree = subtrees[i]
                    value_list = subtree.leaves()
                    temp_str += value_list
            elif R == 3 or R == 4:
                for i in range(start_i + 1, end_i):
                    subtree = subtrees[i]
                    value_list = subtree.leaves()
                    temp_str += value_list

        if temp_str:
            temp = ' '.join(temp_str)
            temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
            temp = temp.replace('-LRB- ', '(')
            temp = temp.replace(' -RRB-', ')')
            if temp != '':
                if temp != '?' and temp != '!':
                    INST_extract[s_i] = temp
    return INST_extract

def SC_CCextract(temp_parse):
    SC_CC_extract = {}
    for s_i in temp_parse:
        parse = temp_parse[s_i]
        parse = ParentedTree.convert(parse)
        subtrees = list(parse.subtrees(lambda parse: parse.height() == 2))
        t_n = len(subtrees)
        for i in range(t_n):
            subtree = subtrees[i]
            if subtree.label() == 'CC' and (subtree.leaves()[0].lower() == 'or' or subtree.leaves()[0].lower() == 'and'):
                parent = subtree.parent()
                for subsubtree in parent:
                    if subsubtree.label() != 'CC' and subsubtree.label() != ',' and subsubtree.label() != '.' and subsubtree.label() != '``' and subsubtree.label() != "''":
                        temp_str = list(subsubtree.leaves())
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            if s_i in SC_CC_extract:
                                SC_CC_extract[s_i].append(temp)
                            else:
                                SC_CC_extract[s_i] = [temp]
                if s_i in SC_CC_extract and len(SC_CC_extract[s_i]) < 2:
                    SC_CC_extract[s_i] = []
    return SC_CC_extract

def SC_SCextract(temp_parse):
    SC_SC_extract = {}
    for s_i in temp_parse:
        parse = temp_parse[s_i]['parse']
        type_id = temp_parse[s_i]['class']
        temp_str = []
        subtrees = list(parse.subtrees(lambda parse: parse.height() == 2))
        t_n = len(subtrees)
        start_i = -1
        flag = False
        if type_id == 'a':
            for i in range(t_n):
                subtree = subtrees[i]
                value_list = subtree.leaves()
                if subtree.label() == 'CC' or subtree.label() == ',':
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            if s_i in SC_SC_extract:
                                SC_SC_extract[s_i].append(temp)
                            else:
                                SC_SC_extract[s_i] = [temp]
                    temp_str = []
                    flag = False
                if value_list[0].isdecimal():
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            if s_i in SC_SC_extract:
                                SC_SC_extract[s_i].append(temp)
                            else:
                                SC_SC_extract[s_i] = [temp]
                    temp_str = []
                    flag = True
                
                if flag:
                    temp_str += value_list
        else:
            for i in range(t_n):
                subtree = subtrees[i]
                value_list = subtree.leaves()
                if subtree.label() == 'CC' or subtree.label() == ',':
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            if s_i in SC_SC_extract:
                                SC_SC_extract[s_i].append(temp)
                            else:
                                SC_SC_extract[s_i] = [temp]
                    temp_str = []
                    flag = False
                if len(value_list[0]) == 1 and value_list[0].isalpha():
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            if s_i in SC_SC_extract:
                                SC_SC_extract[s_i].append(temp)
                            else:
                                SC_SC_extract[s_i] = [temp]
                    temp_str = []
                    flag = True
                
                if flag:
                    temp_str += value_list
        if temp_str:
            temp = ' '.join(temp_str)
            temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip("?").strip("!").strip()
            temp = temp.replace('-LRB- ', '(')
            temp = temp.replace(' -RRB-', ')')
            if temp != '':
                if s_i in SC_SC_extract:
                    SC_SC_extract[s_i].append(temp)
                else:
                    SC_SC_extract[s_i] = [temp]
        if s_i in SC_SC_extract and len(SC_SC_extract[s_i]) < 2:
            SC_SC_extract.pop(s_i)
    return SC_SC_extract

def NEextract(temp_parse):
    NE_extract = {}
    for s_i in temp_parse:
        parse = temp_parse[s_i]
        flag = False
        temp_str = []
        for subtree in parse.subtrees(lambda parse: parse.height() == 2):
            if subtree.label() in w_tag:
                flag = True
                temp_str += subtree.leaves()
                continue
            if flag:
                temp_str += subtree.leaves()
        temp = ' '.join(temp_str)
        temp = temp.replace('-LRB- ', '(')
        temp = temp.replace(' -RRB-', ')')
        if temp != '':
            NE_extract[s_i] = temp
    return NE_extract

def I_SC_CCextract(parse):
    I_SC_CC_extract = []
    flag1 = False
    flag2 = False
    kakko_flag = False
    R = 0
    temp_str = []
    subtrees = list(parse.subtrees(lambda parse: parse.height() == 2))
    t_n = len(subtrees)
    start_i = -1
    for i in range(t_n):
        subtree = subtrees[i]
        value_list = subtree.leaves()
        if subtree.label() == '``':
            kakko_flag = True
            continue
        elif subtree.label() == "''":
            kakko_flag = False
            continue
        if not(flag1) and not(flag2) and value_list[0].lower() in vb_words1:
            flag1 = True
            start_i = i
            continue
        elif not(flag1) and not(flag2) and value_list[0].lower() in vb_words2:
            flag2 = True
            start_i = i
            continue

        if flag1 and not(kakko_flag):
            if R == 0 and i == start_i + 1 and subtree.label() in w_tag:
                R = 1
                start_i = i
            elif R == 0 and (value_list[0].lower() == 'like' or value_list[0].lower() == '…'):
                R = 2
                start_i = i + 1
            elif R == 0 and i == start_i + 1 and value_list[0].lower() == 'to':
                R = 3
                start_i = i + 1
            elif R == 0 and i == start_i + 1 and (value_list[0].lower() == 'about' or value_list[0].lower() == 'for'):
                R = 4
                start_i = i + 1
            elif R == 0 and i == start_i + 1 and value_list[0].lower() == 'that':
                R = 5
                start_i = i + 1
            elif R == 0 and i == start_i + 1 and (value_list[0] in sb_words or subtree.label == 'NNP' or subtree.label == 'NNPS'):
                R = 6
                start_i = i
                continue
            elif R == 6 and i == start_i + 1 and subtree.label() in w_tag:
                R = 1
                start_i = i
            elif R == 6 and i == start_i + 1 and value_list[0].lower() == 'to':
                R = 3
                start_i = i + 1
            elif R == 6 and i == start_i + 1 and (value_list[0].lower() == 'about' or value_list[0].lower() == 'for'):
                R = 4
                start_i = i + 1

        if flag2 and not(kakko_flag):
            if R == 0 and i == start_i + 1 and subtree.label() in w_tag:
                R = 1
                start_i = i
            if R == 0 and (value_list[0].lower() == 'like' or value_list[0].lower() == '…'):
                R = 2
                start_i = i + 1
            if R == 0 and i < t_n - 1 and value_list[0].lower() == 'to' and subtrees[i + 1].label() == 'VB':
                R = 3
                end_i = i
            if R == 0 and i < t_n - 1 and value_list[0].lower() == 'for':
                R = 4
                end_i = i
            if R == 0 and i == start_i + 1 and value_list[0].lower() == 'that':
                R = 5
                start_i = i + 1

        if (flag1 or flag2) and not(kakko_flag) and (value_list[0].lower() in vb_words1 or value_list[0].lower() in vb_words2):
            if R == 0 and flag1:
                start_i += 1
                R = 4
            if R == 6 and flag1:
                start_i += 1
                R = 4
            if R == 0 and flag2:
                start_i += 1
                R = 5
            if flag1:
                end_i = i
            if flag2 and (R == 1 or R == 2 or R == 5):
                end_i = i

            if flag1:
                for j in range(start_i, end_i):
                    subtree = subtrees[j]
                    v_list = subtree.leaves()
                    if subtree.label() == 'CC' or subtree.label() == ',':
                        if temp_str:
                            temp = ' '.join(temp_str)
                            temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                            temp = temp.replace('-LRB- ', '(')
                            temp = temp.replace(' -RRB-', ')')
                            if temp != '':
                                I_SC_CC_extract.append(temp)
                        temp_str = []
                        continue
                    temp_str += v_list
            elif flag2:
                if R == 1 or R == 2 or R == 5:
                    for j in range(start_i, end_i):
                        subtree = subtrees[j]
                        v_list = subtree.leaves()
                        if subtree.label() == 'CC' or subtree.label() == ',':
                            if temp_str:
                                temp = ' '.join(temp_str)
                                temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                                temp = temp.replace('-LRB- ', '(')
                                temp = temp.replace(' -RRB-', ')')
                                if temp != '':
                                    I_SC_CC_extract.append(temp)
                            temp_str = []
                            continue
                        temp_str += v_list
                elif R == 3 or R == 4:
                    for j in range(start_i + 1, end_i):
                        subtree = subtrees[j]
                        v_list = subtree.leaves()
                        if subtree.label() == 'CC' or subtree.label() == ',':
                            if temp_str:
                                temp = ' '.join(temp_str)
                                temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                                temp = temp.replace('-LRB- ', '(')
                                temp = temp.replace(' -RRB-', ')')
                                if temp != '':
                                    I_SC_CC_extract.append(temp)
                            temp_str = []
                            continue
                        temp_str += v_list
            if temp_str:
                temp = ' '.join(temp_str)
                temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                temp = temp.replace('-LRB- ', '(')
                temp = temp.replace(' -RRB-', ')')
                if temp != '':
                    I_SC_CC_extract.append(temp)
                
            if value_list[0].lower() in vb_words1:
                flag1 = True
                flag2 = False
            else:
                flag1 = False
                flag2 = True
            R = 0
            temp_str = []
            start_i = i
            continue

    if R == 0 and flag1:
        start_i += 1
        R = 4
    if R == 6 and flag1:
        start_i += 1
        R = 4
    if R == 0 and flag2:
        start_i += 1
        R = 5

    if flag1:
        for i in range(start_i, t_n):
            subtree = subtrees[i]
            value_list = subtree.leaves()
            if subtree.label() == 'CC' or subtree.label() == ',':
                if temp_str:
                    temp = ' '.join(temp_str)
                    temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                    temp = temp.replace('-LRB- ', '(')
                    temp = temp.replace(' -RRB-', ')')
                    if temp != '':
                        I_SC_CC_extract.append(temp)
                temp_str = []
                continue
            temp_str += value_list
    elif flag2:
        if R == 1 or R == 2 or R == 5:
            for i in range(start_i, t_n):
                subtree = subtrees[i]
                value_list = subtree.leaves()
                if subtree.label() == 'CC' or subtree.label() == ',':
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            I_SC_CC_extract.append(temp)
                    temp_str = []
                    continue
                temp_str += value_list
        elif R == 3 or R == 4:
            for i in range(start_i + 1, end_i):
                subtree = subtrees[i]
                value_list = subtree.leaves()
                if subtree.label() == 'CC' or subtree.label() == ',':
                    if temp_str:
                        temp = ' '.join(temp_str)
                        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
                        temp = temp.replace('-LRB- ', '(')
                        temp = temp.replace(' -RRB-', ')')
                        if temp != '':
                            I_SC_CC_extract.append(temp)
                    temp_str = []
                    continue
                temp_str += value_list

    if temp_str:
        temp = ' '.join(temp_str)
        temp = temp.strip().strip(":").strip("'").strip('"').strip(',').strip('.').strip()
        temp = temp.replace('-LRB- ', '(')
        temp = temp.replace(' -RRB-', ')')
        if temp != '':
            I_SC_CC_extract.append(temp)
    
    if len(I_SC_CC_extract) < 2:
        I_SC_CC_extract = []

    return I_SC_CC_extract

def SC_SC_Iextract(temp_parse):
    SC_CC_I_extract = SC_SCextract(temp_parse)
    return SC_CC_I_extract

def type_get(res):
    extract_dic = {}
    sentence_list, type_dic, parse_dic = questionEN.question(res)
    all_type_list = []
    temp_parse = {
        'INST': {},
        'SELECT_CC': {},
        'SELECT_SC': {},
        'NE': {},
        'I&SC_CC': {}
    }
    for s_i in type_dic:
        d = type_dic[s_i]
        type_list = list(d.keys())
        all_type_list += type_list
        #R3
        if 'INST' in type_list and 'SELECT_CC' in type_list:
            if 'I&SC_CC' in extract_dic:
                extract_dic['I&SC_CC'][s_i] = I_SC_CCextract(parse_dic[s_i])
            else:
                extract_dic['I&SC_CC'] = {
                    s_i: I_SC_CCextract(parse_dic[s_i])
                }
        else:
            if 'INST' in type_list:
                temp_parse['INST'][s_i] = parse_dic[s_i]
            if 'SELECT_CC' in type_list:
                temp_parse['SELECT_CC'][s_i] = parse_dic[s_i]
        if 'SELECT_SC' in type_list:
            temp_parse['SELECT_SC'][s_i] = {
                "parse": parse_dic[s_i],
                "class": d["SELECT_SC"]["class"]
            }
        if 'NE' in type_list:
            temp_parse['NE'][s_i] = parse_dic[s_i]
    
    all_type_list = list(dict.fromkeys(all_type_list))
    if 1 < len(all_type_list):
        #R1
        if 'YESNO' in all_type_list:
            extract_dic['YESNO'] = {}
        #R2
        if 'SELECT_SC' in all_type_list and 'INST' in all_type_list:
            extract_dic['SC_SC&I'] = SC_SC_Iextract(temp_parse['SELECT_SC'])
        #R4
        if 'INST' in all_type_list:
            extract_dic['INST'] = INSTextract(temp_parse['INST'])
        #R5
        if 'SELECT_CC' in all_type_list:
            extract_dic['SELECT_CC'] = SC_CCextract(temp_parse['SELECT_CC'])
        if 'SELECT_SC' in all_type_list:
            extract_dic['SELECT_SC'] = SC_SCextract(temp_parse['SELECT_SC'])
    else:
        if 'YESNO' in all_type_list:
            extract_dic['YESNO'] = {}
        elif 'INST' in all_type_list:
            extract_dic['INST'] = INSTextract(temp_parse['INST'])
        elif 'SELECT_CC' in all_type_list:
            extract_dic['SELECT_CC'] = SC_CCextract(temp_parse['SELECT_CC'])
        elif 'SELECT_SC' in all_type_list:
            extract_dic['SELECT_SC'] = SC_SCextract(temp_parse['SELECT_SC'])
        elif 'NE' in all_type_list:
            extract_dic['NE'] = NEextract(temp_parse['NE'])
    
    return extract_dic
