<template>
  <div>
    <el-row>
      <el-col :span="4">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </el-col>
    </el-row>
    <el-table
      :data="data"
      style="width: 100%;"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="50"
        align="ceDnter"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="180"
        align="center"
      />
      <el-table-column
        prop="team"
        label="团队"
        width="180"
        align="center"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="180"
        align="center"
      />
      <el-table-column
        prop="type"
        label="类型"
        width="180"
        align="center"
      />
      <el-table-column
        prop="cases"
        label="用例"
        width="180"
        align="center"
      />
      <el-table-column
        label="统计"
        width="180"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleHistory(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-s-data"
            type="primary"
            plain
          >
            查看
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        prop="created"
        label="创建时间"
        width="180"
        align="center"
      />
      <el-table-column
        prop="updated"
        label="更新时间"
        width="180"
        align="center"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="200"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleRun(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-caret-right"
            type="primary"
          >
            运行
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
      total: 0,
      limit: 10,
      page: 0,
      team: '',
      project: '',
      cases: []
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
        .post('/api/v1/suite/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
            for (const i in this.data) {
              this.data[i].cases = this.data[i].cases.join(',')
            }
          } else {
            this.$message({
              type: 'error',
              message: res.data.message
            })
          }
        })
    },
    handleHistory (index, row) {
      this.$message({
        showClose: true,
        message: '开发者正在加班加点开发，很快就可以用喽！',
        type: 'error'
      })
    },
    handleRun (index, row) {
      this.$prompt('请输入报告名', '运行套件', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        this.$axios({
          url: '/api/v1/suite/trigger',
          method: 'post',
          data: JSON.stringify({
            report: value,
            ...row
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: '触发成功!'
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message
            })
          }
        }).catch((res) => {
          this.$message({
            type: 'error',
            message: res.data.message
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消运行！'
        })
      })
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$axios({
          url: '/api/v1/suite/delete',
          method: 'post',
          data: JSON.stringify({
            id_list: [row.id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          if (res.data.status === 0) {
            this.refresh()
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
          } else {
            this.$message({
              type: 'error',
              message: res.data.message
            })
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.refresh()
    }
  }
}
</script>
