<template>
  <div>
    <el-row>
      <el-col :span="4">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </el-col>
    </el-row>
    <el-table
      :data="data"
      style="width: 100%"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="80"
      />
      <el-table-column
        prop="team"
        label="团队"
        width="180"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="180"
      />
      <el-table-column
        prop="name"
        label="报告名"
        width="180"
      />
      <el-table-column
        prop="type"
        label="类型"
        width="180"
      />
      <el-table-column
        prop="start"
        label="开始时间"
        width="180"
      />
      <el-table-column
        prop="end"
        label="结束时间"
        width="180"
      />
      <el-table-column
        prop="duration"
        label="运行时间"
        width="80"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleOpen(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-edit"
            type="warning"
          >
            查看
          </el-button>
          <el-button
            @click="handleDelete(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-delete"
            type="danger"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader
  },
  data () {
    return {
      data: [],
      limit: 10,
      page: 0,
      team: '',
      project: ''
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      const params = {
        limit: this.limit,
        skip: this.page * this.limit
      }
      if (this.team !== '') {
        params.team = this.team
      }
      if (this.project !== '') {
        params.project = this.project
      }
      this.$axios
        .post('/api/v1/report/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
          } else {
            this.$message({
              type: 'error',
              message: res.data.message
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '服务出错，请联系管理员'
          })
        })
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.refresh()
    },
    handleOpen (value) {
      console.log(value)
    },
    handleDelete (value) {
      console.log(value)
    }
  }
}
</script>
