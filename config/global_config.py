import os
import json
class GlobalConfig:
    def __init__(self) -> None:
        self.keyboard_flag = True
        self.mouse_flag = False
        self.choose_sound = ""
        self.auto_run = False
        # 查看是否有config.json
        if not os.path.exists(f'config.json'):
            # 没有就创建
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.__dict__, f, ensure_ascii=False, indent=2)
                print('创建config.json')
        # 查看是否有sound.ini
        if not os.path.exists('sound.ini'):
            # 没有就创建
            with open('sound.ini', 'w', encoding='utf-8') as f:
                f.write('')
                print('创建sound.ini')
        # 查看是否有sounds文件夹
        if not os.path.exists('sounds'):
            # 没有就创建
            os.mkdir('sounds')
            print('创建sounds文件夹')

    def reload(self):
        with open('config.json', 'r', encoding='utf-8') as f:
            self.__dict__.update(json.loads(f.read()))

    def save(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

global_config_obj = GlobalConfig()
