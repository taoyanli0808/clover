<template>
  <div>
    <TeamProjectCascader  v-on:selectedTeamProject="selectedTeamProject" />
    <el-select v-model="plugin" @change="changePlugin" placeholder="请选择插件">
      <el-option label="postman" value="postman" />
    </el-select>
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
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传postman集合文件</div>
    </el-upload>
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
      project: '',
      plugin: '',
      file: '',
      fileList: []
    }
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    },
    changePlugin (value) {
      this.plugin = value
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    handleUpload (params) {
      console.log(params)

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
      formData.append('plugin', this.plugin)
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
