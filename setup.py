from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import yaml


def get_error_info(file, error):
    backslash = '\\'
    error_len = len(str(error))
    otstup = '-' * 35 if error_len > 35 else '-' * error_len
    return f"{otstup}\nМодуль {file.split(backslash)[-1]}\nОшибка: {error}\n{otstup}"


class CreatingChannel:
    def __init__(self, name, l_id, c_id, u_l):
        self.voice_name = name
        self.lobby_id = l_id
        self.categ_id = c_id
        self.user_limit = u_l


with open("config.yaml", "r", encoding='UTF-8') as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    channels_config = config['channels']
    URI = config['mongodb_link']


CLIENT = MongoClient(URI, server_api=ServerApi('1'))
DB = CLIENT["dota_bot"]
COLLECTION = DB["voice_channels"]

CHANNELS_CFGS = [CreatingChannel(
    channels_config.get(x)["voice_name"],
    channels_config.get(x)["lobby_id"],
    channels_config.get(x)["categ_id"],
    channels_config.get(x)["user_limit"]
)
                 for x in channels_config]

SEARCH_CHANNEL_ID = config['search_channel_id']


COLLECTION.delete_many({})
