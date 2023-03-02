import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '@/assets/css/index.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
document.oncontextmenu = function(){
  event.returnValue = false;
}
// 或者直接返回整个事件
document.oncontextmenu = function(){
  return false;
}
createApp(App).use(ElementPlus).use(store).use(router).mount('#app')
