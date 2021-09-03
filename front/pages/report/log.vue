<template>
  <div class="container">
    <div class="block">
      <el-timeline>
        <el-timeline-item
          v-for="log in logs"
          :key="log.index"
          :timestamp="log.time"
          hide-timestamp="true"
        >
          <el-card>
            <p :style="log.color">{{log.time + ' - ' + log.level + ' - ' + log.step + ' - ' + log.message}}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
    <!-- <el-button @click="handleDownload" type="primary" class="download">
      下 载
    </el-button> -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      logs: []
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
          for (const i in res.data.data.logs) {
            this.logs.push(
              {
                ...res.data.data.logs[i],
                index: i,
                type: this.setColor(res.data.data.logs[i].level)
              }
            )
          }
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
    },
    handleDownload () {
      this.download('clover运行日志-' + this.$route.query.id + '.log', this.logs)
    },
    setColor (level) {
      switch (level) {
        case 'error':
          return { 'background-color': '#F56C6C' }
        case 'warn':
          return { 'background-color': '#E6A23C' }
        case 'info':
          return { 'background-color': '#67C23A' }
        default:
          return { 'background-color': '#909399' }
      }
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
