// 存放 python那边export的函数


// 获取音效包列表
export  const  get_sound_list_test = () => {
  return pywebview.api.getSoundList()
}


// 选择音效包
export const select_sound = (sound_name) => {
  return pywebview.api.selectSound(sound_name);
}