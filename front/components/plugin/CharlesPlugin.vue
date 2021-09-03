<template>
  <div>
    <el-row>
      <el-upload
        ref="upload"
        :auto-upload="false"
        :show-file-list="false"
        action="null"
        class="upload-demo"
        style="margin-bottom: 20px;"
        accept=".har"
        drag
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">
          请先将文件拖到此处或<em>点击上传插件文件</em>
        </div>
        <div class="el-upload__text">
          然后选择团队与项目点击“创建接口”
        </div>
        <div slot="tip" class="el-upload__tip">
          Charles仅支持.har文件，且在测试中...<a href="http://github.com/taoyanli0808/clover/issues">反馈问题</a>
        </div>
      </el-upload>
    </el-row>
    <el-row class="plugin">
      <el-col :span="12">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </el-col>
      <el-col :span="12">
        <el-button @click="handleUpload" style="float: right;" size="small" type="primary" plain>创建接口</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader
  },
  data () {
    return {
      team: '',
      project: ''
    }
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    },
    handleUpload () {
      const fileList = this.$refs.upload.uploadFiles
      if (fileList.length === 0) {
        this.$message({
          type: 'warning',
          message: '请选择要上传的插件文件!',
          center: true
        })
        return false
      }

      // 只取最新上传的文件
      const file = fileList[fileList.length - 1].raw
      const limit10M = file.size / 1024 / 1024 <= 10
      if (!limit10M) {
        // 后续这里处理下，超过10M不再继续走上传逻辑。
        this.$message({
          type: 'warning',
          message: '上传的文件大小应该小于10M!',
          center: true
        })
        return false
      }

      if (this.team === '' || this.project === '') {
        this.$message({
          type: 'warning',
          message: '请选择接口所属团队与项目!',
          center: true
        })
        return false
      }

      const formData = new FormData()

      formData.append('team', this.team)
      formData.append('project', this.project)
      formData.append('plugin', 'charles')
      formData.append('file', file)

      const loading = this.$loading({
        text: '插件创建中...',
        spinner: 'el-icon-loading'
      })
      this.$axios.post(
        '/api/v1/plugin/create',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      ).then((res) => {
        loading.close()
        if (res.data.status === 0) {
          if (res.data.data.total === res.data.data.success) {
            this.$confirm(
              '共' + res.data.data.total + '条接口上传成功，是否跳转到接口列表查看？',
              '创建接口插件',
              {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
              this.$router.push({
                path: '/interface/'
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '您选择取消，将停留在插件页面。'
              })
            })
          } else {
            this.$alert(
              '您选择了' + res.data.data.total + '个接口，上传时' + res.data.data.success + '个接口请求成功，上传时' + res.data.data.failed + '个接口请求失败，请关注！',
              '创建接口插件',
              {
                confirmButtonText: '确定',
                callback: (action) => {
                  this.$message({
                    type: 'info',
                    message: '您可以继续创建接口。'
                  })
                }
              })
          }
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
      }).catch((error) => {
        loading.close()
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

<style scope>
.el-card__header {
  text-align: center;
}

.el-card__body {
  text-align: center;
}

.plugin {
  padding-left: 20px;
  padding-right: 20px;
}
</style>
