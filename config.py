from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini", encoding='utf-8-sig')

TOKEN = config['token']['TOKEN']

BOSS_ID = config['chat_ids']['BOSS_ID']
LOZHKIN_ID = config['chat_ids']['LOZHKIN_ID']
PELICAN_TEAM_ID = config['chat_ids']['PELICAN_TEAM_ID']

BOT_URL = config['bot_url']['BOT_URL']

WORK_MAIL_LOGIN = config['mail']['WORK_MAIL_LOGIN']
WORK_MAIL_PASSWORD = config['mail']['WORK_MAIL_PASSWORD']
PROF_MAIL = config['mail']['PROF_MAIL']
ZHOZH_MAIL = config['mail']['ZHOZH_MAIL']