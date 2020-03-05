<template>
  <div class="banner">
    <el-row>
      <el-col :span="8" v-for="item in data" :key="item.title">
        <el-row class="card">
          <el-col :span="12" class="background">
            <el-image
              :src="item.image"
              :alt="item.title"
              class="image"
            />
          </el-col>
          <el-col :span="12" class="content">
            <div><span class="description">{{ item.version || item.name }}</span></div>
            <div><span class="number">{{ item.title }}</span></div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: {
        clover: {
          'title': 'clover',
          'version': '0.1.0',
          'image': require('assets/img/info-clover.jpg')
        },
        python: {
          'title': 'python',
          'version': '3.6',
          'image': require('assets/img/info-python.jpg')
        },
        platform: {
          'title': 'platform',
          'name': 'linux',
          'image': '团队数量'
        }
      }
    }
  },
  mounted () {
    this.info()
  },
  methods: {
    info () {
      this.$axios
        .get('/api/v1/index/info', {})
        .then((res) => {
          if (res.data.status === 0) {
            // 这里获取后端返回的系统和版本信息。
            this.data.clover.version = res.data.data.clover
            this.data.python.version = res.data.data.python
            this.data.platform.name = res.data.data.platform
            // 这里根据不同操作系统类型适配不同图标。
            if (this.data.platform.name === 'darwin') {
              this.data.platform.image = require('assets/img/info-platform-apple.jpg')
            } else if (this.data.platform.name === 'windows') {
              this.data.platform.image = require('assets/img/info-platform-windows.jpg')
            } else if (this.data.platform.name === 'centos') {
              this.data.platform.image = require('assets/img/info-platform-centos.jpg')
            } else if (this.data.platform.name === 'ubuntu') {
              this.data.platform.image = require('assets/img/info-platform-ubuntu.jpg')
            } else if (this.data.platform.name === 'redhat') {
              this.data.platform.image = require('assets/img/info-platform-redhat.jpg')
            } else {
              this.data.platform.image = require('assets/img/info-platform.jpg')
            }
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              center: true
            })
          }
        }).catch((res) => {
          this.$message({
            type: 'error',
            message: '服务异常，请联系管理员！',
            center: true
          })
        })
    }
  }
}
</script>

<style scoped>
.banner {
  background-color: #F2F2F2;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-top: -20px;
  margin-left: -20px;
  margin-right: -20px;
}

.card {
  padding-left: 10px;
  padding-right: 10px;
}

.background {
  max-height: 100px;
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: #FFFFFF;
}

.image {
  width: 80px;
  height: 80px;
  border-radius: 5px 0 0 5px;
}

.content {
  border-radius: 0 5px 5px 0;
  background-color: #FFFFFF;
}

.number {
  font-size: 14px;
  line-height: 30px;
}

.description {
  font-size: 48px;
  line-height: 70px;
  background-color: #FFFFFF;
}
</style>
