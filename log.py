import json
import logging
import logging.handlers
import pathlib


HERE = pathlib.Path(__file__).resolve().parent
LOGDIR = HERE / 'logs'
CQHTTP_LOGDIR = LOGDIR / 'cqhttp'
CQHTTP_LOGDIR.mkdir(exist_ok=True, parents=True)
CQHTTP_GROUPS_LOGDIR = CQHTTP_LOGDIR / 'groups'
CQHTTP_USERS_LOGDIR = CQHTTP_LOGDIR / 'users'
CQHTTP_GROUPS_LOGDIR.mkdir(exist_ok=True)
CQHTTP_USERS_LOGDIR.mkdir(exist_ok=True)


def get_cqhttp_event_logger(*, group_id=None, user_id=None):
    if group_id:
        name = 'cqhttp-group-%s' % group_id
        logfile = CQHTTP_GROUPS_LOGDIR / ('%s.json' % group_id)
    elif user_id:
        name = 'cqhttp-user-%s' % user_id
        logfile = CQHTTP_USERS_LOGDIR / ('%s.json' % user_id)
    else:
        name = 'cqhttp-other'
        logfile = CQHTTP_LOGDIR / 'other.json'

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # No rollover for now.
        fh = logging.handlers.RotatingFileHandler(logfile, encoding='utf-8')
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

    return logger


def log_cqhttp_event(payload):
    logger = get_cqhttp_event_logger(group_id=payload.get('group_id'),
                                     user_id=payload.get('user_id'))
    logger.info(json.dumps(payload, ensure_ascii=False, sort_keys=True))
