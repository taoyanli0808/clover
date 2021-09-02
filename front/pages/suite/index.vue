<template>
  <div>
    <div class="page-header">
      <div style="display: inline">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </div>
      <div style="display: inline">
        <el-input v-model="caseName" size="small" placeholder="请输入套件名" class="input-with-select">
          <el-button @click="search" slot="append" size="small" icon="el-icon-search" />
        </el-input>
      </div>
      <div style="float: right; padding: 3px 0; display: block;">
        <el-button
          @click="createSuite"
          type="primary"
          size="small"
          plain
        >
          创建套件
        </el-button>
      </div>
    </div>
    <CardList ref="list" />
  </div>
</template>

<script>
import CardList from '~/components/utils/CardList.vue'
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    CardList,
    TeamProjectCascader
  },
  data () {
    return {
      team: '',
      project: '',
      caseName: ''
    }
  },
  methods: {
    createSuite () {
      this.$router.push({
        path: '/suite/create'
      })
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.$store.commit('setTeam', this.team)
      this.$store.commit('setProject', this.project)
      this.$refs.list.search()
    },
    search () {
      this.$store.commit('setTeam', this.team)
      this.$store.commit('setProject', this.project)
      this.$store.commit('setCaseName', this.caseName)
      this.$refs.list.search()
    }
  }
}
</script>

<style scoped>
.el-input {
  width: 300px;
}

.page-header {
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
}
</style>
