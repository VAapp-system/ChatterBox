import json
import glob
import sys
import os
import copy
from collections import deque
import time
import traceback
import selenium
import requests
import http
import pathlib
sys.path.append('./module')
import Tree_VA as Tree
from Tree_VA import Node
from simulator import Crawler
import emoji_remove as ER
import data_check

args = sys.argv
locale = args[1]

def dialogue():
    if locale == 'EN':
        import question_typeEN
        path1 = './command_info_en.txt'
        path2 = './name_info_en.txt'
        path3 = './data/taxonomy_info_en.json'
        path4 = './data/namedEntity_info_en.json'
        path5 = './notOK_info_en.txt'
        path6 = './description_info_en.json'
        path7 = './data/wrongRes_info_en.json'
        path8 = './pageEx_info_en.json'
        path9 = './NEquestion_info_en.json'
        multiple_NE = ["digit"]
        include_NE = ["search_keyword", "word"]
    elif locale == 'JA':
        import question_typeJA
        path1 = './command_info_ja.txt'
        path2 = './name_info_ja.txt'
        path3 = './data/taxonomy_info_ja.json'
        path4 = './data/namedEntity_info_ja.json'
        path5 = './notOK_info_ja.txt'
        path6 = './description_info_ja.json'
        path7 = './data/wrongRes_info_ja.json'
        path8 = './pageEx_info_ja.json'
        path9 = './NEquestion_info_ja.json'
        path13 = './data/parse_rule.json'
        with open(path13, 'r', encoding='utf-8') as f13:
            parse_rule = json.load(f13)
        multiple_NE = ['時間', '駅', 'バス停', '難易度', '地名', '方言', 'マルバツ', '数字', '日にち']
        include_NE = ['キーワード', '単語', 'しりとり', '言葉', 'メモ']

    if not(os.path.exists(path5)):
        pathlib.Path(path5).touch()          
    with open(path1, 'r', encoding='utf-8') as f1:
        command = f1.readlines()
    with open(path2, 'r', encoding='utf-8') as f2:
        name = f2.readlines()
    with open(path3, 'r', encoding='utf-8') as f3:
        taxonomy = json.load(f3)
    with open(path4, 'r', encoding='utf-8') as f4:
        NE = json.load(f4)
    with open(path5, 'r', encoding='utf-8') as f5:
        not_OK_list = f5.readlines()
    with open(path6, 'r', encoding='utf-8') as f6:
        des_dic = json.load(f6)
    with open(path7, 'r', encoding='utf-8') as f7:
        WR = json.load(f7)
    with open(path8, 'r', encoding='utf-8') as f8:
        APP = json.load(f8)
    with open(path9, 'r', encoding='utf-8') as f9:
        OTHER_all_req = json.load(f9)

    LIMIT_COUNT = 10
    wrong_res = WR['fixed_form_text']
    
    files = glob.glob("./debug/debug*")
    start = len(files) + 1
    end = len(command) + 1

    try:
        crawler = Crawler()
        mlad = 'your_gmail'
        pw = 'your_password'
        crawler.setting(mlad, pw)
        if locale == 'EN':
            crawler.english()
        elif locale == 'JA':
            crawler.japanese()
            
        for i in range(start, end):
            try:
                #=====initialization process=====
                start_time = time.time()
                path10 = './logfile/log' + str(i) + '.txt'
                f10 = open(path10, 'w', encoding='utf-8')
                dir_path = 'debug' + str(i)
                if not(os.path.exists('./debug/' + dir_path)):
                    os.mkdir('./debug/' + dir_path)

                print('App Number: ' + str(i), file=f10)
                print('App Name: ' + name[i - 1].strip(), file=f10)
    
                turn = 1
                
                end_count = 0
                notCall_count = 0
                next_flag = False
                Node.Node_id = 1
                res_dic = {}
                
                root_candidate = {
                    "START": {
                        1: {
                            "req": command[i - 1].strip(),
                        }
                    }
                }
                root_node = Node(None, None, None, None, root_candidate, None)
                parent_node = root_node
                QEType = "START"
                Q_id = 1
                
                whole_example_req = des_dic[str(i)]

                app = APP[str(i)]
                page_url = app['PageUrl']
                before_storage = crawler.exit_check(page_url, locale)
                if not(before_storage):
                    print('No app', file=f10)
                    f10.close()
                    continue

                #=====initialization process end=====

                #=====start of dialogue=====
                d_count = 0
                while True:
                    d_count += 1
                    end_time = time.time()
                    if end_time - start_time > 3600:
                        print("Time out", file=f10)
                        turn = 4

                    print('\nstate' + str(turn), file=f10)
                    print('dialogue count: ' + str(d_count), file=f10)
                    print("node count: " + str(Node.Node_id), file=f10)
                    if turn == 1 or turn == 5:
                        try:
                            next_flag = crawler.next(locale)
                        except selenium.common.exceptions.ElementClickInterceptedException:
                            next_flag = crawler.other_next()
                        if not(next_flag):
                            print("Attempted recovery to initial state", file=f10)
                            if turn == 1:
                                next_flag = False
                                os.rmdir('./debug/' + dir_path)
                                f10.close()
                            else:
                                next_flag = True
                            not_OK_list.append(str(i - 1) + ' Attempted recovery to initial state\n')
                            break
                        warning_text = crawler.warning()
                        if "We're sorry, but something went wrong. Please try again." in warning_text:
                            print("Failure to recover to initial state", file=f10)
                            if turn == 1:
                                next_flag = False
                                os.rmdir('./debug/' + dir_path)
                                f10.close()
                            else:
                                next_flag = True
                            not_OK_list.append(str(i - 1) + ' Failure to recover to initial state\n')
                            break
                        QEType = "START"
                        Q_id = 1
                        req = command[i - 1].strip()
                    if turn == 3:
                        record_touple = req_list.popleft()
                        QEType = record_touple[0]
                        Q_id = record_touple[1]
                        if QEType == 'START':
                            if not(crawler.next(locale)):
                                print("Attempted recovery to initial state", file=f10)
                                not_OK_list.append(str(i) + ' Attempted recovery to initial state\n')
                                break
                        req = parent_node.candidate[QEType][Q_id]["req"]
                        present_node = parent_node.candidate[QEType][Q_id]["child"]
                        if not(req_list):
                            if not(present_node):
                                print('state 3 → 2', file=f10)
                                turn = 2
                            else:
                                print('state 3 → 7', file=f10)
                                turn = 7
                        else:
                            present_node = present_node[0]
                    elif turn == 4 or turn == 6:
                        QEType = "END"
                        Q_id = 1
                        req = 'cancel'

                    #=====request input process=====
                    req = ER.remove(req)
                    print('request: ' + req, file=f10)
                    crawler.input_req(req)
                    
                    r_start = time.time()
                    class_value, responses = crawler.output_res()
                    TO_flag = False
                    while class_value == 's7r-query-input-box md-input-has-placeholder md-actions-blue-theme flex md-input-has-value':
                        time.sleep(2)
                        if time.time() - r_start > 30:
                            TO_flag = True
                            break
                        class_value, responses = crawler.output_res()

                    if TO_flag:
                        print("Receive timeout", file=f10)
                        crawler.end()
                        not_OK_list.append(str(i) + ' Receive timeout\n')
                        break

                    receive_flag = False
                    kakko_count = 0
                    r_n = len(responses)
                    for kakko_i in reversed(range(r_n)):
                        e = responses[kakko_i]
                        t = e.get_attribute("textContent")
                        if t == '}':
                            kakko_count += 1
                        elif t == '{':
                            kakko_count -= 1
                            if kakko_count == 0:
                                receive_flag = True
                                break
                    if not(receive_flag):
                        print("Response reception failure", file=f10)
                        crawler.cancel()
                        not_OK_list.append(str(i) + ' Response reception failure\n')
                        break

                    responses = responses[kakko_i:]
                    text = ''
                    for e in responses:
                        t = e.get_attribute("textContent")
                        text += t.strip()
                    pattern_dic = json.loads(text)
                    pattern_dic['request'] = req
                    debug_path = './debug/' + dir_path + '/debug' + str(d_count) + '.json'
                    with open(debug_path, 'w', encoding='utf-8') as fd:
                        json.dump(pattern_dic, fd, indent=4, ensure_ascii=False)

                    res = pattern_dic['response']
                    if not(res) and 'visualResponse' in pattern_dic and 'visualElementsList' in pattern_dic['visualResponse']:
                        for p_dic in pattern_dic['visualResponse']['visualElementsList']:
                            if 'displayText' in p_dic:
                                res += p_dic['displayText']['content']

                    if res == "We're sorry, but something went wrong. Please try again.":
                        print("Cannot call app", file=f10)
                        new_node = Node(req, res, QEType, Q_id, {}, parent_node)
                        parent_node.visited((QEType, Q_id), new_node)
                        notCall_count += 1
                        if 10 < notCall_count:
                            crawler.cancel()
                            not_OK_list.append(str(i) + ' Cannot call App\n')
                            break
                        else:
                            req_list = deque()
                            flag = Tree.chain(root_node, req_list)
                            if flag:
                                print('state 2 → 3', file=f10)
                                parent_node = root_node
                                turn = 3
                                continue
                            else:
                                print('Next App', file=f10)
                                break

                    canvas_flag = False
                    if 'visualResponse' in pattern_dic and 'visualElementsList' in pattern_dic['visualResponse']:
                        for element in pattern_dic['visualResponse']['visualElementsList']:
                            if 'immersiveResponse' in element:
                                canvas_flag = True
                    if turn == 8 and not(canvas_flag):
                        print('canvas end', file=f10)
                        print('state 8 → 2', file=f10)
                        turn = 2
                    elif canvas_flag:
                        print("canvas flag", file=f10)
                        if turn != 3 and turn != 7:
                            print('state ' + str(turn) + ' → 8', file=f10)
                            turn = 8
                        canvas_texts, canvas_html, simu_html = crawler.canvas()

                        canvas_folder = 'canvas' + str(i)
                        if not(os.path.exists('./canvas/' + canvas_folder)):
                            os.mkdir('./canvas/' + canvas_folder)
                        canvas_path = './canvas/' + canvas_folder + '/source_canvas' + str(d_count) + '.html'
                        simu_path = './canvas/' + canvas_folder  + '/source_simulator' + str(d_count) + '.html'
                        with open(canvas_path, 'w', encoding='utf-8') as fc:
                            fc.write(canvas_html)
                        with open(simu_path, 'w', encoding='utf-8') as fs:
                            fs.write(simu_html)

                        if not(res):
                            res = '\n'.join(canvas_texts)
                        canvas_commands = []
                        for canvas_text in canvas_texts:
                            if len(canvas_text) < 20:
                                canvas_commands.append(canvas_text)

                    print("response: " + res, file=f10)

                    leave_flag = False
                    if not(pattern_dic['expectUserResponse']) or pattern_dic['agentName'] == "":
                        leave_flag = True
                        print('App Exited', file=f10)

                    wrong_flag = False
                    for wrong in wrong_res:
                        if wrong in res:
                            wrong_flag = True
                            print('Inappropriate request', file=f10)
                            break
                    if parent_node.res == res:
                        wrong_flag = True
                        print('Inappropriate request', file=f10)

                    if turn == 3:
                        if not(canvas_flag) and present_node.canvas:
                            if not(wrong_flag):
                                print('not canvas', file=f10)
                                print('new response', file=f10)
                                parent_node.candidate[QEType][Q_id]["loop_start"] = True
                        elif res != present_node.res:
                            if not(wrong_flag):
                                print('Different from past node response', file=f10)
                                parent_node.candidate[QEType][Q_id]["loop_start"] = True
                                same_node = Tree.loop_search(present_node, res, canvas_flag, [])
                                if same_node:
                                    parent_node.add((QEType, Q_id), same_node)
                                    S_QType = same_node.QType
                                    S_Q_id = same_node.Q_id
                                    same_node.parent.candidate[S_QType][S_Q_id]["loop_end"].append(same_node.idx)
                                    same_node.parent.candidate[S_QType][S_Q_id]["visit"] = True
                                    same_node.parent = parent_node
                                    same_node.req = req
                                    same_node.req_list.append(req)
                                    same_node.QType = QEType
                                    same_node.Q_id = Q_id
                                    parent_node.candidate[QEType][Q_id]["loop_count"] = 2
                                    parent_node = same_node
                                    req_list = deque()
                                    flag = Tree.chain(same_node, req_list)
                                    if flag:
                                        print('state 3 → 3', file=f10)
                                        turn = 3
                                    else:
                                        req_list = deque()
                                        flag = Tree.chain(root_node, req_list)
                                        if flag:
                                            print('state 3 → 6', file=f10)
                                            turn = 6
                                        else:
                                            print('state 3 → 4', file=f10)
                                            turn = 4
                                    continue
                                else:
                                    print('new response', file=f10)
                                    if canvas_flag:
                                        print('state 3 → 8', file=f10)
                                        turn = 8
                        else:
                            print("Same as previous response", file=f10)
                            parent_node = present_node
                            continue
                    
                    if turn == 7:
                        parent_node.candidate[QEType][Q_id]["loop_count"] += 1
                        child = parent_node.candidate[QEType][Q_id]['child']
                        for child_node in child:
                            if child_node.res == res and ((child_node.canvas and canvas_flag) or (not(child_node.canvas) and not(canvas_flag))):
                                present_node = child_node
                                parent_node = present_node
                                req_list = deque()
                                flag = Tree.chain(present_node, req_list)
                                if flag:
                                    print('state 7 → 3', file=f10)
                                    turn = 3
                                    break
                                else:
                                    req_list = deque()
                                    flag = Tree.chain(root_node, req_list)
                                    if flag:
                                        print('state 7 → 6', file=f10)
                                        turn = 6
                                    else:
                                        print('state 7 → 4', file=f10)
                                        turn = 4
                                    break
                        if turn != 7:
                            continue
                        else:
                            if not(wrong_flag):
                                for child_node in child:
                                    same_node = Tree.loop_search(child_node, res, canvas_flag, [])
                                    if same_node:
                                        parent_node.add((QEType, Q_id), same_node)
                                        S_QType = same_node.QType
                                        S_Q_id = same_node.Q_id
                                        same_node.parent.candidate[S_QType][S_Q_id]["loop_end"].append(same_node.idx)
                                        same_node.parent.candidate[S_QType][S_Q_id]["visit"] = True
                                        same_node.parent = parent_node
                                        same_node.req = req
                                        same_node.req_list.append(req)
                                        same_node.QType = QEType
                                        same_node.Q_id = Q_id
                                        parent_node = same_node
                                        req_list = deque()
                                        flag = Tree.chain(same_node, req_list)
                                        if flag:
                                            print('state 7 → 3', file=f10)
                                            turn = 3
                                        else:
                                            req_list = deque()
                                            flag = Tree.chain(root_node, req_list)
                                            if flag:
                                                print('state 7 → 6', file=f10)
                                                turn = 6
                                            else:
                                                print('state 7 → 4', file=f10)
                                                turn = 4
                                        break
                            if turn != 7:
                                continue
                            else:
                                print('new response', file=f10)
                                if canvas_flag:
                                    print('state 3 → 8', file=f10)
                                    turn = 8

                    option = []
                    for op_dic in pattern_dic['clientOperationList']:
                        if 'showSuggestionsPayLoad' in op_dic:
                            option += op_dic['showSuggestionsPayLoad']['textsList']
                            break

                    if 'visualResponse' in pattern_dic and 'visualElementsList' in pattern_dic['visualResponse']:
                        for element in pattern_dic['visualResponse']['visualElementsList']:
                            if 'listSelect' in element:
                                for item in element['listSelect']['itemsList']:
                                    option.append(item['title'])
                                
                    option = list(dict.fromkeys(option))
                    print("suggestions:", file=f10)
                    print(option, file=f10)

                    if turn == 4 and leave_flag:
                        print('Next App', file=f10)
                        new_node = Node(req, res, QEType, Q_id, {}, parent_node)
                        parent_node.visited((QEType, Q_id), new_node)
                        break
                    elif turn == 4 and not(leave_flag):
                        print('Exit is not possible', file=f10)
                        if end_count == 1:
                            print('Non-Exitable Apps', file=f10)
                            print('Next App', file=f10)
                            new_node = Node(req, res, QEType, Q_id, {}, parent_node)
                            parent_node.visited((QEType, Q_id), new_node)
                            break
                        else:
                            end_count += 1
                            new_node = Node(req, res, "NOT_END", 1, {}, parent_node)
                            parent_node.visited(("NOT_END", 1), new_node)
                            parent_node = new_node
                            continue

                    pre_flag = False
                    if res in res_dic:
                        print('same response', file=f10)
                        candidate = res_dic[res]
                        pre_flag = True
                        temp_canvas = {}
                        if turn != 8 and 'CANVAS' in candidate:
                            temp_canvas = candidate.pop('CANVAS')
                        if option:
                            if "OPTION" not in candidate:
                                candidate["OPTION"] = {}
                            for op in option:
                                flag = True
                                for idx in candidate["OPTION"]:
                                    Q_dic = candidate["OPTION"][idx]
                                    if Q_dic["req"] == op:
                                        flag = False
                                        break
                                if flag:
                                    new_idx = len(candidate["OPTION"]) + 1
                                    candidate["OPTION"][new_idx] = {
                                        "req": op
                                    }
                        if turn == 8:
                            if canvas_commands:
                                print(canvas_commands, file=f10)
                                if "CANVAS" not in candidate:
                                    candidate["CANVAS"] = {}
                                for cm in canvas_commands:
                                    flag = True
                                    for idx in candidate["CANVAS"]:
                                        Q_dic = candidate["CANVAS"][idx]
                                        if Q_dic["req"] == cm:
                                            flag = False
                                            break
                                    if flag:
                                        new_idx = len(candidate["CANVAS"]) + 1
                                        candidate["CANVAS"][new_idx] = {
                                            "req": cm
                                        }
                        res_dic[res] = copy.deepcopy(candidate)
                        if turn != 8 and temp_canvas:
                            res_dic[res]["CANVAS"] = temp_canvas
                    else:
                        print('No same response', file=f10)
                        candidate = {}
                        if option:
                            candidate["OPTION"] = {}
                            for idx in range(len(option)):
                                candidate["OPTION"][idx + 1] = {
                                    "req": option[idx]
                                }
                        if turn == 8:
                            if canvas_commands:
                                print(canvas_commands, file=f10)
                                candidate["CANVAS"] = {}
                                for idx in range(len(canvas_commands)):
                                    candidate["CANVAS"][idx + 1] = {
                                        "req": canvas_commands[idx]
                                    }

                    if turn == 1 or turn == 2 or turn == 3 or turn == 5 or turn == 7:
                        if (locale == 'EN' and 'is not linked yet. You can link' in res) or (locale == 'JA' and 'リンクできます' in res):
                            print('OAuth', file=f10)
                            new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                            parent_node.visited((QEType, Q_id), new_node)
                            parent_node = new_node
                            req_list = deque()
                            flag = Tree.chain(root_node, req_list)
                            if flag:
                                print('state ' + str(turn) + ' → 6', file=f10)
                                turn = 6
                            else:
                                print('state ' + str(turn) + ' → 4', file=f10)
                                turn = 4
                            continue

                    if turn == 1 and leave_flag:
                        print('state repeat', file=f10)
                        print('state 1 → 5', file=f10)
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.add((QEType, Q_id), new_node)
                        parent_node = root_node
                        turn = 5
                        fast_count = 1
                        continue

                    if turn == 5 and leave_flag:
                        fast_count += 1
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.add((QEType, Q_id), new_node)
                        parent_node = root_node
                        if fast_count == LIMIT_COUNT:
                            print('Next App', file=f10)
                            break
                        else:
                            continue
                    elif turn == 5 and not(leave_flag):
                        print('state 5 → 1', file=f10)
                        turn = 1

                    if turn == 2 and leave_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(root_node, req_list)
                        if flag:
                            print('state 2 → 3', file=f10)
                            parent_node = root_node
                            turn = 3
                            continue
                        else:
                            print('Next App', file=f10)
                            break

                    if turn == 3 and leave_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.candidate[QEType][Q_id]["loop_start"] = True
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(root_node, req_list)
                        if flag:
                            parent_node = root_node
                            turn = 3
                            continue
                        else:
                            print('Next App', file=f10)
                            break

                    if turn == 7 and leave_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(root_node, req_list)
                        if flag:
                            parent_node = root_node
                            print('state 7 → 3', file=f10)
                            turn = 3
                            continue
                        else:
                            print('Next App', file=f10)
                            break
                            
                    if turn == 6 and leave_flag:
                        print('state 6 → 3', file=f10)
                        end_count = 0
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        parent_node.visited((QEType, Q_id), new_node)
                        parent_node = root_node
                        turn = 3
                        continue
                    elif turn == 6 and not(leave_flag):
                        if end_count == 1:
                            print('Non-Exitable Apps', file=f10)
                            print('Next App', file=f10)
                            end_count = 0
                            new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                            parent_node.visited((QEType, Q_id), new_node)
                            break
                        else:
                            new_node = Node(req, res, "NOT_END", 1, candidate, parent_node)
                            parent_node.visited(("NOT_END", 1), new_node)
                            parent_node = new_node
                            end_count += 1
                            continue

                    if (turn == 2 or turn == 8) and wrong_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        if turn == 8:
                            new_node.canvas = True
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(parent_node, req_list)
                        if flag:
                            print('Return to parent node', file=f10)
                            record_touple = req_list.popleft()
                            QEType = record_touple[0]
                            Q_id = record_touple[1]
                            req = parent_node.candidate[QEType][Q_id]["req"]
                        else:
                            parent_node = new_node
                            req_list = deque()
                            flag = Tree.chain(root_node, req_list)
                            if flag:
                                print('state '+ str(turn) + ' → 6', file=f10)
                                turn = 6
                            else:
                                print('state '+ str(turn) + ' → 4', file=f10)
                                turn = 4
                        continue

                    if turn == 3 and wrong_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        if canvas_flag:
                            new_node.canvas = True
                        parent_node.candidate[QEType][Q_id]["loop_start"] = True
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(parent_node, req_list)
                        if flag:
                            print('Return to parent node', file=f10)
                        else:
                            parent_node = new_node
                            req_list = deque()
                            flag = Tree.chain(root_node, req_list)
                            if flag:
                                print('state 3 → 6', file=f10)
                                turn = 6
                            else:
                                print('state 3 → 4', file=f10)
                                turn = 4
                        continue

                    if turn == 7 and wrong_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        if canvas_flag:
                            new_node.canvas = True
                        parent_node.visited((QEType, Q_id), new_node)
                        req_list = deque()
                        flag = Tree.chain(parent_node, req_list)
                        if flag:
                            print('Return to parent node', file=f10)
                            print('state 7 → 3', file=f10)
                            turn = 3
                        else:
                            parent_node = new_node
                            req_list = deque()
                            flag = Tree.chain(root_node, req_list)
                            if flag:
                                print('state 7 → 6', file=f10)
                                turn = 6
                            else:
                                print('state 7 → 4', file=f10)
                                turn = 4
                        continue

                    #=====create a list of requests=====
                    if pre_flag:
                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        req_dic = new_node.candidate
                        print('reuse', file=f10)
                        print('requests:', file=f10)
                        print(req_dic, file=f10)
                        req = None
                        for QType in req_dic:
                            QType_dic = req_dic[QType]
                            for idx in QType_dic:
                                Q_dic = QType_dic[idx]
                                req = Q_dic["req"]
                                old_type = QEType
                                QEType = QType
                                old_id = Q_id
                                Q_id = idx
                                break
                            if req:
                                break
                    
                    else:
                        if locale == 'EN':
                            try:
                                extract_dic = question_typeEN.type_get(res)
                            except requests.exceptions.HTTPError:
                                extract_dic = {}
                        elif locale == 'JA':
                            extract_dic = question_typeJA.type_get(res, parse_rule)
                        consensus_query_type = list(extract_dic.keys())
                        if "YESNO" not in consensus_query_type:
                            if option:
                                if locale == 'EN':
                                    if 'Yes' in option or 'yes' in option or 'YES' in option or 'No' in option or 'no' in option or 'NO' in option:
                                        consensus_query_type.append('YESNO')
                                elif locale == 'JA':
                                    if 'はい' in option or 'いいえ' in option:
                                        consensus_query_type.append('YESNO')
                        print('Applicable question types:', file=f10)
                        print(consensus_query_type, file=f10)

                        if locale == 'EN':
                            if 'YESNO' in consensus_query_type:
                                candidate["YESNO"] = {
                                    1: {
                                        "req": "Yes"
                                    },
                                    2: {
                                        "req": "No"
                                    }
                                }
                            if 'INST' in consensus_query_type:
                                candidate["INST"] = {}
                                idx = 1
                                for str_id in extract_dic['INST']:
                                    candidate["INST"][idx] = {
                                        "req": extract_dic['INST'][str_id],
                                        "string_ID": str_id
                                    }
                                    idx += 1
                            if 'SELECT_CC' in consensus_query_type:
                                candidate["SELECT_CC"] = {}
                                idx = 1
                                for str_id in extract_dic['SELECT_CC']:
                                    for cc_req in extract_dic['SELECT_CC'][str_id]:
                                        candidate["SELECT_CC"][idx] = {
                                            "req": cc_req,
                                            "string_ID": str_id
                                        }
                                        idx += 1
                            if 'SELECT_SC' in consensus_query_type:
                                candidate["SELECT_SC"] = {}
                                idx = 1
                                for str_id in extract_dic['SELECT_SC']:
                                    for sc_req in extract_dic['SELECT_SC'][str_id]:
                                        candidate["SELECT_SC"][idx] = {
                                            "req": sc_req,
                                            "string_ID": str_id
                                        }
                                        idx += 1
                            if 'I&SC_CC' in consensus_query_type:
                                candidate["I&SC_CC"] = {}
                                idx = 1
                                for str_id in extract_dic['I&SC_CC']:
                                    for icc_req in extract_dic['I&SC_CC'][str_id]:
                                        candidate["I&SC_CC"][idx] = {
                                            "req": icc_req,
                                            "string_ID": str_id
                                        }
                                        idx += 1
                            if 'SC_SC&I' in consensus_query_type:
                                candidate["SC_SC&I"] = {}
                                idx = 1
                                for str_id in extract_dic['SC_SC&I']:
                                    for sci_req in extract_dic['SC_SC&I'][str_id]:
                                        candidate["SC_SC&I"][idx] = {
                                            "req": sci_req,
                                            "string_ID": str_id
                                        }
                                        idx += 1
                        elif locale == 'JA':
                            if 'YESNO' in consensus_query_type:
                                candidate["YESNO"] = {
                                    1: {
                                        "req": "はい"
                                    },
                                    2: {
                                        "req": "いいえ"
                                    }
                                }
                            if 'INST' in consensus_query_type:
                                candidate["INST"] = {}
                                idx = 1
                                inst_req_dic = {}
                                for type_id in extract_dic['INST']:
                                    for inst_req in extract_dic['INST'][type_id]:
                                        if inst_req in inst_req_dic:
                                            temp_idx = inst_req_dic[inst_req]
                                            candidate["INST"][temp_idx]['type_ID'].append(type_id)
                                        else:
                                            candidate["INST"][idx] = {
                                                "req": inst_req,
                                                "type_ID": [type_id]
                                            }
                                            inst_req_dic[inst_req] = idx
                                            idx += 1
                            if 'SELECT' in consensus_query_type:
                                candidate["SELECT"] = {}
                                idx = 1
                                select_req_dic = {}
                                for type_id in extract_dic['SELECT']:
                                    for select_req in extract_dic['SELECT'][type_id]:
                                        if select_req in select_req_dic:
                                            temp_idx = select_req_dic[select_req]
                                            candidate["SELECT"][temp_idx]['type_ID'].append(type_id)
                                        else:
                                            candidate["SELECT"][idx] = {
                                                "req": select_req,
                                                "type_ID": [type_id]
                                            }
                                            select_req_dic[select_req] = idx
                                            idx += 1
                            if 'LINK' in consensus_query_type:
                                candidate["LINK"] = {}
                                idx = 1
                                link_req_dic = {}
                                for type_id in extract_dic['LINK']:
                                    for link_req in extract_dic['LINK'][type_id]:
                                        if link_req in link_req_dic:
                                            temp_idx = link_req_dic[link_req]
                                            candidate["LINK"][temp_idx]['type_ID'].append(type_id)
                                        else:
                                            candidate["LINK"][idx] = {
                                                "req": link_req,
                                                "type_ID": [type_id]
                                            }
                                            link_req_dic[link_req] = idx
                                            idx += 1
                                            
                        if 'NE' in consensus_query_type:
                            candidate["NE"] = {}
                            consensus_name = []
                            for str_id in extract_dic['NE']:
                                que_res = extract_dic['NE'][str_id]
                                for nm in NE:
                                    if nm in que_res:
                                        flag = False
                                        for nam in consensus_name:
                                            if nm in nam:
                                                flag = True
                                                break
                                            if nam in nm:
                                                consensus_name.remove(nam)
                                        if not(flag):
                                            consensus_name.append(nm)
                            print('Applicable words:', file=f10)
                            print(consensus_name, file=f10)
                            consensus_name_type = []
                            for nm in consensus_name:
                                consensus_name_type += NE[nm]
                            consensus_name_type = list(set(consensus_name_type))
                            print('relevant eigenvalue classification:', file=f10)
                            print(consensus_name_type, file=f10)
                            if consensus_name_type:
                                idx = 1
                                for name_type in consensus_name_type:
                                    if name_type in multiple_NE:
                                        for name_typetype in taxonomy[name_type]:
                                            for ne_req in taxonomy[name_type][name_typetype]:
                                                candidate["NE"][idx] = {
                                                    "req": ne_req,
                                                    "NEType": name_typetype
                                                }
                                                idx += 1
                                    elif name_type in include_NE:
                                        for name_typeIn in taxonomy[name_type]:
                                            if name_typeIn in multiple_NE:
                                                for name_typetype in taxonomy[name_typeIn]:
                                                    for ne_req in taxonomy[name_typeIn][name_typetype]:
                                                        candidate["NE"][idx] = {
                                                            "req": ne_req,
                                                            "NEType": name_typetype
                                                        }
                                                        idx += 1
                                            else:
                                                for ne_req in taxonomy[name_typeIn]:
                                                    candidate["NE"][idx] = {
                                                        "req": ne_req,
                                                        "NEType": name_typeIn
                                                    }
                                                    idx += 1
                                    else:
                                        for ne_req in taxonomy[name_type]:
                                            candidate["NE"][idx] = {
                                                "req": ne_req,
                                                "NEType": name_type
                                            }
                                            idx += 1
                        
                        if whole_example_req:
                            candidate["EXAMPLE"] = {}
                            idx = 1
                            for e_req in whole_example_req:
                                candidate["EXAMPLE"][idx] = {
                                    "req": e_req
                                }
                                idx += 1
                        
                        if OTHER_all_req[str(i)]:
                            OTHER_req = OTHER_all_req[str(i)]
                            candidate["OTHER"] = {}
                            idx = 1
                            for o_req in OTHER_req:
                                candidate["OTHER"][idx] = {
                                    "req": o_req
                                }
                                idx += 1
                                
                        if res not in res_dic:
                            res_dic[res] = copy.deepcopy(candidate)

                        new_node = Node(req, res, QEType, Q_id, candidate, parent_node)
                        
                        req_dic = new_node.candidate
                        print('New', file=f10)
                        print('Request List:', file=f10)
                        print(req_dic, file=f10)
                        req = None
                        for QType in req_dic:
                            QType_dic = req_dic[QType]
                            for idx in QType_dic:
                                Q_dic = QType_dic[idx]
                                req = Q_dic["req"]
                                old_type = QEType
                                QEType = QType
                                old_id = Q_id
                                Q_id = idx
                                break
                            if req:
                                break
                    #=====End of request list creation=====

                    if turn == 8:
                        new_node.canvas = True

                    if req:
                        parent_node.add((old_type, old_id), new_node)
                        parent_node = new_node
                        if turn != 8:
                            print('state ' + str(turn) + ' → 2', file=f10)
                            turn = 2
                        else:
                            print('state ' + str(turn) + ' → 8', file=f10)
                            turn = 8
                        print('Next question type: ' + QEType, file=f10)
                        print('Next question ID: ' + str(Q_id), file=f10)
                    else:
                        print("No request", file=f10)
                        new_node.over = True
                        parent_node.visited((QEType, Q_id), new_node)
                        parent_node = new_node
                        req_list = deque()
                        flag = Tree.chain(root_node, req_list)
                        if flag:
                            print('state ' + str(turn) + ' → 6', file=f10)
                            turn = 6
                        else:
                            print('state ' + str(turn) + ' → 4', file=f10)
                            turn = 4

                if not(next_flag):
                    break

                print('dialogue end', file=f10)
                crawler.end()

                print('Logging completed', file=f10)
                f10.close()

                dir_path = 'tree_list' + str(i)
                if not(os.path.exists('./tree/' + dir_path)):
                    os.mkdir('./tree/' + dir_path)
                dic = {}
                Tree.save(root_node, dic)
                for layer in dic:
                    path11 = './tree/' + dir_path + '/tree' + str(layer) + '.json'
                    with open(path11, 'w', encoding='utf-8') as f11:
                        json.dump(dic[layer], f11, indent=4, ensure_ascii=False)

                after_storage = None
                try:
                    after_storage = crawler.get_storage(page_url, locale)
                except:
                    pass
                storage = {
                    'before': before_storage,
                    'after': after_storage
                }
                path14 = './user_storage/data' + str(i) + '.json'
                with open(path14, 'w', encoding='utf-8') as f14:
                    json.dump(storage, f14, indent=4, ensure_ascii=False)


            except KeyboardInterrupt:
                f10.close()
                crawler.cancel()
                break
            except:
                print(i, file=f10)
                print("Error occurred", file=f10)

                f10.close()

                path12 = './error/errorLog' + str(i) + '.txt'
                with open(path12, 'w', encoding='utf-8') as f12:
                    traceback.print_exc(file=f12)
                
                dir_path = 'tree_list' + str(i)
                if not(os.path.exists('./tree/' + dir_path)):
                    os.mkdir('./tree/' + dir_path)
                dic = {}
                Tree.save(root_node, dic)
                for layer in dic:
                    path11 = './tree/' + dir_path + '/tree' + str(layer) + '.json'
                    with open(path11, 'w', encoding='utf-8') as f11:
                        json.dump(dic[layer], f11, indent=4, ensure_ascii=False)

                after_storage = None
                try:
                    after_storage = crawler.get_storage(page_url, locale)
                except:
                    pass
                storage = {
                    'before': before_storage,
                    'after': after_storage
                }
                path14 = './user_storage/data' + str(i) + '.json'
                with open(path14, 'w', encoding='utf-8') as f14:
                    json.dump(storage, f14, indent=4, ensure_ascii=False)

                crawler.cancel()
                
            #=====data check=====
            check_dic = data_check.check(i, locale, name[i - 1].strip())
            path15 = './check/check' + str(i) + '.json'
            with open(path15, 'w', encoding='utf-8') as f15:
                json.dump(check_dic, f15, indent=4, ensure_ascii=False)

        try:
            crawler.quit()
        except http.client.RemoteDisconnected:
            pass
        except ConnectionRefusedError:
            pass
    except:
        traceback.print_exc()
        if crawler:
            try:
                crawler.quit()
            except http.client.RemoteDisconnected:
                pass
            except ConnectionRefusedError:
                pass
            
    with open(path5, 'w', encoding='utf-8') as f5:
        f5.writelines(not_OK_list)

if __name__ == '__main__':
    dialogue()