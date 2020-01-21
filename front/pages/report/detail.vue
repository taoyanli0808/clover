<template>
  <div class="container">
    <el-row>
      <h1>{{ data.name || 'Clover测试报告' }}</h1>
    </el-row>
    <el-row>
      <h2>Summary</h2>
    </el-row>
    <el-row>
      <el-col :span="4">
        <div>部门</div>
      </el-col>
      <el-col :span="4">
        <div>{{ data.team }}</div>
      </el-col>
      <el-col :span="4">
        <div>项目</div>
      </el-col>
      <el-col :span="4">
        {{ data.project }}
      </el-col>
      <el-col :span="4">
        <div>类型</div>
      </el-col>
      <el-col :span="4">
        {{ data.type }}
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4">
        <div>Clover平台</div>
      </el-col>
      <el-col :span="4">
        <div>{{ data.platform.clover }}</div>
      </el-col>
      <el-col :span="4">
        <div>Python</div>
      </el-col>
      <el-col :span="4">
        {{ data.platform.python }}
      </el-col>
      <el-col :span="4">
        <div>操作系统</div>
      </el-col>
      <el-col :span="4">
        {{ data.platform.platform }}
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="4">
        <div>开始时间</div>
      </el-col>
      <el-col :span="4">
        <div>{{ data.start }}</div>
      </el-col>
      <el-col :span="4">
        <div>结束时间</div>
      </el-col>
      <el-col :span="4">
        {{ data.end }}
      </el-col>
      <el-col :span="4">
        <div>运行时间</div>
      </el-col>
      <el-col :span="4">
        {{ data.duration }}
      </el-col>
    </el-row>
    <el-row>
      <h2>Detail</h2>
    </el-row>
    <el-row>
      <el-table
        :data="results"
        style="width: 100%"
        border
      >
        <el-table-column
          prop="name"
          label="用例名"
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
          prop="elapsed"
          label="请求时间"
          width="180"
        />
        <el-table-column
          prop="elapsed"
          label="请求时间"
          width="180"
        />
        <el-table-column
          prop="status"
          label="状态"/>
      </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: {
        platform: {},
        detail: {}
      },
      results: []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.$axios
        .post('/api/v1/report/search', { id: this.$route.query.id })
        .then((res) => {
          if (res.data.status === 0) {
            this.data = res.data.data
            for (const name in this.data.detail) {
              for (const index in this.data.detail[name].result) {
                this.results.push({
                  name,
                  start: this.data.detail[name].start,
                  end: this.data.detail[name].end,
                  elapsed: this.data.detail[name].elapsed,
                  status: this.data.detail[name].result[index].status,
                  actual: this.data.detail[name].result[index].actual,
                  expect: this.data.detail[name].result[index].expect,
                  operate: this.data.detail[name].result[index].operate
                })
              }
            }
            console.log(this.results)
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message,
              center: true
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '服务出错，请联系管理员',
            center: true
          })
        })
    }
  }
}
</script>

<style scoped>
.container {
  padding-left: 36px;
  padding-right: 36px;
}
</style>
