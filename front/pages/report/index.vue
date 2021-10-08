<template>
  <div>
    <div class="page-header">
      <div style="display: inline">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </div>
      <div style="display: inline">
        <el-input v-model="name" size="small" placeholder="请输入报告名" class="input-with-select">
          <el-button slot="append" @click="search" size="small" icon="el-icon-search" />
        </el-input>
      </div>
    </div>
    <el-table
      :data="data"
      v-loading="loading"
      element-loading-text="拼命加载中"
      style="width: 100%"
      border
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
        width="120"
      />
      <el-table-column
        prop="duration"
        label="运行时间"
        width="120"
      />
      <el-table-column
        prop="interface.total"
        label="接口数量"
        width="120"
      />
      <el-table-column
        prop="interface.verify"
        label="断言数量"
        width="120"
      />
      <el-table-column
        prop="interface.percent"
        label="成功率"
        width="120"
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
          <el-button
            @click="handleLog(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-bank-card"
            type="info"
          >
            日志
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @current-change="handleCurrentChange"
      :total="total"
      background
      layout="total, prev, pager, next, jumper"
    />
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
      total: 0,
      name: '',
      team: '',
      project: '',
      loading: true
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.loading = true
      const params = {
        limit: this.limit,
        offset: this.page * this.limit
      }
      if (this.team !== '') {
        params.team = this.team
      }
      if (this.project !== '') {
        params.project = this.project
      }
      if (this.name !== '') {
        params.name = this.name
      }
      this.$axios
        .post('/api/v1/report/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
            for (const i in this.data) {
              this.data[i].interface.percent = this.data[i].interface.percent.toFixed(0) + '%'
            }
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              center: true
            })
          }
          this.loading = false
        })
        .catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
          this.loading = false
        })
    },
    search () {
      this.page = 0
      this.refresh()
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.refresh()
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    handleOpen (index, row) {
      this.$router.push({
        path: '/report/detail',
        query: {
          id: row.id
        }
      })
    },
    handleDelete (index, row) {
      this.$confirm('此操作将删除该测试报告, 是否继续?', '删除报告', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$axios({
          url: '/api/v1/report/delete',
          method: 'post',
          data: JSON.stringify(row),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          if (res.data.status === 0) {
            this.refresh()
            this.$message({
              type: 'success',
              message: '删除成功!',
              center: true
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message,
              center: true
            })
          }
        }).catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除',
          center: true
        })
      })
    },
    handleLog (index, row) {
      this.$router.push({
        path: 'report/log',
        query: {
          id: row.id
        }
      })
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
