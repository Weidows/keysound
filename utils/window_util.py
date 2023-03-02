from config.window_config import window_config_obj
import os
from pystray import MenuItem
import pystray
from PIL import Image
from config.global_config import global_config_obj
import winreg
import webview
from utils.mouse_util import *
from utils.keyboard_util import *
from utils.sound_util import *
import json

# 初始化函数
def initUI():
    ...

# 销毁window
def destroy_window():
    window_config_obj.window.destroy()
    window_config_obj.window_flag = False

# 窗口即将关闭事件
def on_closing():
    print('窗口即将关闭')
    window_config_obj.window_flag = False

# 发信号给主线程创建window （webview必须在主线程创建）
def test():
    if not window_config_obj.window_flag:
      window_config_obj.event.set()
    window_config_obj.window_flag = True


# 开机自启
def auto_start(flag):
    global_config_obj.auto_run = flag
    # 写入本地config.json
    global_config_obj.save()
    if global_config_obj.auto_run:
      # 添加开机自启注册表
      key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
      winreg.SetValueEx(key, 'KeySound', 0, winreg.REG_SZ, f"{os.getcwd()}\KeySound.exe")
      winreg.CloseKey(key)
    else:
      # 删除开机自启注册表
      key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
      winreg.DeleteValue(key, 'KeySound')
      winreg.CloseKey(key)


# 键盘 鼠标 总开关
def globalSwitch(open1, switch1, switch2):
    if open1:
      global_config_obj.keyboard_flag = switch1
      global_config_obj.mouse_flag = switch2
      global_config_obj.save()
    else:
      # 读取本地config.json
      global_config_obj.reload()
      return global_config_obj.keyboard_flag,global_config_obj.mouse_flag

# 查看是否开机自启
def is_auto_start():
    return global_config_obj.auto_run

# 创建window
def create_window_():
    window_config_obj.window = webview.create_window('KeySound', 'http://127.0.0.1:8080/', width=1200, height=550,text_select=False,resizable=True)
    window_config_obj.window.events.closing += on_closing
    window_config_obj.window.expose(getSoundList,
                       getSoundInfo,
                       updateSoundInfo,
                       newSoundInfo,
                       delSoundInfo,
                       addSoundFile,
                       selectSound,
                       initUI,
                       playSound,
                       exportSound,
                       importSound,
                       globalSwitch,
                      delSoundFile,
                      is_auto_start,
                      auto_start,
    )
    # 查看本地debug.txt是否存在 存在则开启debug模式
    if os.path.exists('debug.txt'):
      webview.start(debug=True)
    else:
      webview.start()


# 创建菜单
def create_menu(event):
    window_config_obj.event = event
    test()
    menu = (
      # MenuItem(text='销毁创建', action=self.destroy_window),
      # MenuItem(text='测试', action=self.test),
      MenuItem(text='显示', action=test, default=True, visible=False),
      MenuItem(text='退出', action=on_exit),
    )
    image = Image.open("logo.ico")
    icon = pystray.Icon("name", image, "keysound", menu)
    icon.run()

# 卸载托盘图标
def on_exit(icon):
    icon.visible = False
    icon.stop()
    if window_config_obj.window_flag:
      window_config_obj.window.destroy()
    # 强制退出
    os._exit(0)
