<template>
  <div>
    <el-menu
      @select="handleSelect"
      :default-active="$route.path"
      mode="horizontal"
    >
      <el-menu-item index="/">
        平台首页
      </el-menu-item>
      <el-submenu index="2">
        <template slot="title">
          接口测试
        </template>
        <el-menu-item index="/interface/">
          接口列表
        </el-menu-item>
        <el-menu-item index="/suite/">
          套件列表
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
        <el-menu-item v-if="keyword" index="/keyword">
          关键字配置
        </el-menu-item>
        <el-menu-item index="/config/plugin">
          插件配置
        </el-menu-item>
        <el-menu-item v-if="task" index="/config/task">
          定时任务
        </el-menu-item>
      </el-submenu>
      <el-menu-item index="/report">
        查看报告
      </el-menu-item>
      <el-menu-item v-if="join" index="keep">
        <a href="https://github.com/52clover" target="_blank">
          加入我们
        </a>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  data () {
    return {
      join: true,
      task: true,
      keyword: true
    }
  },
  mounted () {
    this.updateConfig()
  },
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
    },
    updateConfig () {
      this.$axios.get('/api/v1/index/config', {})
        .then((res) => {
          this.join = res.data.data.join
          this.task = res.data.data.task
          this.keyword = res.data.data.keyword
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '服务出错，请联系管理员',
            center: true
          })
          this.loading = false
        })
    }
  }
}
</script>
