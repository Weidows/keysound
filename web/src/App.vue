<template>
  <Load v-if="load"/>
  <Menu/>
  <!-- <router-view></router-view> -->
  <!-- 组件全部缓存 -->
   <router-view v-slot="{ Component }">
   <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>


</template>

<script>
import Menu from '@/components/Menu.vue'
import Load from '@/components/Loading.vue'
import {ref} from 'vue'
export default {
  name: 'App',
  components: {
    Menu,
    Load
  },
  data () {
    const load = ref(true)
    window.addEventListener('load', () => {
      load.value = false
      console.log('load');
    })
    return {
      load
    }
  },
}
</script>
<style lang="less">
#app {
  height: 100%;
  // width: 1200px;
  display: flex;
  background-color: #333;
}
</style>
