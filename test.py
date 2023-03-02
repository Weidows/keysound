import win32api
import win32con
from tendo import singleton

if __name__ == '__main__':

  try:
    me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
  except:
    print("已经有一个实例在运行了!")
    win32api.MessageBox(0, "KeySound 已经在运行了\n请留意右下角图标", "提示",win32con.MB_ICONWARNING)
    exit()

  input("Press Enter to continue...")