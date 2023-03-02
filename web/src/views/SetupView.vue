<template>
  <div class="setup">
    <p>键盘发声 <el-switch v-model="value1" @change="sw" /></p>
    <!-- <p>鼠标发声 <el-switch v-model="value2" @change="sw" /></p> -->
    <p>开机自启 <el-switch v-model="value3" @change="auto_run" /></p>
  </div>
</template>

<script>
import { onMounted, reactive, toRefs,onActivated } from "vue";
export default {
  setup() {
    const state = reactive({
      value1: false,
      value2: false,
      value3: false,
    });
    onActivated(() => {
        pywebview.api.globalSwitch(false, state.value1, state.value2).then((result) => {
            state.value1 = result[0];
            state.value2 = result[1];
          });
        pywebview.api.is_auto_start().then((result) => {
            state.value3 = result;
        });
    });
    const sw = () => {
      pywebview.api.globalSwitch(true, state.value1, state.value2);
    };
    const auto_run = ()=>{
      pywebview.api.auto_start(state.value3);
    }

    return {
      ...toRefs(state),
      auto_run,
      sw,
    };
  },
};
</script>

<style lang="less" scoped>
.setup {
  padding: 10px;
  background-color: #333;
  color: #fff;
}
</style>
