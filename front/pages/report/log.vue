<template>
  <div class="container">
    <pre>{{ logs }}</pre>
    <el-button @click="handleDownload" type="primary" class="download">
      下 载
    </el-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      logs: ''
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
          this.logs = res.data.data
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务出错，请联系管理员',
          center: true
        })
      })
    },
    handleDownload () {
      this.download('clover运行日志-' + this.$route.query.id + '.log', this.logs)
    }
  }
}
</script>

<style scoped>
.container {
  padding-left: 10px;
  padding-right: 80px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.download {
  float: right;
}
</style>
