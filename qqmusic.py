#!/usr/bin/env python3

import argparse
import json
import re

import attrdict
import requests


def search(query):
    try:
        r = requests.get('https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp',
                         params=dict(w=query), timeout=5)
        # Handle JSONP
        m = re.match(r'^callback\((?P<json>.*)\)$', r.text)
        if not m:
            return []
        ro = attrdict.AttrDict(json.loads(m.group('json')))
        return ro.data.song.list
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='+')
    args = parser.parse_args()

    results = search(' '.join(args.query))
    for result in results:
        singers = ' & '.join(s.name for s in result.singer)
        print('%s《%s》%s' % (singers, result.songname, result.albumname))
        print('https://y.qq.com/n/yqq/song/%s.html' % result.songmid)
        print()


if __name__ == '__main__':
    main()
