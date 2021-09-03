<template>
  <el-select
    v-model="team"
    @change="selectTeam"
    placeholder="请选择团队"
    size="small"
    clearable
  >
    <el-option
      v-for="item in teams"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script>
export default {
  data () {
    return {
      team: '',
      teams: []
    }
  },
  mounted () {
    this.getTeam()
  },
  methods: {
    getTeam () {
      this.teams = []
      this.$axios({
        url: '/api/v1/team/aggregate',
        method: 'post',
        data: JSON.stringify({
          key: 'team'
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        for (const index in res.data.data) {
          this.teams.push({
            label: res.data.data[index],
            value: res.data.data[index]
          })
        }
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    selectTeam (value) {
      this.team = value
      this.$emit('selectedTeam', this.team)
    }
  }
}
</script>
