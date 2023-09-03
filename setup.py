from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import yaml
from os import getenv
from dotenv import load_dotenv


def get_error_info(file, error):
    backslash = '\\'
    error_len = len(str(error))
    otstup = '-' * 35 if error_len > 35 else '-' * error_len
    return f"{otstup}\nМодуль {file.split(backslash)[-1]}\nОшибка: {error}\n{otstup}"


class LiveChannel:
    def __init__(self, name, l_id, c_id, u_l):
        self.voice_name = name
        self.lobby_id = l_id
        self.categ_id = c_id
        self.user_limit = u_l


with open("config.yaml", "r", encoding='UTF-8') as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

load_dotenv()
DB_URL = getenv('MONGODB_URL')
CLIENT = MongoClient(DB_URL, server_api=ServerApi('1'))
DB = CLIENT[config["db_name"]]
COLLECTION = DB[config["coll_name"]]

chnls_cfg = config['channels']
LIVE_CHANNELS = [
    LiveChannel(
        chnls_cfg.get(chnl)["voice_name"],
        chnls_cfg.get(chnl)["lobby_id"],
        chnls_cfg.get(chnl)["categ_id"],
        chnls_cfg.get(chnl)["user_limit"]
    )

    for chnl in chnls_cfg
]

SEARCH_CHANNEL_ID = config['search_channel_id']
