<template>
  <el-cascader
    v-model="cascader"
    :options="options"
    @change="handleChange"
    placeholder="请选择团队和项目"
    clearable
  />
</template>

<script>
export default {
  data () {
    return {
      cascader: [],
      options: []
    }
  },
  mounted () {
    this.getCascader()
  },
  methods: {
    getCascader () {
      this.$axios
        .post('/api/v1/team/aggregate', { cascader: null })
        .then((res) => {
          this.options = res.data.data
        })
    },
    handleChange (value) {
      this.cascader = value
      const data = {
        team: value[0],
        project: value[1]
      }
      this.$emit('selectedTeamProject', data)
    }
  }
}
</script>

<style scoped>
.el-cascader {
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
