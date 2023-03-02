
# # 销毁window
# def destroy_window():
#   window.destroy()

# # 创建window
# def create_window():
#   global window
#   window =  webview.create_window('KeySound', 'http://127.0.0.1:8080/', width=1300, height=600,text_select=False)
#   window.expose(getSoundList, getSoundInfo, updateSoundInfo,newSoundInfo,delSoundInfo, addSoundFile, selectSound,initUI,playSound, exportSound,importSound)
#   webview.start(debug=True)


# def on_exit(icon, item):
#     icon.stop()
# def notify(icon: pystray.Icon):
#     icon.notify("我是消息类容", "消息标题")

# def run():
#   menu = (
#     MenuItem(text='销毁window', action=destroy_window), 
#     MenuItem(text='创建window', action=create_window),
#     MenuItem(text='发送通知', action=notify),
#     MenuItem(text='我是点击图标的菜单', action=destroy_window, default=True, visible=False),
#     MenuItem(text='退出', action=on_exit),
#   )
#   image = Image.open("logo.ico")
#   icon = pystray.Icon("name", image, "鼠标移动到\n托盘图标上\n展示内容", menu)
#   icon.run()



# # 抬起按键时，调用js中的upKEY方法
# def upKEY(key):
#   if window:
#     window.evaluate_js(f'window.upKEY("{key}")')

# # 按下按键时，调用js中的downKEY方法
# def downKEY(key):
#   print(window)
#   if window:
#     window.evaluate_js(f'window.downKEY("{key}")')


# # 获取音效包列表
# def getSoundList():
#   soundList = os.listdir('./sounds')
#   return soundList

# # 获取音效包信息
# def getSoundInfo(soundName):
#   # 读取index.json
#   json_data = json.load(open(f'./sounds/{soundName}/index.json', 'r', encoding='utf-8'))
#   json_data['soundsList'] = os.listdir(f'./sounds/{soundName}/sounds')
#   return json_data



# # 更新音效包信息
# def updateSoundInfo(soundInfo):
#   name = soundInfo['name']
#   # 读取index.json
#   json_data = open(f'./sounds/{name}/index.json', 'w', encoding='utf-8')
#   json.dump(soundInfo, json_data, ensure_ascii=False, indent=4)
#   # json_data.close()
#   # return True


# # 新建音效包
# def newSoundInfo(name):
#   print(name)
#   temp = {
#   "name": name,
#   "mode": "",
#   "repeat_sound": "",
#   "assigned_sounds": []
#   }
#   # 创建文件夹
#   os.mkdir(f'./sounds/{name}')
#   os.mkdir(f'./sounds/{name}/sounds')
#   # 写入index.json
#   json_data = open(f'./sounds/{name}/index.json', 'w', encoding='utf-8')
#   json.dump(temp, json_data, ensure_ascii=False, indent=4)

# import shutil
# # 删除音效包
# def delSoundInfo(name):
#   # os.removedirs(f'./sounds/{name}')
#   shutil.rmtree(f"./sounds/{name}")  
#   return True

# # 往音效包里添加mp3等音效文件
# def addSoundFile(name):
#   file_types = ('Image Files (*.mp3;*.wav)', 'All files (*.*)')
#   result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
#   if result:
#     print(result)
#     for file in result:
#       shutil.copy(file, f'./sounds/{name}/sounds/')
#     return True

# # 选择音效包
# def selectSound(name):
#   global SELECT_SOUND
#   SELECT_SOUND = name
#   # 存入本地sound.ini
#   with open('sound.ini', 'w', encoding='utf-8') as f:
#     f.write(name)
#   return True

# # 播放音效
# def playSound(key):
#   print(key)
#   print(SELECT_SOUND)
#   if SELECT_SOUND == "":
#     return
#   # 读取index.json
#   json_data = json.load(open(f'./sounds/{SELECT_SOUND}/index.json', 'r', encoding='utf-8'))
#   mode = json_data['mode']
#   repeat_sound = json_data['repeat_sound']
#   assigned_sounds = json_data['assigned_sounds']
#   # 指定模式
#   if mode == '指定':
#     for sound in assigned_sounds:
#       if sound['key'] == key:
#         playsound.playsound(f'./sounds/{SELECT_SOUND}/sounds/{sound["sound"]}')
#   # 重复模式
#   elif mode == '重复':
#     playsound.playsound(f'./sounds/{SELECT_SOUND}/sounds/{repeat_sound}')
#   # 随机模式
#   elif mode == '随机':
#     soundsList = os.listdir(f'./sounds/{SELECT_SOUND}/sounds')
#     import random
#     sound = random.choice(soundsList)
#     print('随机播放音效：', sound)
#     playsound.playsound(f'./sounds/{SELECT_SOUND}/sounds/{sound}')
#     print('播放完毕------------')



# # 初始化函数
# def initUI():
#     return SELECT_SOUND

    
# # 导出音效包
# def exportSound(name):
#   file_types = ('Image Files (*.zip)', 'All files (*.*)')
#   print(name)
#   result = window.create_file_dialog(webview.SAVE_DIALOG, allow_multiple=False, file_types=file_types,save_filename=name)
#   if result:
#     print(result)
#     result = result.split('.')[0]
#     shutil.make_archive(result, 'zip', f'./sounds/{name}')
#     return True



# # 导入音效包
# def importSound():
#   file_types = ('Image Files (*.zip)', 'All files (*.*)')
#   result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
#   for i in result:
#     print(i)
#     i = str(i)
#     # 创建文件夹
#     name = i.split('\\')[-1].split('.')[0]
#     os.mkdir(f'./sounds/{name}')
#     shutil.unpack_archive(i, f'./sounds/{name}')
#     return True
    
  
# def callback(event):
#   event.name = event.name[0].upper() + event.name[1:]
#   event.name = keyfilter(event.name)
#   if event.name not in keyList:
#     keyList[event.name] = False
#   if event.event_type == 'down' and keyList[event.name] == False:
#     print(event.name,' is down')
#     keyList[event.name] = True
#     # window.evaluate_js(f'window.downKEY("{event.name}")')
#     threading.Thread(target=downKEY, args=(event.name,)).start()
#     threading.Thread(target=playSound, args=(event.name,)).start()
#   elif event.event_type == 'up' and keyList[event.name] == True:
#     print(event.name, ' is up')
#     keyList[event.name] = False
#     # window.evaluate_js(f'window.upKEY("{event.name}")')
#     threading.Thread(target=upKEY, args=(event.name,)).start()



# # 监听键盘事件
# def on_key_event():
#   keyboard.hook(callback)
#   keyboard.wait()




# 创建window




# if __name__ == '__main__':
#     # 读取本地sound.ini
#     if os.path.exists('sound.ini'):
#       with open('sound.ini', 'r', encoding='utf-8') as f:
#         SELECT_SOUND = f.read()

#     # 启动键盘监听线程
#     t = threading.Thread(target=on_key_event)
#     t.daemon = True
#     t.start()

#     threading.Thread(target=run).start()

#     # webview.create_window('KeySound', 'http://127.0.0.1:8080/', width=1200, height=500)
#     # window = webview.create_window('KeySound', 'http://127.0.0.1:8080/', width=1300, height=600,text_select=False)
#     # window.expose(getSoundList, getSoundInfo, updateSoundInfo,newSoundInfo,delSoundInfo, addSoundFile, selectSound,initUI,playSound, exportSound,importSound)
#     # webview.start(debug=True)
#     create_window()


# -------------------------------
# 整理代码


