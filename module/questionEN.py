from nltk.parse import CoreNLPParser
from collections import deque
import sentenceEN
from nltk.tree import ParentedTree

parser = CoreNLPParser(url='Stanford CoreNLP server URL')

w_tag = ['WHADJP', 'WHADVP', 'WHNP', 'WHPP', 'WDT', 'WP', 'WP$', 'WRB', 'WP-S']
i_tag = ['VB', 'VBG', 'VBP']
vb_words = ['say', 'ask', 'saying', 'asking']
wh_words = ['what', 'when', 'where', 'which', 'who', 'whom', 'whose', 'why', 'how']

def question(res):
    type_dic = {}
    parse_dic = {}
    sentence_list = sentenceEN.split(res)
    s_n = len(sentence_list)
    for s_i in range(s_n):
        type_dic[s_i] = {}
        sentence = sentence_list[s_i]
        if 'Now, ready to make your new ' in sentence:
            type_dic[s_i]['YESNO'] = True
        parse = next(parser.raw_parse(sentence))
        parse_dic[s_i] = parse
        queue = deque()
        queue.append(parse)
        while queue:
            n = len(queue)
            tag_list = []
            for i in range(n):
                tree = queue.popleft()
                for p in tree:
                    if type(p) is not str:
                        queue.append(p)
                        tag = p.label()
                        if tag == 'SQ':
                            flag = False
                            if 0 < len(tag_list):
                                before_tag = tag_list[-1]
                                if before_tag not in w_tag:
                                    flag = True
                            else:
                                flag = True
                            if flag:
                                for subtree in p.subtrees(lambda p: p.height() == 2):
                                    if subtree.label() == 'CC':
                                        flag = False
                                        break
                                if flag:
                                    if 'YESNO' not in type_dic[s_i]:
                                        type_dic[s_i]['YESNO'] = True
                        if tag in w_tag:
                            value_list = p.leaves()
                            for value in value_list:
                                if value.lower() in wh_words:
                                    if 'NE' not in type_dic[s_i]:
                                        type_dic[s_i]['NE'] = True

                        tag_list.append(tag)

        parse = ParentedTree.convert(parse)
        for subtree in parse.subtrees(lambda parse: parse.height() == 2):
            if subtree.label() in i_tag:
                value_list = subtree.leaves()
                if value_list[0].lower() in vb_words:
                    parent = subtree
                    while parent.label() != 'S' and parent.label() != 'SBAR' and parent.label() != 'SBARQ' and parent.label() != 'SINV' and parent.label() != 'SQ' and parent.label() != 'ROOT':
                        parent = parent.parent()
                    prp_flag = True
                    for subtree in parent:
                        if subtree.label() == 'NP':
                            for subsubtree in subtree.subtrees(lambda parse: parse.height() == 2):
                                if subsubtree.label() == 'PRP' and (subsubtree.leaves()[0].lower() == 'i' or subsubtree.leaves()[0].lower() == 'me'):
                                    prp_flag = False
                                    break
                        if not(prp_flag):
                            break
                    if prp_flag:
                        if 'INST' not in type_dic[s_i]:
                            type_dic[s_i]['INST'] = True
        
        for subtree in parse.subtrees(lambda parse: parse.height() == 2):
            if subtree.label() == 'CC':
                value_list = subtree.leaves()
                if value_list[0].lower() == 'or' or value_list[0].lower() == 'and':
                    if 'SELECT_CC' not in type_dic[s_i]:
                        type_dic[s_i]['SELECT_CC'] = True

        numbers = []
        single_chars = []
        for subtree in parse.subtrees(lambda parse: parse.height() == 2):
            value_list = subtree.leaves()
            if value_list[0].isdecimal():
                numbers.append(int(value_list[0]))
            if len(value_list[0]) == 1 and value_list[0].isalpha():
                single_chars.append(value_list[0])
        if 1 < len(numbers) and numbers[0] == 1 and len(list(range(numbers[0], numbers[-1] + 1))) == len(numbers):
            if 'SELECT_SC' not in type_dic[s_i]:
                type_dic[s_i]['SELECT_SC'] = {
                    "judge": True,
                    "class": 'a'
                }
        if 1 < len(single_chars) and (single_chars[0] == 'a' or single_chars[0] == 'A') and len(list(range(ord(single_chars[0]), ord(single_chars[-1]) + 1))) == len(single_chars):
            if 'SELECT_SC' not in type_dic[s_i]:
                type_dic[s_i]['SELECT_SC'] = {
                    "judge": True,
                    "class": 'b'
                }
                        
    return sentence_list, type_dic, parse_dic
