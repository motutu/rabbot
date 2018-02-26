#!/usr/bin/env python3

# Text to speech.

import argparse
import string
import subprocess
import tempfile
import urllib.parse

import requests

import config


GOOGLE_TRANSLATE_REVPROXY = config.config.get('tts', 'google_translate_revproxy', fallback='')
GOOGLE_TRANSLATE = GOOGLE_TRANSLATE_REVPROXY or 'https://translate.google.com/'


def text_to_speech(text, *, lang='zh', separate_letters=True):
    try:
        if separate_letters:
            text = ''.join((ch + ' ') if ch in string.ascii_letters else ch for ch in text)
        r = requests.get(urllib.parse.urljoin(GOOGLE_TRANSLATE, 'translate_tts'),
                         params=dict(ie='UTF-8', tl=lang, client='tw-ob', q=text),
                         timeout=5)
        assert r.status_code == 200
        return r.content
    except Exception:
        return b''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+')
    args = parser.parse_args()

    with tempfile.NamedTemporaryFile() as fp:
        content = text_to_speech(' '.join(args.text))
        fp.write(content)
        fp.flush()
        subprocess.run(['mpv', fp.name])


if __name__ == '__main__':
    main()
