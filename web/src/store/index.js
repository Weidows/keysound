import { createStore } from 'vuex'

export default createStore({
  state: {
    keyboard_flag: false, // 键盘发声开关
    mouse_flag: false, // 鼠标发声开关
    keysound: "", // 键盘发声音效
    keymode: "", // 键盘发声模式 '随机', '重复', '指定', '单键随机'
    auto_run: false, // 自动运行开关
    soundlist: [], // 音效包列表
    count: 0,
  },
  getters: {
  },
  mutations: {
    setMenu(state, menu) {
      console.log("setMenu", menu);
      state.count += 1
    }
  },
  actions: {
  },
  modules: {
  }
})
