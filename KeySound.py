# -*- coding:utf-8 _*-
import webview
import threading
import os
from mouse_util import *
from keyboard_util import *
from sound_util import *
from window_util import *


if __name__ == '__main__':
  event1 = threading.Event()
  # 开线程监听键盘
  t1 = threading.Thread(target=on_key_event)
  t1.daemon = True
  t1.start()
  # 开线程创建菜单
  t2 = threading.Thread(target=create_menu, args=(event1,))
  t2.daemon = True
  t2.start()
  while True:
    event1.wait()
    event1.clear()
    create_window_()




