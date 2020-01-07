<template>
  <div>
    <el-row>
      <el-col :span="4">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </el-col>
      <el-col :span="2" :offset="18">
        <el-button
          @click="createSuite"
          type="primary"
          plain
        >
          创建套件
        </el-button>
      </el-col>
    </el-row>
    <el-table
      :data="data"
      @selection-change="handleSelectionChange"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="180"
      />
      <el-table-column
        prop="team"
        label="团队"
        width="180"
      />
      <el-table-column
        prop="name"
        label="用例"
        width="180"
      />
      <el-table-column
        prop="method"
        label="方法"
        width="80"
      />
      <el-table-column
        prop="name"
        label="用例"
        width="180"
      />
      <el-table-column
        prop="host"
        label="域名"
        width="180"
      />
      <el-table-column
        prop="path"
        label="路径"
        width="180"
      />
      <el-table-column
        prop="created"
        label="创建时间"
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
            @click="handleAdd(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-plus"
            type="primary"
          >
            添加
          </el-button>
          <el-button
            @click="handleEdit(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-edit"
            type="warning"
          >
            编辑
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
import Sortable from 'sortablejs'
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
    document.body.ondrop = function (event) {
      event.preventDefault()
      event.stopPropagation()
    }
    this.rowDrop()
  },
  methods: {
    rowDrop () {
      const tbody = document.querySelector('.el-table__body-wrapper tbody')
      const _this = this
      Sortable.create(tbody, {
        onEnd ({ newIndex, oldIndex }) {
          const currRow = _this.data.splice(oldIndex, 1)[0]
          _this.data.splice(newIndex, 0, currRow)
        }
      })
    },
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
        .post('/api/v1/interface/search', params)
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
    handleAdd (index, row) {
      this.$router.push({
        path: '/interface/create'
      })
    },
    handleEdit (index, row) {
      this.$message({
        showClose: true,
        message: '付费功能，暂不开放！',
        type: 'error'
      })
      /*
      this.$router.push({
        path: '/interface/edit'
      })
      */
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        console.log(row.id)
        this.$axios({
          url: '/api/v1/interface/delete',
          method: 'post',
          data: JSON.stringify({
            id_list: [row.id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          this.refresh()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
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
    },
    handleSelectionChange (value) {
      const index = []
      value.forEach((val, idx) => {
        this.data.forEach((v, i) => {
          if (val.id === v.id) {
            index.push(i)
          }
        })
      })
      this.cases = []
      const temp = index.sort()
      for (const i in temp) {
        this.cases.push(this.data[temp[i]].id)
      }
    },
    createSuite (value) {
      this.$axios({
        url: '/api/v1/suite/create',
        method: 'post',
        data: JSON.stringify({
          'team': this.team,
          'project': this.project,
          'type': 'interface',
          'cases': this.cases
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: res.data.message
          })
        } else {
          this.$message({
            type: 'error',
            message: res.data.message
          })
        }
      })
    }
  }
}
</script>
