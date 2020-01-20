<template>
  <el-menu
    @select="handleSelect"
    :default-active="$route.path"
    class="el-menu-demo"
    mode="horizontal"
  >
    <el-menu-item index="/">
      平台首页
    </el-menu-item>
    <el-submenu index="2">
      <template slot="title">
        接口测试
      </template>
      <el-menu-item index="/interface/create">
        创建接口
      </el-menu-item>
      <el-menu-item index="/interface/">
        接口列表
      </el-menu-item>
      <el-menu-item index="/interface/suite/">
        测试套件
      </el-menu-item>
    </el-submenu>
    <el-submenu index="3">
      <template slot="title">
        配置管理
      </template>
      <el-menu-item index="/config/project">
        项目配置
      </el-menu-item>
      <el-menu-item index="/config/variable">
        变量配置
      </el-menu-item>
      <el-menu-item index="/config/keyword">
        关键字配置
      </el-menu-item>
    </el-submenu>
    <el-menu-item index="/report">
      查看报告
    </el-menu-item>
    <el-menu-item index="keep">
      <a href="https://github.com/taoyanli0808/clover" target="_blank">
        加入我们
      </a>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  methods: {
    handleSelect (key, keyPath) {
      if (key === 'keep') {
        // eslint-disable-next-line no-console
        console.log(key)
      } else {
        this.$router.push({
          path: key
        })
      }
    }
  }
}
</script>
