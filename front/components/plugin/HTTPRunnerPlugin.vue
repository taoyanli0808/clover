<template>
  <div>
    <el-upload
      ref="upload"
      :limit="1"
      :file-list="fileList"
      :show-file-list="false"
      :on-exceed="handleExceed"
      :http-request="handleUpload"
      action="null"
      class="upload-demo"
      accept=".json"
      drag
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">请先选择团队与项目</div>
      <div class="el-upload__text">然后将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">开发中，敬请期待...</div>
    </el-upload>
  </div>
</template>

<script>
export default {
  data () {
    return {
      file: '',
      fileList: []
    }
  },
  methods: {
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    handleUpload (params) {
      const formData = new FormData()

      const limit10M = params.file.size / 1024 / 1024 <= 10
      if (!limit10M) {
        // 后续这里处理下，超过10M不再继续走上传逻辑。
        this.$message({
          type: 'warning',
          message: '上传的文件大小应该小于10M!',
          center: true
        })
      }

      formData.append('team', this.team)
      formData.append('project', this.project)
      formData.append('plugin', 'postman')
      formData.append('file', params.file)

      this.$axios.post(
        '/api/v1/plugin/create',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      ).then(function (res) {
        if (res.data.status === 0) {
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
      }).catch(function () {
        this.$message({
          type: 'error',
          message: '服务器偷懒了！',
          center: true
        })
      })
    }
  }
}
</script>

<style scoped>
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

.el-card__header {
  text-align: center;
}
</style>
