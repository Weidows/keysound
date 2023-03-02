# -*- coding:utf-8 _*-
import webview
import keyboard
import pynput
import threading
import os
import json
import playsound
import pystray
from PIL import Image
from pystray import MenuItem
import shutil
from utils.keyfilter import keyfilter
import winreg

class KeySound:
  def __init__(self) -> None:
    self.initConfig()
    self.sotp_mouse = False # True:停止鼠标监听
    self.window = None
    self.window_flag = False
    self.SELECT_SOUND = ""
    self.keyList = {}
    self.keyboard_flag = False
    self.mouse_flag = False
    self.auto_run = False
    # 读取本地config.json
    json_data = json.load(open(f'config.json', 'r', encoding='utf-8'))
    self.keyboard_flag = json_data['keyboard_flag']
    self.mouse_flag = json_data['mouse_flag']
    self.auto_run = json_data['auto_run']
    self.SELECT_SOUND = json_data['choose_sound']


  # 启动键盘监听线程
  def on_key_event(self):
    keyboard.hook(self.callback)
    keyboard.wait()

  # 监听键盘事件
  def callback(self, event):
    event.name = event.name[0].upper() + event.name[1:]
    event.name = keyfilter(event.name)
    if event.name not in self.keyList:
      self.keyList[event.name] = False
    if event.event_type == 'down' and self.keyList[event.name] == False:
      print(event.name,' is down')
      self.keyList[event.name] = True
      # window.evaluate_js(f'window.downKEY("{event.name}")')
      threading.Thread(target=self.downKEY, args=(event.name,)).start()
      threading.Thread(target=self.playSound, args=(event.name,)).start()
    elif event.event_type == 'up' and self.keyList[event.name] == True:
      print(event.name, ' is up')
      self.keyList[event.name] = False
      # window.evaluate_js(f'window.upKEY("{event.name}")')
      threading.Thread(target=self.upKEY, args=(event.name,)).start()

  # 播放音效
  def playSound(self, key):
    if self.keyboard_flag == False:
      return
    if self.SELECT_SOUND == "":
      return
    # 读取index.json
    json_data = json.load(open(f'./sounds/{self.SELECT_SOUND}/index.json', 'r', encoding='utf-8'))
    mode = json_data['mode']
    repeat_sound = json_data['repeat_sound']
    assigned_sounds = json_data['assigned_sounds']
    # 指定模式
    if mode == '指定':
      for sound in assigned_sounds:
        if sound['key'] == key:
          playsound.playsound(f'./sounds/{self.SELECT_SOUND}/sounds/{sound["sound"]}')
    # 重复模式
    elif mode == '重复':
      playsound.playsound(f'./sounds/{self.SELECT_SOUND}/sounds/{repeat_sound}')
    # 随机模式
    elif mode == '随机':
      soundsList = os.listdir(f'./sounds/{self.SELECT_SOUND}/sounds')
      import random
      sound = random.choice(soundsList)
      print('随机播放音效：', sound)
      playsound.playsound(f'./sounds/{self.SELECT_SOUND}/sounds/{sound}')
      print('播放完毕------------')

  # 按键按下
  def downKEY(self, key):
    if self.window_flag:
      self.window.evaluate_js(f'window.downKEY("{key}")')

  # 按键抬起
  def upKEY(self, key):
    if self.window_flag:
      self.window.evaluate_js(f'window.upKEY("{key}")')

  # 获取音效列表
  def getSoundList(self):
    soundsList = os.listdir('./sounds')
    return soundsList
  
  # 获取音效信息
  def getSoundInfo(self, soundName):
    # 读取index.json
    json_data = json.load(open(f'./sounds/{soundName}/index.json', 'r', encoding='utf-8'))
    json_data['soundsList'] = os.listdir(f'./sounds/{soundName}/sounds')
    return json_data
  
  # 更新音效信息
  def updateSoundInfo(self, soundInfo):
   name = soundInfo['name']
   # 读取index.json
   json_data = open(f'./sounds/{name}/index.json', 'w', encoding='utf-8')
   json.dump(soundInfo, json_data, ensure_ascii=False, indent=4)

  # 新建音效信息
  def newSoundInfo(self, name):
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
  def delSoundInfo(self, name):
    shutil.rmtree(f"./sounds/{name}")  
    return True

  # 添加音效文件
  def addSoundFile(self, name):
    file_types = ('Image Files (*.mp3;*.wav)', 'All files (*.*)')
    result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    if result:
      print(result)
      for file in result:
        shutil.copy(file, f'./sounds/{name}/sounds/')
      return True

  # 删除音效文件
  def delSoundFile(self, name):
    os.remove(f'./sounds/{self.SELECT_SOUND}/sounds/{name}')
    return True

  # 选择音效
  def selectSound(self, name):
    self.SELECT_SOUND = name
    # 存入本地sound.ini
    tmp = {
        'keyboard_flag': self.keyboard_flag,
        'mouse_flag': self.mouse_flag,
        'choose_sound': self.SELECT_SOUND,
        'auto_run': self.auto_run
    }
    json_data = open(f'config.json', 'w', encoding='utf-8')
    json.dump(tmp, json_data, ensure_ascii=False, indent=4)

  # 初始化函数
  def initUI(self):
      json_data = json.load(open('config.json', 'r', encoding='utf-8'))
      self.SELECT_SOUND = json_data['choose_sound']
      return self.SELECT_SOUND
  
  # 导出音效
  def exportSound(self, name):
    file_types = ('Image Files (*.zip)', 'All files (*.*)')
    print(name)
    result = self.window.create_file_dialog(webview.SAVE_DIALOG, allow_multiple=False, file_types=file_types,save_filename=name)
    if result:
      print(result)
      result = result.split('.')[0]
      shutil.make_archive(result, 'zip', f'./sounds/{name}')
      return True

  # 导入音效
  def importSound(self):
    file_types = ('Image Files (*.zip)', 'All files (*.*)')
    result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    for i in result:
      print(i)
      i = str(i)
      # 创建文件夹
      name = i.split('\\')[-1].split('.')[0]
      os.mkdir(f'./sounds/{name}')
      shutil.unpack_archive(i, f'./sounds/{name}')
      return True

  # 键盘 鼠标 总开关
  def globalSwitch(self, open1, switch1, switch2):
    if open1:
      self.keyboard_flag = switch1
      self.mouse_flag = switch2
      print('键盘开关：', self.keyboard_flag)
      print('鼠标开关：', self.mouse_flag)
      tmp = {
        'choose_sound': self.SELECT_SOUND,
        'keyboard_flag': self.keyboard_flag,
        'mouse_flag': self.mouse_flag,
        'auto_run': self.auto_run
      }
      json_data = open(f'config.json', 'w', encoding='utf-8')
      json.dump(tmp, json_data, ensure_ascii=False, indent=4)
    else:
      # 读取本地config.json
      json_data = json.load(open('config.json', 'r', encoding='utf-8'))
      self.keyboard_flag = json_data['keyboard_flag']
      self.mouse_flag = json_data['mouse_flag']
      return self.keyboard_flag,self.mouse_flag
    # return True

  # 鼠标监听回调
  def on_move(self, x, y):
    print('Pointer moved to {0}'.format((x, y)))
    if self.sotp_mouse:
    # Stop listener
      return False


  def on_click(self,x, y, button, pressed):
      # print(f"{'点击' if pressed else '抬起'}了{button}")
      if self.mouse_flag:
        if pressed:
          print('点击了', button)
          if button == pynput.mouse.Button.left:
            # self.window.evaluate_js(f'window.mouse_down("l")')
            threading.Thread(target=self.window.evaluate_js, args=(f'window.mouse_down("l")',)).start()
          elif button == pynput.mouse.Button.right:
            # self.window.evaluate_js(f'window.mouse_down("r")')
            threading.Thread(target=self.window.evaluate_js, args=(f'window.mouse_down("r")',)).start()
        else:
          print('抬起了', button)
          if button == pynput.mouse.Button.left:
            # self.window.evaluate_js(f'window.mouse_up("l")')
            threading.Thread(target=self.window.evaluate_js, args=(f'window.mouse_up("l")',)).start()
          elif button == pynput.mouse.Button.right:
            # self.window.evaluate_js(f'window.mouse_up("r")')
            threading.Thread(target=self.window.evaluate_js, args=(f'window.mouse_up("r")',)).start()


  def on_scroll(self, x, y, dx, dy):
      print('Scrolled {0} at {1}'.format(
          'down' if dy < 0 else 'up',
          (x, y)))


  # 启动鼠标监听
  def start_mouse(self):
    with pynput.mouse.Listener(
        # on_move=self.on_move,
        on_click=self.on_click,
        # on_scroll=self.on_scroll
        ) as listener:
      listener.join()
  


  # 开机自启
  def auto_start(self, flag):
    self.auto_run = flag
    # 写入本地config.json
    tmp = {
      'choose_sound': self.SELECT_SOUND,
      'keyboard_flag': self.keyboard_flag,
      'mouse_flag': self.mouse_flag,
      'auto_run': self.auto_run
    }
    json_data = open(f'config.json', 'w', encoding='utf-8')
    json.dump(tmp, json_data, ensure_ascii=False, indent=4)
    if self.auto_run:
      # 添加开机自启注册表
      key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
      winreg.SetValueEx(key, 'KeySound', 0, winreg.REG_SZ, f"{os.getcwd()}\KeySound.exe")
      winreg.CloseKey(key)
    else:
      # 删除开机自启注册表
      key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
      winreg.DeleteValue(key, 'KeySound')
      winreg.CloseKey(key)



  # 查看是否开机自启
  def is_auto_start(self):
    return self.auto_run

  # 创建window
  def create_window_(self):
    self.window = webview.create_window('KeySound', 'http://127.0.0.1:8080/', width=1200, height=550,text_select=False,resizable=True)
    # self.window = webview.create_window('KeySound', './ui/index.html', width=1200, height=550,text_select=False,resizable=True)
    self.window.events.closing += self.on_closing
    self.window.expose(self.getSoundList, 
                       self.getSoundInfo, 
                       self.updateSoundInfo,
                       self.newSoundInfo,
                       self.delSoundInfo, 
                       self.addSoundFile, 
                       self.selectSound,
                       self.initUI,
                       self.playSound, 
                       self.exportSound,
                       self.importSound,
                       self.globalSwitch,
                      self.delSoundFile,
                      self.is_auto_start,
                      self.auto_start,
    )
    # 查看本地debug.txt是否存在 存在则开启debug模式
    if os.path.exists('debug.txt'):
      webview.start(debug=True)
    else:
      webview.start()
  
  # 发信号给主线程创建window （webview必须在主线程创建）
  def test(self):
    if not self.window_flag:
      self.event.set()
    self.window_flag = True
    

  # 销毁window
  def destroy_window(self):
    self.window.destroy()
    self.window_flag = False
  
  # 窗口即将关闭事件
  def on_closing(self):
    print('窗口即将关闭')
    self.window_flag = False
    # self.window.destroy()
    # return True

  # 卸载托盘图标
  def on_exit(self, icon):
    icon.visible = False
    icon.stop()
    if self.window_flag:
      self.window.destroy()
    # 强制退出
    os._exit(0)


  # 创建菜单
  def create_menu(self, event):
    self.event = event
    self.test()
    self.menu = (
      # MenuItem(text='销毁创建', action=self.destroy_window), 
      # MenuItem(text='测试', action=self.test),
      MenuItem(text='显示', action=self.test, default=True, visible=False),
      MenuItem(text='退出', action=self.on_exit),
    )
    image = Image.open("logo.ico")
    icon = pystray.Icon("name", image, "keysound", self.menu)
    icon.run()

  # 初始化配置文件
  def initConfig(self):
    # 查看是否有config.json
    try:
      if not os.path.exists(f'config.json'):
        # 没有就创建
        json_data = {
          'keyboard_flag': True,
          'mouse_flag': False,
          'choose_sound': '',
          'auto_run': False
        }
        with open('config.json', 'w', encoding='utf-8') as f:
          json.dump(json_data, f, ensure_ascii=False, indent=2)
          f.close()
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
    except:
      pass


          
if __name__ == '__main__':
  event1 = threading.Event()
  keysound = KeySound()
  # 开线程监听键盘
  t1 = threading.Thread(target=keysound.on_key_event)
  t1.daemon = True
  t1.start()
  # 开线程创建菜单
  t2 = threading.Thread(target=keysound.create_menu, args=(event1,))
  t2.daemon = True
  t2.start()
  while True:
    event1.wait()
    event1.clear()
    keysound.create_window_()




