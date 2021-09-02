<template>
  <div>
    <el-table
      ref="interface"
      :data="data"
      :height="tableHeight"
      @selection-change="handleSelectionChange"
      v-loading="loading"
      element-loading-text="拼命加载中"
      style="width: 100%; box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)"
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
        label="用例"
        width="180"
        show-overflow-tooltip
      />
      <el-table-column
        prop="method"
        label="方法"
        width="80"
      />
      <el-table-column
        prop="host"
        label="域名"
        width="180"
        show-overflow-tooltip
      />
      <el-table-column
        prop="path"
        label="路径"
        width="180"
        show-overflow-tooltip
      />
      <el-table-column
        prop="created"
        label="创建时间"
        width="180"
      />
      <el-table-column
        prop="updated"
        label="更新时间"
        width="180"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="400"
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
    <el-pagination
      @current-change="handleCurrentChange"
      :total="total"
      background
      layout="total, prev, pager, next, jumper"
    />
    <el-dialog :visible.sync="dialogFormVisible" title="运行接口">
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
      this.tableHeight = window.innerHeight - this.$refs.interface.$el.offsetTop - 100
    })
  },
  methods: {
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    changeSwitch (row) {
      this.$axios({
        url: '/api/v1/interface/switch',
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
        .post('/api/v1/interface/search', params)
        . then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
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
      this.loading = false
    },
    handleRun (index, row) {
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
        url: '/api/v1/interface/trigger',
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
    handleEdit (index, row) {
      this.$router.push({
        path: '/interface/edit',
        query: {
          id: row.id
        }
      })
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
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
            message: '删除成功!',
            center: true
          })
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
    }
  }
}
</script>
