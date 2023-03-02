<template>
  <div class="keyboard">
    <!-- 选择音效 -->
    <div class="currentSound">
      <div style="height: 100%">
        <el-select
          v-model="value"
          class="m-2"
          placeholder="选择音效包"
          size="large"
          @change="changeSound"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>

        <el-select
          v-model="sound_info.mode"
          class="m-2"
          placeholder="选择模式"
          size="large"
          style="width: 120px; margin-left: 10px"
          @change="changeMode"
          v-if="value"
        >
          <el-option
            v-for="item in ['随机', '重复', '指定', '单键随机']"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
        <!-- 选择指定音效包 -->
        <el-select
          v-model="sound_info.repeat_sound"
          class="m-2"
          placeholder="选择重复音效"
          size="large"
          style="width: 150px; margin-left: 10px"
          v-if="sound_info.mode == '重复'"
          @change="updata"
        >
          <el-option
            v-for="item in sound_info.soundsList"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>

        <el-tooltip
          class="box-item"
          effect="light"
          content="允许修改"
          placement="top"
          v-if="revise_switch && sound_info.mode == '指定'"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="revise_switch = !revise_switch"
          >
            <i style="font-size: 25px" class="iconfont icon-suoding"></i>
          </el-button>
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="light"
          content="禁止修改"
          placement="top"
          v-if="!revise_switch && sound_info.mode == '指定'"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="revise_switch = !revise_switch"
          >
            <i style="font-size: 25px" class="iconfont icon-jiesuo"></i>
          </el-button>
        </el-tooltip>

        <span v-if="revise_switch && sound_info.mode == '指定'">
          <span style="margin: 0px 10px">KEY: {{ currentKey }}</span>
          <el-select
            v-model="currentSound"
            class="m-2"
            placeholder="选择音效"
            size="large"
            style="width: 150px"
            @change="changeCurrentSound"
          >
            <el-option
              v-for="item in sound_info.soundsList"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
          <!-- 清楚按钮 -->
          <el-tooltip
            class="box-item"
            effect="light"
            content="清除键位绑定"
            placement="top"
            v-if="currentSound"
          >
            <el-button
              plain
              style="margin-left: 10px; padding: 0px 10px"
              @click="clearCurrentSound"
            >
              <i style="font-size: 25px" class="iconfont icon-qingchu"></i>
            </el-button>
          </el-tooltip>
        </span>
        <el-tooltip
          class="box-item"
          effect="light"
          content="导入音效文件"
          placement="top"
          v-if="value"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="addSoundFile"
          >
            <i style="font-size: 25px" class="iconfont icon-daoru_o"></i>
          </el-button>
        </el-tooltip>

        <el-tooltip
          class="box-item"
          effect="light"
          content="删除音效包"
          placement="top"
          v-if="value"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="delSoundInfo"
          >
            <i style="font-size: 25px" class="iconfont icon-shanchu"></i>
          </el-button>
        </el-tooltip>
      </div>

      <div style="height: 100%">
        <el-tooltip
          class="box-item"
          effect="light"
          content="新建音效包"
          placement="top"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="createsounds"
          >
            <i style="font-size: 25px" class="iconfont icon-xinjian"></i>
          </el-button>
        </el-tooltip>

        <el-tooltip
          class="box-item"
          effect="light"
          content="导入音效包"
          placement="top"
        >
          <!-- css 图标反转 -->
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="importSound"
          >
            <i
              style="
                font-size: 25px;
                transform: rotate(180deg);
                -webkit-transform: rotate(180deg);
              "
              class="iconfont icon-daochu"
            ></i>
          </el-button>
        </el-tooltip>

        <el-tooltip
          class="box-item"
          effect="light"
          content="导出音效包"
          placement="top"
        >
          <el-button
            plain
            style="margin-left: 10px; padding: 0px 10px"
            @click="exportSound"
          >
            <i style="font-size: 25px" class="iconfont icon-daochu"></i>
          </el-button>
        </el-tooltip>
      </div>
    </div>
    <!-- 音效包的声音文件列表 -->
    <div class="soundsList">
      <ul>
        <li v-for="(item, index) in sound_info.soundsList" :key="index">
          <span>{{ item }}</span>
          <!-- <el-button type="danger" text > 删除 </el-button> -->
          <p @click="del_one_sound(item)">删除</p>
        </li>
      </ul>
    </div>
    <KeyBoard />
    <!-- <Mouse/> -->
  </div>
</template>

<script>
import KeyBoard from "@/components/KeyBoard.vue";
import Mouse from "@/components/Mouse.vue";
import { reactive, toRefs, onMounted } from "vue";
import bus from "@/utils/bus.js";
import { ElMessage, ElMessageBox } from "element-plus";
import { get_sound_list_test } from '@/utils/pyapi.js'
export default {
  name: "HomeView",
  components: {
    KeyBoard,
    Mouse,
  },
  setup() {
    const data = reactive({
      // 修改开关
      revise_switch: false,
      // 当前选择的key
      currentKey: "Q",
      // 当前key的音效
      currentSound: "",
      // 当前选择的音效包
      value: "",
      // 音效包列表
      options: [],
      // 音效包信息
      sound_info: {},
      // 指定音效包选择
      select_sound: "",
    });
    // 获取音效包列表
    const getSoundList = () => {
      data.options = [];
      pywebview.api.getSoundList().then((res) => {
        console.log(res);
        res.forEach((element) => {
          data.options.push({
            value: element,
            label: element,
          });
        });
      });
    };
    // 选择音效包
    const changeSound = (value) => {
      data.value = value;
      data.revise_switch = false;
      // 选择音效包 python 里
      pywebview.api.selectSound(value);
      // 获取音效包信息
      pywebview.api.getSoundInfo(value).then((res) => {
        console.log(res);
        data.sound_info = res;
        addStyle();
      });
    };

    // 把changeSound挂在到window上
    window.changeSound = changeSound;

    const delStyle = () => {
      let keys = document.querySelectorAll(".key");
      keys.forEach((key) => {
        key.classList.remove("keybind");
        key.removeAttribute("alt");
      });
    };

    // 给音效包里存在的键位添加样式
    const addStyle = () => {
      // 先获取模式
      let mode = data.sound_info.mode;
      // 先清楚所有的样式
      let keys = document.querySelectorAll(".key");
      keys.forEach((key) => {
        key.classList.remove("keybind");
        key.removeAttribute("alt");
      });

      if (mode == "指定") {
        // 先获取到所有的键位
        let keys = document.querySelectorAll(".key");
        data.sound_info.assigned_sounds.forEach((element) => {
          console.log(element);
          keys.forEach((key) => {
            if (key.innerText == element.key) {
              // 添加类名
              key.classList.add("keybind");
              // 添加alt属性
              key.setAttribute("alt", element.sound);
            }
          });
        });
      } else if (mode == "重复") {
        // 先获取到所有的键位
        let keys = document.querySelectorAll(".key");
        // 给全部键加上 sound_info.repeat_sound
        keys.forEach((key) => {
          // 添加类名
          key.classList.add("keybind");
          // 添加alt属性
          key.setAttribute("alt", data.sound_info.repeat_sound);
        });
      } else if (mode == "随机") {
        // 先获取到所有的键位
        let keys = document.querySelectorAll(".key");
        keys.forEach((key) => {
          // 移除类名
          key.classList.remove("keybind");
          // 移除alt属性
          key.removeAttribute("alt");
        });
      }
    };

    onMounted(() => {
      bus.on("keyDown", (key) => {
        if (data.revise_switch) {
          data.currentKey = key;
          console.log("开关打开了");
          // 读取配置里的key sounds填入currentSound
          var tmpkey = "";
          data.sound_info.assigned_sounds.forEach((element) => {
            if (element.key == key) {
              tmpkey = element.sound;
            }
          });
          if (tmpkey != "") {
            data.currentSound = tmpkey;
          } else {
            data.currentSound = "";
          }
        } else {
          console.log("开关没打开");
          // 播放音效qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
          // pywebview.api.playSound(key);
        }
      });
      bus.on("selectKEY", (key) => {
        data.currentKey = key;
        // 读取配置里的key sounds填入currentSound
        var tmpkey = "";
        data.sound_info.assigned_sounds.forEach((element) => {
          if (element.key == key) {
            tmpkey = element.sound;
          }
        });
        if (tmpkey != "") {
          data.currentSound = tmpkey;
        } else {
          data.currentSound = "";
        }
      });

      window.addEventListener("pywebviewready", function () {
        getSoundList();
        pywebview.api.initUI().then((res) => {
          if (res) {
            changeSound(res);
          }
        });
      });
    });

    // 修改当前key的音效
    const changeCurrentSound = (value) => {
      console.log(value);
      // 修改配置
      let tmp = "";
      data.sound_info.assigned_sounds.forEach((element) => {
        if (element.key == data.currentKey) {
          // element.sound = value
          tmp = element;
        }
      });
      if (tmp != "") {
        tmp.sound = value;
      } else {
        data.sound_info.assigned_sounds.push({
          key: data.currentKey,
          sound: value,
        });
      }
      // // 更新配置
      updata();
    };

    // 清楚当前key的音效
    const clearCurrentSound = () => {
      // 修改配置
      let tmp = "";
      data.sound_info.assigned_sounds.forEach((element) => {
        if (element.key == data.currentKey) {
          // element.sound = value
          tmp = element;
        }
      });
      if (tmp != "") {
        data.sound_info.assigned_sounds.splice(
          data.sound_info.assigned_sounds.indexOf(tmp),
          1
        );
      }
      // // 更新配置
      updata();
      // 把选择的音效清空
      data.currentSound = "";
    };

    // 更新配置
    const updata = () => {
      console.log(data.sound_info);
      pywebview.api.updateSoundInfo(data.sound_info);
      addStyle();
    };

    // 修改模式
    const changeMode = (value) => {
      // console.log(value);
      data.sound_info.mode = value;
      // 更新配置
      updata();
      // 更新样式
      addStyle();
    };

    // 创建音效包
    const createsounds = () => {
      ElMessageBox.prompt("输入音效包名", "Tip", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[^`~!@#$%^&*()_+<>?:"{},.\/;'[\]]*$/,
        inputErrorMessage: "请输出合法的文件名",
      })
        .then(({ value }) => {
          ElMessage({
            type: "success",
            message: `创建音效包 ${value} 成功`,
          });
          // 创建音效包
          pywebview.api.newSoundInfo(value).then((res) => {
            // 重新获取音效包列表
            getSoundList();
            // 把当前选择音效包设置为新创建的
            data.value = value;
            // 从新获取音效包信息
            changeSound(data.value);
          });
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "取消创建",
          });
        });
      // 删除音效包
    };
    // 删除音效包
    const delSoundInfo = () => {
      ElMessageBox.confirm("此操作将永久删除该音效包, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          ElMessage({
            type: "success",
            message: "删除成功!",
          });
          // 删除音效包
          pywebview.api.delSoundInfo(data.sound_info.name).then((res) => {
            // console.log(res);
            // 重新获取音效包列表
            getSoundList();
            // 把当前选择的音效包清空
            data.value = "";
            // 清空音效包信息
            data.sound_info = {};
            pywebview.api.selectSound("");
          });
          // 样式清空
          delStyle();
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "已取消删除",
          });
        });
    };

    // 添加音效文件
    const addSoundFile = () => {
      pywebview.api.addSoundFile(data.sound_info.name).then((res) => {
        changeSound(data.sound_info.name);
      });
    };

    // 导出音效包
    const exportSound = () => {
      if (!data.value) {
        ElMessage({
          type: "error",
          message: "请先选择音效包",
        });
        return;
      }
      pywebview.api.exportSound(data.sound_info.name).then((res) => {
        if (res) {
          ElMessage({
            type: "success",
            message: "导出成功",
          });
        } else {
          ElMessage({
            type: "error",
            message: "导出失败",
          });
        }
      });
    };

    // 导入音效包
    const importSound = () => {
      pywebview.api.importSound().then((res) => {
        if (res) {
          ElMessage({
            type: "success",
            message: "导入成功",
          });
          // 重新获取音效包列表
          getSoundList();
        } else {
          ElMessage({
            type: "error",
            message: "导入失败",
          });
        }
      });
    };

    // 删除单个音效
    const del_one_sound = (name) => {
      console.log(name);
      pywebview.api.delSoundFile(name).then((res) => {
        changeSound(data.sound_info.name);
      });
    };
    return {
      ...toRefs(data),
      changeSound,
      changeCurrentSound,
      updata,
      changeMode,
      clearCurrentSound,
      createsounds,
      delSoundInfo,
      addSoundFile,
      exportSound,
      importSound,
      del_one_sound,
    };
  },
};
</script>

<style lang="less" scoped>
.keyboard {
  height: 100%;
  width: 95%;
  background-color: #333;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #fff;
  .currentSound {
    // height: 40px;
    padding: 5px 10px;
    // background: red;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .soundsList {
    // height: 90px;
    height: 20%;
    width: 470px;
    padding: 0px 10px;
    ul {
      height: 100%;
      overflow: auto;
      // 滚动条样式
      &::-webkit-scrollbar {
        width: 5px;
        height: 5px;
      }
      &::-webkit-scrollbar-thumb {
        background: #fff;
        border-radius: 10px;
      }
      &::-webkit-scrollbar-track {
        background: #666;
        border-radius: 10px;
      }
      // span{
      //   cursor: pointer;
      // }
      li {
        width: 33%;
        list-style: none;
        cursor: pointer;
        display: inline-flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
        border-bottom: 1px #ffffff00 solid;
        padding: 0 5px;
        span{
          width: 100%;
          display: flex;
        }
        p {
          // padding: 0 5px;
          color: #fff;
          transition: all 0.2s;
          // 不允许换行
          white-space: nowrap;
          &:hover {
            color: red;
          }
        }
        &:hover {
          // color: #333;
          // background: #fff;
          border-bottom: 1px #fff solid;
        }
      }
    }
  }
}
/deep/.el-button {
  height: 100%;
  // margin-left: 10px;
}
</style>
