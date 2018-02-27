import urllib.parse

import attrdict
import requests


APIBASE = 'http://127.0.0.1:5700/'


def group_members(group_id):
    try:
        r = requests.get(urllib.parse.urljoin(APIBASE, '/get_group_member_list'),
                         params=dict(group_id=group_id), timeout=5)
        return attrdict.AttrDict(r.json()).data
    except Exception:
        return []
