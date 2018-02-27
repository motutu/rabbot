# Config file structure:
#
# - bot.nickname
# - tts.google_translate_proxy

import configparser
import pathlib


HERE = pathlib.Path(__file__).resolve().parent
CONFIG_FILE = HERE / 'config.ini'
config = configparser.ConfigParser()
config.read([CONFIG_FILE.as_posix()])
