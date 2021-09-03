<template>
  <div>
    <el-row v-for="(suites, index) in suites" :key="index" :gutter="20" class="row">
      <el-col :md="6" :lg="6" :xl="4" v-for="suite in suites" :key="suite.id">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>
              套件ID：{{ suite.id }}
            </span>
          </div>
          <div class="card-item">
            <div class="item">
              套件：{{ longText(suite.name) }}
            </div>
            <div class="item">
              团队：{{ suite.team }}
            </div>
            <div class="item">
              项目：{{ suite.project }}
            </div>
            <div class="item">
              接口：{{ count(suite.cases) }}
            </div>
            <div class="item">
              创建：{{ suite.created }}
            </div>
            <div class="item">
              更新：{{ suite.updated }}
            </div>
          </div>
          <div class="operate">
            <div style="float: left; padding: 3px 0; display: inline;">
              <el-switch
                v-model="suite.status"
                @change="changeSwitch(suite)"
                active-color="success"
                inactive-color="info"
              />
            </div>
            <div style="float: right; padding: 3px 0" type="text">
              <el-button @click="handleRun(suite)" type="success" icon="el-icon-video-play" size="mini" circle />
              <el-button @click="handleEdit(suite)" type="primary" icon="el-icon-edit" size="mini" circle />
              <el-button @click="handleDelete(suite)" type="danger" icon="el-icon-delete" size="mini" circle />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-pagination
      @current-change="handleCurrentChange"
      :total="total"
      :page-size="24"
      :pager-count="11"
      layout="total, prev, pager, next, jumper"
      background
    />
    <el-dialog :visible.sync="visible" title="运行套件">
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
        <el-button @click="visible = false">
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
  data () {
    return {
      total: 0,
      page: 0,
      limit: 24,
      dataPerRow: 6,
      suite: {},
      suites: [],
      report: '',
      variables: '',
      visible: false
    }
  },
  computed: {
    longText () {
      return function (data) {
        const number = window.screen.width < 1920 ? 18 : 12
        return data.length > number ? data.substr(0, number) + '...' : data
      }
    },
    count () {
      return function (data) {
        return data.length
      }
    },
    team () {
      return this.$store.state.team
    },
    project () {
      return this.$store.state.project
    },
    caseName () {
      return this.$store.state.caseName
    }
  },
  mounted () {
    this.search()
  },
  methods: {
    search () {
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
      if (this.caseName !== '') {
        params.caseName = this.caseName
      }
      this.$axios
        .post('/api/v1/suite/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.suites = []
            this.total = res.data.total
            const len = res.data.data.length
            const number = window.screen.width < 1920 ? 4 : 6
            const line = len % number === 0 ? len / number : Math.floor((len / number) + 1)
            for (let i = 0; i < line; i++) {
              const temp = res.data.data.slice(i * number, i * number + number)
              this.suites.push(temp)
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
    changeSwitch (suite) {
      this.$axios({
        url: '/api/v1/suite/switch',
        method: 'post',
        data: JSON.stringify({
          id_list: suite.id,
          status: suite.status
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          if (suite.status) {
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
    handleRun (suite) {
      this.visible = true
      this.suite = suite
    },
    runCase () {
      const params = {
        trigger: 'clover',
        report: this.report,
        ...this.suite
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
        this.visible = false
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    handleEdit (suite) {
      this.$router.push({
        path: '/suite/edit',
        query: {
          id: suite.id
        }
      })
    },
    handleDelete (suite) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$axios({
          url: '/api/v1/suite/delete',
          method: 'post',
          data: JSON.stringify({
            id_list: [suite.id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          if (res.data.status === 0) {
            this.search()
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
    handleCurrentChange (value) {
      this.page = value - 1
      this.search()
    }
  }
}
</script>

<style scoped>
.row {
  margin-bottom: 20px;
}

.text {
    font-size: 14px;
  }

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
.box-card {
  width: 100%;
  box-shadow: 0 -5px orange;
}

.caed-item {
  display: block;
  font-size: 14px;
}

.item {
  margin-bottom: 3px;
}

.operate {
  padding-top: 17px;
  padding-bottom: 20px;
}
</style>
