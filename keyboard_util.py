import keyboard
from utils.keyfilter import keyfilter
import threading
from window_config import window_config_obj
from sound_util import playSound

keyList = {}

# 启动键盘监听线程
def on_key_event():
    keyboard.hook(callback)
    keyboard.wait()

# 监听键盘事件
def callback(event):
    event.name = event.name[0].upper() + event.name[1:]
    event.name = keyfilter(event.name)
    if event.name not in keyList:
        keyList[event.name] = False
    if event.event_type == 'down' and keyList[event.name] == False:
        print(event.name,' is down')
        keyList[event.name] = True
        threading.Thread(target=downKey, args=(event.name,)).start()
        threading.Thread(target=playSound, args=(event.name,)).start()
    elif event.event_type == 'up' and keyList[event.name] == True:
        print(event.name, ' is up')
        keyList[event.name] = False
        threading.Thread(target=upKey, args=(event.name,)).start()

# 按键按下
def downKey(key):
    if window_config_obj.window_flag:
        window_config_obj.window.evaluate_js(f'window.downKEY("{key}")')

# 按键抬起
def upKey(key):
    if window_config_obj.window_flag:
        window_config_obj.window.evaluate_js(f'window.upKEY("{key}")')
