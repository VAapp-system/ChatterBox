from collections import deque

class Node:
    Node_id = 1
    def __init__(self, req, res, QType, Q_id, candidate, parent):
        self.req = req
        self.res = res
        self.QType = QType
        self.Q_id = Q_id
        self.parent = parent
        candidate = candidate
        for QType in candidate:
            QType_dic = candidate[QType]
            for Q_id in QType_dic:
                Q_dic = QType_dic[Q_id]
                Q_dic["visit"] = False
                Q_dic["child"] = []
                Q_dic["loop_start"] = False
                Q_dic["loop_end"] = []
                Q_dic["loop_count"] = 1
        self.candidate = candidate
        self.over = False
        self.canvas = False
        self.idx = Node.Node_id
        self.req_list = [req]
        Node.Node_id += 1

    def add(self, Q_touple, node):
        QType = Q_touple[0]
        Q_id = Q_touple[1]
        candidate = self.candidate
        Q_dic = candidate[QType][Q_id]
        Q_dic["child"].append(node)

    def visited(self, Q_touple, node):
        QType = Q_touple[0]
        Q_id = Q_touple[1]
        candidate = self.candidate
        if QType == 'END' or QType == 'NOT_END':
            candidate[QType] = {
                "1": {
                    "req": "cancel",
                    "visit": True,
                    "child": [node],
                    "loop_start": False,
                    "loop_end": [],
                    "loop_count": 1
                }
            }
        else:
            Q_dic = candidate[QType][Q_id]
            Q_dic["visit"] = True
            Q_dic["child"].append(node)

def save(node, dic):
    queue = deque()
    queue.append(node)
    idx_list = []
    layer = 1
    while queue:
        n = len(queue)
        jf = {}
        for i in range(n):
            node = queue.popleft()
            idx = node.idx
            idx_list.append(idx)
            jf[idx] = {
                "req": node.req,
                "res": node.res,
                "QType": node.QType,
                "Q_id": node.Q_id,
                "over": node.over,
                "canvas": node.canvas,
                "id": node.idx,
                "req_list": node.req_list,
            }
            candidate = node.candidate
            for QType in candidate:
                QType_dic = candidate[QType]
                for Q_id in QType_dic:
                    Q_dic = QType_dic[Q_id]
                    child = Q_dic["child"]
                    temp_child = []
                    if child:
                        for child_node in child:
                            if type(child_node) is int:
                                temp_child.append(child_node)
                                continue
                            if child_node.idx in idx_list:
                                temp_child.append(child_node.idx)
                                continue
                            if child_node.idx in Q_dic["loop_end"]:
                                temp_child.append(child_node.idx)
                                continue
                            queue.append(child_node)
                            temp_child.append(child_node.idx)
                    Q_dic["child"] = temp_child
            jf[idx]["candidates"] = candidate
            if node.parent:
                jf[idx]["parent"] = node.parent.idx
            else:
                jf[idx]["parent"] = None
        idx_list = list(dict.fromkeys(idx_list))
        dic[layer] = jf
        layer += 1

def loop_search(node, res, canvas_flag, index_list):
    if not(node):
        return False
    if node.res == res and ((node.canvas and canvas_flag) or (not(node.canvas) and not(canvas_flag))):
        return node
    candidate = node.candidate
    for QType in candidate:
        if QType == 'END' or QType == 'NOT_END':
            continue
        QType_dic = candidate[QType]
        for Q_id in QType_dic:
            Q_dic = QType_dic[Q_id]
            child = Q_dic["child"]
            for child_node in child:
                if child_node.idx in index_list:
                    continue
                if child_node.idx in Q_dic["loop_end"]:
                    continue
                index_list.append(child_node.idx)
                coin_node = loop_search(child_node, res, canvas_flag, index_list)
                if coin_node:
                    return coin_node
    return False
    
def chain(node, req_list):
    if not(node.candidate):
        node.over = True
        return False
    if node.over:
        return False
    candidate = node.candidate
    for QType in candidate:
        QType_dic = candidate[QType]
        for Q_id in QType_dic:
            Q_dic = QType_dic[Q_id]
            if Q_dic["visit"]:
                continue
            elif 1000 <= len(Q_dic["child"]) or 1000 <= Q_dic["loop_count"]:
                Q_dic["visit"] = True
                continue
            req_list.append((QType, Q_id))
            if Q_dic["loop_start"]:
                return True
            if not(Q_dic["child"]):
                return True
            else:
                child_node = Q_dic["child"][0]
                flag = chain(child_node, req_list)
                if flag:
                    return True
            Q_dic["visit"] = True
            req_list.pop()
    node.over = True
    return False
