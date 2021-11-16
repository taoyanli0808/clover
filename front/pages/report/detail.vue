<template>
  <div class="container">
    <el-row>
      <div class="report">
        {{ data.name || 'Clover测试报告' }}
      </div>
    </el-row>
    <el-row>
      <div class="title">
        汇总
      </div>
    </el-row>
    <el-row>
      <el-table
        :data="headers"
        :show-header="false"
        style="width: 100%"
        border
      >
        <el-table-column
          prop="hc1"
          min-width="16.66%"
        />
        <el-table-column
          prop="hc2"
          min-width="16.66%"
        />
        <el-table-column
          prop="hc3"
          min-width="16.66%"
        />
        <el-table-column
          prop="hc4"
          min-width="16.66%"
        />
        <el-table-column
          prop="hc5"
          min-width="16.66%"
        />
        <el-table-column
          prop="hc6"
          min-width="16.66%"
        />
      </el-table>
    </el-row>
    <el-row>
      <div class="title">
        断言
      </div>
    </el-row>
    <el-row>
      <el-table
        :data="results"
        :row-class-name="tableRowClassName"
        style="width: 100%"
        border
      >
        <el-table-column
          type="expand"
        >
          <template slot-scope="props">
            <InterfaceRunDetail v-bind:log="props.row" />
          </template>
        </el-table-column>
        <el-table-column
          prop="interface_name"
          label="接口名"
        />
        <el-table-column
          prop="start"
          label="开始时间"
        />
        <el-table-column
          prop="end"
          label="结束时间"
        />
        <el-table-column
          prop="performance.elapsed"
          label="接口耗时"
        />
        <el-table-column
          prop="performance.threshold"
          label="时间基准"
        />
        <el-table-column
          prop="validator.status"
          label="断言结果"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.validator.status === '通过' ? 'success' : 'danger'"
              disable-transitions
            >
              {{ scope.row.validator.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="performance.status"
          label="性能结果"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.performance.status === '通过' ? 'success' : 'danger'"
              disable-transitions
            >
              {{ scope.row.performance.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import InterfaceRunDetail from '~/components/report/InterfaceRunDetail.vue'

export default {
  components: {
    InterfaceRunDetail
  },
  data () {
    return {
      data: {
        platform: {
        }
      },
      headers: [],
      results: [],
      total: 0,
      success: 0,
      failed: 0,
      error: 0,
      skip: 0,
      percent: 0.0,
      fail_or_error: false
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.base_infomation()
      this.validator_and_performance()
    },
    base_infomation () {
      this.$axios
        .post('/api/v1/report/search', { id: this.$route.query.id })
        .then((res) => {
          if (res.data.status === 0) {
            this.data = res.data.data
            this.total = this.data.interface.total
            this.success = this.data.interface.passed
            this.failed = this.data.interface.failed
            this.error = this.data.interface.error
            this.skip = this.data.interface.skiped
            this.percent = this.data.interface.percent.toFixed(0) + '%'
            this.headers.push({
              hc1: '部门',
              hc2: this.data.team,
              hc3: '项目',
              hc4: this.data.project,
              hc5: '类型',
              hc6: this.data.type
            })
            this.headers.push({
              hc1: 'Clover平台',
              hc2: this.data.platform.clover,
              hc3: 'Python',
              hc4: this.data.platform.python,
              hc5: '操作系统',
              hc6: this.data.platform.platform
            })
            this.headers.push({
              hc1: '开始时间',
              hc2: this.data.start,
              hc3: '结束时间',
              hc4: this.data.end,
              hc5: '持续时间(ms)',
              hc6: this.data.duration
            })
            this.headers.push({
              hc1: '全部',
              hc2: '成功',
              hc3: '失败',
              hc4: '错误',
              hc5: '跳过',
              hc6: '通过率'
            })
            this.headers.push({
              hc1: this.total,
              hc2: this.success,
              hc3: this.failed,
              hc4: this.error,
              hc5: this.skip,
              hc6: this.percent
            })
            if ((this.success + this.skip) !== this.total) {
              this.$message({
                type: 'error',
                message: '测试报告中检测到断言失败或错误，请关注！',
                center: true,
                offset: 160
              })
            }
          } else {
            this.$message({
              type: 'warning',
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
    },
    validator_and_performance () {
      this.$axios({
        url: '/api/v1/log/search',
        method: 'post',
        data: JSON.stringify({
          id: this.$route.query.id,
          logid: this.$route.query.logid
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.results = res.data.data
          this.resultHandler(this.results)
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
          message: error,
          center: true
        })
      })
    },
    resultHandler (results) {
      for (const i in results) {
        if (results[i].validator.status === 'passed') {
          results[i].validator.status = '通过'
        } else {
          results[i].validator.status = '失败'
        }
        if (results[i].performance.status === 'passed') {
          results[i].performance.status = '通过'
        } else {
          results[i].performance.status = '失败'
        }
        results[i].response.data = JSON.parse(results[i].response.data)
      }
    },
    tableRowClassName ({ row, rowIndex }) {
      if (row.validator.status === '通过') {
        return 'success'
      } else {
        return 'danger'
      }
    }
  }
}
</script>

<style scoped>
.container {
  padding-left: 36px;
  padding-right: 36px;
}

.report {
  padding-top: 20px;
  padding-bottom: 20px;
  font-size: 36px;
  text-align: center;
}

.title {
  padding-top: 20px;
  padding-bottom: 20px;
  font-size: 20px;
}
</style>
