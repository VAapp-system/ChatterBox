from nltk.tokenize import sent_tokenize

keisyo = ['Prof', 'Mr', 'Ms', 'Miss', 'Dr', 'Esq', 'e', 'g']

def split(res):
    sentence_list = sent_tokenize(res)
    not_ok_sentence_list = {}
    s_n = len(sentence_list)
    for i in range(s_n):
        sentence = sentence_list[i]
        n = len(sentence)
        for j in range(n):
            char = sentence[j]
            if char == '.' and j < n - 1 and sentence[j + 1] != ' ':
                temp = ''
                for k in reversed(range(j)):
                    if sentence[k] == ' ':
                        break
                    temp += sentence[k]
                temp = temp[::-1]
                if temp not in keisyo:
                    if i in not_ok_sentence_list:
                        not_ok_sentence_list[i].append(j)
                    else:
                        not_ok_sentence_list[i] = [j]
    new_sentence_list = []
    for i in range(s_n):
        sentence = sentence_list[i]
        if i in not_ok_sentence_list:
            index_list = not_ok_sentence_list[i]
            start_i = 0
            for idx in index_list:
                new_sentence_list.append(sentence[start_i:idx + 1])
                start_i = idx + 1
            new_sentence_list.append(sentence[start_i:])
        else:
            new_sentence_list.append(sentence)

    sentence_list = new_sentence_list
    return sentence_list
