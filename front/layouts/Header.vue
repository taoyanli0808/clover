<template>
  <el-menu :default-active="activeIndex" @select="handleSelect" class="el-menu-demo" mode="horizontal">
    <el-menu-item index="1">
      <a href="/">平台首页</a>
    </el-menu-item>
    <el-submenu index="2">
      <template slot="title">
        接口测试
      </template>
      <el-menu-item index="2-1">
        <a href="/interface/">接口列表</a>
      </el-menu-item>
      <el-menu-item index="2-2">
        <a href="/suite/">任务列表</a>
      </el-menu-item>
      <el-menu-item index="2-3">
        先这样
      </el-menu-item>
    </el-submenu>
    <el-submenu index="3">
      <template slot="title">
        配置管理
      </template>
      <el-menu-item index="3-1">
        <a href="/config/project">项目配置</a>
      </el-menu-item>
      <el-menu-item index="3-2">
        <a href="/config/variable">变量配置</a>
      </el-menu-item>
    </el-submenu>
    <el-menu-item index="4">
      <a href="https://github.com/taoyanli0808/clover" target="_blank">
        加入我们
      </a>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  data () {
    return {
      activeIndex: '1',
      activeIndex2: '1'
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>
