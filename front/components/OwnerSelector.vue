<template>
  <el-select
    v-model="owner"
    @change="selectOwner"
    placeholder="请选择负责人"
    size="small"
    clearable
  >
    <el-option
      v-for="item in owners"
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
      owner: '',
      owners: []
    }
  },
  mounted () {
    this.getOwner()
  },
  methods: {
    getOwner () {
      this.owners = []
      this.$axios({
        url: '/api/v1/team/aggregate',
        method: 'post',
        data: JSON.stringify({
          type: 'team',
          key: 'owner'
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        for (const index in res.data.data) {
          this.owners.push({
            label: res.data.data[index],
            value: res.data.data[index]
          })
        }
      })
    },
    selectOwner () {
      this.$emit('selectedOwner', this.owner)
    }
  }
}
</script>
