import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')

def remove(req):
    req = req.translate(non_bmp_map)
    return req