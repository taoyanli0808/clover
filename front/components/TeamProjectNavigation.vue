<template>
  <div>
    <el-menu
      @select="handleSelect"
      class="el-menu-vertical-demo"
      unique-opened
    >
      <el-submenu v-for="(option, oi) in options" :key="oi" :index="option.name">
        <template slot="title">
          <i class="el-icon-folder" />
          <span>{{ option.name }}</span>
        </template>
        <el-menu-item v-for="(item, ii) in option.items" :key="ii" :index="option.name + '-' + item">
          {{ item }}
        </el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
export default {
  data () {
    return {
      team: '',
      project: '',
      options: []
    }
  },
  mounted () {
    this.getTeamProject()
  },
  methods: {
    handleSelect (key, keyPath) {
      const temp = key.split('-')
      this.team = temp[0]
      this.project = temp[1]
      this.$emit('selectedTeamProject', { team: this.team, project: this.project })
    },
    getTeamProject () {
      this.$axios
        .post('/api/v1/team/navigation', { cascader: null })
        .then((res) => {
          for (const team in res.data.data) {
            this.options.push({
              name: team,
              items: res.data.data[team]
            })
          }
        }).catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
    }
  }
}
</script>
