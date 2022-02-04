left_list = ['「', '『', '(', '<', '《', '[', '{', '【']
right_list = ['」', '』', ')', '>', '》', ']', '}', '】']

def split(res):
    res = res.replace('...', '')
    res = res.replace('はなんですか', 'は何ですか')
    res = res.replace('いずれかから', 'いずれか、から')
    n = len(res)
    flag = True
    index_list = []
    start = 0
    sentence_list = []
    for i in range(n):
        if res[i] in left_list:
            index = left_list.index(res[i])
            index_list.append(index)
            flag = False
            continue
        if not(flag) and res[i] == right_list[index_list[-1]]:
            index_list.pop()
            if len(index_list) == 0:
                flag = True
            continue
        if flag and (res[i] == '\n' or res[i] == '。' or res[i] == '？' or res[i] == '！' or res[i] == '?' or res[i] == '!' or res[i] == '…'):
            sentence = res[start:i]
            sentence = sentence.strip()
            sentence = sentence.replace(" ", "")
            start = i + 1
            if sentence != '':
                sentence_list.append(sentence)
    if start == 0 or start != n:
        sentence = res[start:n]
        sentence = sentence.strip()
        sentence = sentence.replace(" ", "")
        if sentence != '':
            sentence_list.append(sentence)
    
    return sentence_list
