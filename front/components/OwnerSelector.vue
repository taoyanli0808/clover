<template>
  <el-select
    v-model="owner"
    @change="selectOwner"
    placeholder="请选择"
    clearable
  >
    <el-option
      v-for="owner in owners"
      :key="owner.value"
      :label="owner.label"
      :value="owner.value">
    </el-option>
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
      this.$axios({
        url: '/api/v1/environment/aggregate',
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
            label: res.data.data[index]._id,
            value: res.data.data[index]._id
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
