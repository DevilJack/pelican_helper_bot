from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini", encoding='utf-8-sig')

TOKEN = config['token']['TOKEN']

BOSS_ID = config['chat_ids']['BOSS_ID']
LOZHKIN_ID = config['chat_ids']['LOZHKIN_ID']
PELICAN_TEAM_ID = config['chat_ids']['PELICAN_TEAM_ID']

BOT_URL = config['bot_url']['BOT_URL']