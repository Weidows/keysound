from config.global_config import global_config_obj
from config.sound_config import SoundConfig
import playsound
import random
import os
import json
import shutil
import webview
from config.window_config import window_config_obj

# 导出音效
def exportSound(name):
    file_types = ('Image Files (*.zip)', 'All files (*.*)')
    print(name)
    result = window_config_obj.window.create_file_dialog(webview.SAVE_DIALOG, allow_multiple=False, file_types=file_types,save_filename=name)
    if result:
      print(result)
      result = result.split('.')[0]
      shutil.make_archive(result, 'zip', f'./sounds/{name}')
      return True

# 导入音效
def importSound():
    file_types = ('Image Files (*.zip)', 'All files (*.*)')
    result = window_config_obj.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    if not result:
        return
    for i in result:
      print(i)
      i = str(i)
      # 创建文件夹
      name = i.split('\\')[-1].split('.')[0]
      os.mkdir(f'./sounds/{name}')
      shutil.unpack_archive(i, f'./sounds/{name}')
      return True

def play_sound(path: str):
    playsound.playsound(path)

# 播放音效
def playSound(key):
    if global_config_obj.keyboard_flag == False:
        return
    if global_config_obj.choose_sound == "":
        return
    # 读取index.json
    sound_config_obj = SoundConfig.read_from_file(global_config_obj.choose_sound)
    sound_folder = f"./sounds/{global_config_obj.choose_sound}/sounds"
    # 指定模式
    if sound_config_obj.mode == '指定':
        for sound in sound_config_obj.assigned_sounds:
            if sound['key'] == key:
                play_sound(f'{sound_folder}/{sound["sound"]}')
    # 重复模式
    elif sound_config_obj.mode == '重复':
        play_sound(f'{sound_folder}/{sound_config_obj.repeat_sound}')
    # 随机模式
    elif sound_config_obj.mode == '随机':
        soundsList = os.listdir(sound_folder)
        sound = random.choice(soundsList)
        print('随机播放音效：', sound)
        play_sound(f'{sound_folder}/{sound}')
        print('播放完毕------------')


# 获取音效列表
def getSoundList():
    soundsList = os.listdir('./sounds')
    return soundsList

# 获取音效信息
def getSoundInfo(soundName):
    # 读取index.json
    json_data = json.load(open(f'./sounds/{soundName}/index.json', 'r', encoding='utf-8'))
    json_data['soundsList'] = os.listdir(f'./sounds/{soundName}/sounds')
    return json_data

# 更新音效信息
def updateSoundInfo(soundInfo):
   name = soundInfo['name']
   # 读取index.json
   json_data = open(f'./sounds/{name}/index.json', 'w', encoding='utf-8')
   json.dump(soundInfo, json_data, ensure_ascii=False, indent=4)

# 新建音效信息
def newSoundInfo(name):
    print(name)
    temp = {
    "name": name,
    "mode": "",
    "repeat_sound": "",
    "assigned_sounds": []
    }
    # 创建文件夹
    os.mkdir(f'./sounds/{name}')
    os.mkdir(f'./sounds/{name}/sounds')
    # 写入index.json
    json_data = open(f'./sounds/{name}/index.json', 'w', encoding='utf-8')
    json.dump(temp, json_data, ensure_ascii=False, indent=4)

# 删除音效信息
def delSoundInfo(name):
    shutil.rmtree(f"./sounds/{name}")
    return True

# 添加音效文件
def addSoundFile(name):
    file_types = ('Image Files (*.mp3;*.wav)', 'All files (*.*)')
    result = window_config_obj.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    if result:
      print(result)
      for file in result:
        shutil.copy(file, f'./sounds/{name}/sounds/')
      return True

# 删除音效文件
def delSoundFile(name):
    os.remove(f'./sounds/{global_config_obj.choose_sound}/sounds/{name}')
    return True

# 选择音效
def selectSound(name):
    global_config_obj.choose_sound = name
    # 存入本地sound.ini
    global_config_obj.save()
