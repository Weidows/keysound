import json
import os

class SoundConfig:
    def __init__(self) -> None:
        self.name = ""
        self.mode = ""
        self.repeat_sound = ""
        self.assigned_sounds = []
        self.soundsList = []

    @staticmethod
    def read_from_file(filename: str):
        config = SoundConfig()
        json_data = json.load(open(f'./sounds/{filename}/index.json', 'r', encoding='utf-8'))
        # config.name = json_data["name"]
        # config.mode = json_data["mode"]
        # config.repeat_sound = json_data["repeat_sound"]
        # config.assigned_sounds = json_data["assigned_sounds"]
        # config.soundsList = json_data["soundsList"]
        config.__dict__ = json_data
        return config

    @staticmethod
    def create_sound(name: str):
        print(name)
        config = SoundConfig()
        config.name = name
        # 创建文件夹
        os.mkdir(f'./sounds/{name}')
        os.mkdir(f'./sounds/{name}/sounds')
        # 写入index.json
        with open(f'./sounds/{name}/index.json', 'w', encoding='utf-8') as f:
            json.dump(config.__dict__, f, ensure_ascii=False, indent=4)

