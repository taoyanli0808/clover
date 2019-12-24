<template>
  <el-cascader
    v-model="cascader"
    :options="options"
    @change="handleChange"
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
        .post('/api/v1/environment/aggregate', { cascader: null })
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
