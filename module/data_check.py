import json
import glob

def get_key(dic, key_list):
    if isinstance(dic, dict):
        key_list += list(dic.keys())
        for k in dic:
            get_key(dic[k], key_list)
    elif isinstance(dic, list):
        for item in dic:
            get_key(item, key_list)

def get_url_canvas(dic, URL_list, canvas_list):
    if isinstance(dic, dict):
        keys = list(dic.keys())
        for key in keys:
            if key == 'openUrlAction':
                URL_list.append(dic[key]['url'])
            if key == 'immersiveResponse':
                canvas_list.append(dic[key])
            else:
                get_url_canvas(dic[key], URL_list, canvas_list)
    elif isinstance(dic, list):
        for item in dic:
            get_url_canvas(item, URL_list, canvas_list)

def check_tracking(responses, locale):
    class_list = []
    Helpers_list = []
    trackingQue_list = {}
    for res in responses:
        if locale == 'JP':
            if 'リンクできます' in res:
                class_list.append(1)
                if '1' in trackingQue_list:
                    trackingQue_list['OAuth'].append(res)
                else:
                    trackingQue_list['OAuth'] = [res]
            elif '氏名、メールアドレス、プロフィール写真' in res:
                class_list.append(2)
                if '2' in trackingQue_list:
                    trackingQue_list['Google Sign-In'].append(res)
                else:
                    trackingQue_list['Google Sign-In'] = [res]
            elif 'Googleの情報を利用してもよろしいでしょうか' in res or 'Googleの情報を利用してもよろしいですか' in res:
                if '3' in trackingQue_list:
                    trackingQue_list['Helper Intent'].append(res)
                else:
                    trackingQue_list['Helper Intent'] = [res]
                class_list.append(3)
                if '現在地' in res:
                    Helpers_list.append('current location')
                elif '名前' in res:
                    Helpers_list.append('name')
        elif locale == 'EN':
            if 'is not linked yet. You can link' in res:
                class_list.append(1)
                if '1' in trackingQue_list:
                    trackingQue_list['OAuth'].append(res)
                else:
                    trackingQue_list['OAuth'] = [res]
            elif 'your name, email address, and profile picture' in res:
                class_list.append(2)
                if '2' in trackingQue_list:
                    trackingQue_list['Google Sign-In'].append(res)
                else:
                    trackingQue_list['Google Sign-In'] = [res]
            elif ('I\'ll just need to get your' in res and 'from Google' in res) or ("I just need to check" in res and 'Can I get that from Google?' in res):
                class_list.append(3)
                if '3' in trackingQue_list:
                    trackingQue_list['Helper Intent'].append(res)
                else:
                    trackingQue_list['Helper Intent'] = [res]
                if 'location' in res:
                    Helpers_list.append('current location')
                elif 'your name' in res:
                    Helpers_list.append('name')
    class_list = list(set(class_list))
    Helpers_list = list(set(Helpers_list))
    dic = {
        "tracking_res": trackingQue_list,
        "Helper_Intent_type": Helpers_list
    }
    return dic
    
def check_storage(storage_dic, locale, name):
    after = storage_dic['after']
    if not(after) or after == 'None':
        return {}
    elif (locale == 'JP' and after != ("ユーザー ストレージに保存されている " + name + " のデータはありません")) or (locale == 'EN' and after != (name + " hasn't stored anything in User Storage")):
        try:
            storage = json.loads(after)
        except:
            storage = after
    else:
        return {}
    key_list = []
    if isinstance(storage, str):
        key_list.append('userId')
    else:
        get_key(storage, key_list)
    key_list = list(dict.fromkeys(key_list))
    dic = {
        'storage': storage,
        'key_list': key_list
    }
    return dic

def check_userId(dic):
    key_list = dic['key_list']
    id_list = []
    for key in key_list:
        if 'id' in key.lower():
            id_list.append(key)
    return id_list    

def check(app_id, locale, name):
    debug_path = './debug/debug' + str(app_id) + '/debug*.json'
    debug_files = glob.glob(debug_path)
    responses = []
    URL_list = []
    canvas_list = []
    for debug_file in debug_files:
        with open(debug_file, 'r', encoding='utf-8') as f:
            dic = json.load(f)
        if dic['response'] != '':
            responses.append(dic['response'])
        else:
            if 'visualResponse' in dic and 'visualElementsList' in dic['visualResponse']:
                res = ''
                for p_dic in dic['visualResponse']['visualElementsList']:
                    if 'displayText' in p_dic:
                        res += p_dic['displayText']['content']
                res = res.strip()
                if res != '':
                    responses.append(res)
        get_url_canvas(dic, URL_list, canvas_list)
    responses = list(dict.fromkeys(responses))
    storage_path = './user_storage/data' + str(app_id) + '.json'
    with open(storage_path, 'r', encoding='utf-8') as fs:
        storage_dic = json.load(fs)
    check_dic = {}
    check_dic["Tracking"] = check_tracking(responses, locale)
    check_dic["UserStorage"] = check_storage(storage_dic, locale, name)
    if check_dic["UserStorage"]:
        check_dic["UserID"] = check_userId(check_dic["UserStorage"])
    else:
        check_dic["UserID"] = []
    check_dic["URL"] = list(set(URL_list))
    check_dic["InteractiveCanvas"] = canvas_list
    return check_dic
