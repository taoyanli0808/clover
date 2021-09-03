<template>
  <div>
    <el-table
      ref="suite"
      :data="data"
      :height="tableHeight"
      v-loading="loading"
      element-loading-text="拼命加载中"
      style="width: 100%; box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="50"
        align="ceDnter"
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
        prop="project"
        label="项目"
        width="180"
        align="center"
      />
      <el-table-column
        prop="name"
        label="名称"
        width="180"
        align="center"
        show-overflow-tooltip
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
        show-overflow-tooltip
      />
      <!-- <el-table-column
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
      </el-table-column> -->
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
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            @change="changeSwitch(scope.row)"
            active-color="#13ce66"
            inactive-color="#999999"
          />
          <el-tooltip :content="'当前状态为可运行'" placement="top">
            <el-button
              @click="handleRun(scope.$index, scope.row)"
              :disabled="scope.row.status===false"
              size="mini"
              icon="el-icon-video-play"
              type="primary"
            >
              运行
            </el-button>
          </el-tooltip>
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
    <el-pagination
      @current-change="handleCurrentChange"
      :total="total"
      background
      layout="total, prev, pager, next, jumper"
    />
    <el-dialog :visible.sync="dialogFormVisible" title="运行套件">
      <el-form>
        <el-form-item label="测试报告名称">
          <el-input v-model="report" autocomplete="off" />
        </el-form-item>
        <el-form-item label="动态替换变量">
          <el-input
            v-model="variables"
            type="textarea"
            placeholder="key:val形式，使用英文;或者换行分隔。"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button @click="runCase" type="primary">
          确定
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

export default {
  props: {
    team: {
      type: String,
      default: ''
    },
    project: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      value: 'true',
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      cases: [],
      column: {},
      report: '',
      variables: '',
      loading: false,
      dialogFormVisible: false,
      tableHeight: 300
    }
  },
  mounted () {
    this.$nextTick(function () {
      this.tableHeight = window.innerHeight - this.$refs.suite.$el.offsetTop - 100
    })
  },
  methods: {
    createSuite () {
      this.$router.push({
        path: '/suite/create'
      })
    },
    changeSwitch (row) {
      this.$axios({
        url: '/api/v1/suite/switch',
        method: 'post',
        data: JSON.stringify({
          id_list: row.id,
          status: row.status
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          if (row.status) {
            this.$message({
              type: 'success',
              message: res.data.message,
              center: true
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message,
              center: true
            })
          }
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
        this.dialogFormVisible = false
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    refresh (data) {
      this.loading = true
      const params = {
        ...data,
        limit: this.limit,
        offset: this.page * this.limit
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
              message: res.data.message,
              center: true
            })
          }
        })
        .catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
      this.loading = false
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    handleHistory (index, row) {
      this.$message({
        message: '开发者正在加班加点开发，很快就可以用喽！',
        type: 'error',
        center: true
      })
    },
    handleRun (index, row, value) {
      this.dialogFormVisible = true
      this.column = row
    },
    runCase () {
      const params = {
        trigger: 'clover',
        report: this.report,
        ...this.column
      }
      if (this.variables) {
        params.variables = []
        const tmpstr = this.variables.replace(/\n/g, ';')
        const variables = tmpstr.split(';')
        for (const index in variables) {
          const separator = variables[index].indexOf(':')
          params.variables.push({
            name: variables[index].slice(0, separator),
            value: variables[index].slice(separator + 1, variables[index].length)
          })
        }
      }
      this.$axios({
        url: '/api/v1/suite/trigger',
        method: 'post',
        data: JSON.stringify(params),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: '运行用例成功!',
            center: true
          })
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
        this.dialogFormVisible = false
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
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
              message: '删除成功!',
              center: true
            })
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              center: true
            })
          }
        })
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    }
  }
}
</script>
