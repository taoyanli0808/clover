<template>
  <div class="container">
    <el-timeline v-for="log in logs" :key="log.name">
      <el-timeline-item placement="top">
        <el-card>
          <div class="title">
            <h3>{{ log.name }}</h3>
          </div>
          <h4>请求数据</h4>
          <el-table
            :data="log.request"
            :show-header="false"
            style="width: 100%;"
            border
            box-shadow
          >
            <el-table-column
              prop="key"
              width="100"
            />
            <el-table-column
              prop="value"
            />
          </el-table>
          <h4>响应数据</h4>
          <el-tabs v-model="activeResponse" type="border-card">
            <el-tab-pane label="响应码" name="first">
              <pre><code>{{ log.response.status }}</code></pre>
            </el-tab-pane>
            <el-tab-pane label="响应头" name="second">
              <pre><code>{{ log.response.header }}</code></pre>
            </el-tab-pane>
            <el-tab-pane label="响应数据" name="third">
              <pre><code>{{ log.response.json || log.response.content }}</code></pre>
            </el-tab-pane>
          </el-tabs>
          <h4>变量设置</h4>
          <el-tabs v-model="activeResponse" type="border-card">
            <el-tab-pane label="预定义变量" name="first">
              <el-table
                :data="log.variable.default"
                :show-header="false"
                style="width: 100%"
                border
              >
                <el-table-column
                  prop="id"
                  width="100"
                />
                <el-table-column
                  prop="project"
                  width="100"
                />
                <el-table-column
                  prop="team"
                  width="100"
                />
                <el-table-column
                  prop="owner"
                  width="100"
                />
                <el-table-column
                  prop="name"
                  width="200"
                />
                <el-table-column
                  prop="value"
                />
                <el-table-column
                  prop="created"
                  width="200"
                />
                <el-table-column
                  prop="updated"
                  width="200"
                />
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="触发设置变量" name="second">
              <el-table
                :data="log.variable.trigger"
                :show-header="false"
                style="width: 100%"
                border
              >
                <el-table-column
                  prop="name"
                  width="200"
                />
                <el-table-column
                  prop="value"
                />
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="响应提取变量" name="third">
              <el-table
                :data="log.variable.extract"
                :show-header="false"
                style="width: 100%"
                border
              >
                <el-table-column
                  prop="name"
                  width="200"
                />
                <el-table-column
                  prop="value"
                />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-timeline-item>
    </el-timeline>
    <el-button @click="handleDownload" type="primary" class="download">下 载</el-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      logs: [],
      activeResponse: 'first'
    }
  },
  mounted () {
    this.fetch()
  },
  methods: {
    fetch () {
      this.$axios({
        url: '/api/v1/report/log',
        method: 'post',
        data: JSON.stringify({
          id: this.$route.query.id
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          for (const i in res.data.data) {
            this.logs.push({
              name: res.data.data[i].name,
              request: [
                {
                  key: 'url',
                  value: res.data.data[i].url
                },
                {
                  key: 'method',
                  value: res.data.data[i].method
                },
                {
                  key: 'header',
                  value: this.translateData(res.data.data[i].header)
                },
                {
                  key: 'params',
                  value: this.translateData(res.data.data[i].params)
                },
                {
                  key: 'body',
                  value: this.translateData(res.data.data[i].body)
                }
              ],
              response: res.data.data[i].response,
              variable: res.data.data[i].variable
            })
          }
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务出错，请联系管理员',
          center: true
        })
      })
    },
    translateData (data) {
      let result = ''
      for (const key in data) {
        if (key !== '') {
          result += key + ':' + data[key] + '\n'
        }
      }
      return result
    },
    handleDownload () {
      this.download('clover运行日志-' + this.$route.query.id + '.json', JSON.stringify(this.logs, null, 4))
    }
  }
}
</script>

<style scoped>
.container {
  padding-left: 10px;
  padding-right: 80px;
}

h3 {
  padding-top: 5px;
  padding-bottom: 5px;
}

h4 {
  padding-top: 10px;
  padding-bottom: 10px;
}

.el-table .cell {
  white-space: pre-line;
}

.title {
  text-align: center;
}

.download {
  float: right;
}
</style>
