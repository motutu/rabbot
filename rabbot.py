#!/usr/bin/env python3

import re

import attrdict
import flask

import qqmusic


app = flask.Flask(__name__)


@app.route('/dispatch', methods=['POST'])
def dispatch():
    try:
        payload = attrdict.AttrDict(flask.request.json)
        if 'message' in payload:
            m = re.match(r'(点歌|来一?首)(?P<query>.*)$', payload.message)
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
        else:
            return ''
    except Exception:
        return ''


def main():
    app.run(port=9002, debug=True, threaded=True)


if __name__ == '__main__':
    main()
