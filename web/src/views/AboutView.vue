<template>
  <div class="about">
    <p>这是一个基于Vue3.0 + pywebview的桌面应用</p>
    <p>by bilibili Bojaka</p>
    <p>用于给 键盘 和 鼠标 绑定音效</p>
    <p>目前只支持Windows</p>
    <p>当前版本 beta 1.5 稍微优化版</p>
  </div>
</template>


<style lang="less" scoped>
.about {
  width: 95%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 20px;
  p{
    margin-bottom: 5px;
    &:last-child{
      margin-bottom: 0;
    }
  }
}
</style>
