import locale
import sys
import json
import stanza
from pyknp import Juman

args = sys.argv
locale = args[1]

if locale == 'EN':
    nlp = stanza.Pipeline('en')
    path1 = './pageEx_info_en.json'
    path2 = './NEquestion_info_en.json'
elif locale == 'JA':
    path1 = './pageEx_info_ja.json'
    path2 = './NEquestion_info_ja.json'
    
with open(path1, 'r', encoding='utf-8') as f1:
    apps = json.load(f1)

dic = {}
for k in apps:
    app = apps[k]
    description = app['Description']
    NE_list = {}
    if locale == 'EN':
        doc = nlp(description)
        for ent in doc.ents:
            if ent.type == 'DATE' or ent.type == 'ORDINAL' or ent.type == 'CARDINAL' or ent.type == 'TIME' or ent.type == 'LANGUAGE':
                continue
            req = "I want to know " + ent.text + '.'
            if not(req in NE_list):
                NE_list[req] = True
    elif locale == 'JA':
        jumanpp = Juman()
        description = description.strip()
        try:
            result = jumanpp.analysis(description)
            count = 1
            for mrph in result.mrph_list():
                if mrph.hinsi == '名詞':
                    if mrph.bunrui != '副詞的名詞' and mrph.bunrui != '時相名詞' and mrph.bunrui != 'サ変名詞' and mrph.bunrui != '数詞' and mrph.bunrui != '形式名詞':
                        req = mrph.midasi + 'を教えてください'
                        if not(req in NE_list):
                            NE_list[req] = True
        except:
            pass
    dic[k] = NE_list

with open(path2, 'w', encoding='utf-8') as f2:
    json.dump(dic, f2, indent=4, ensure_ascii=False)