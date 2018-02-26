#!/usr/bin/env python3

import re

import attrdict
import flask

import qqmusic
import tts


app = flask.Flask(__name__)


@app.route('/dispatch', methods=['POST'])
def dispatch():
    try:
        payload = attrdict.AttrDict(flask.request.json)
        if 'message' in payload:
            message = payload.message

            m = re.match(r'(点歌|来一?首)(?P<query>.*)$', message)
            if m:
                query = m.group('query').strip()
                results = qqmusic.search(query)
                if not results:
                    return flask.jsonify(
                        reply='未发现“%s”相关歌曲' % query,
                        auto_escape=True,
                    )
                return flask.jsonify(
                    reply=[{
                        'type': 'music',
                        'data': {'type': 'qq', 'id': str(results[0].songid)},
                    }],
                    at_sender=False,
                )

            # The following features requires at-mentioning the bot
            at_self = '[CQ:at,qq=%s]' % payload.self_id
            if not at_self in message:
                return
            message = message.replace(at_self, '').strip()

            m = re.match(r'^骂(?P<name>.*)$', message)
            if m:
                name = m.group('name').strip()
                if name:
                    if '沙发' in name:
                        text = '沙发是莫寒的唯一甜粉。魔法一生推。'
                    else:
                        text = '辣鸡%s' % name
                    audio_url = flask.url_for('say', s=text, _external=True)
                    return flask.jsonify(
                        reply=[{
                            'type': 'record',
                            'data': {'file': audio_url},
                        }],
                        at_sender=False,
                    )
        else:
            return ''
    except Exception:
        return ''


# /say?s=魔法一生推
@app.route('/say')
def say():
    try:
        text = flask.request.args.get('s', '').strip()
        if not text:
            return ''
        content = tts.text_to_speech(text)
        return content
    except Exception:
        return ''


def main():
    app.run(port=9002, debug=True, threaded=True)


if __name__ == '__main__':
    main()
