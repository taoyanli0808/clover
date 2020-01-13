<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="3">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      </el-col>
      </el-col>
      <el-col
        :span="3"
        :offset="15"
      >
        <el-button
          @click="handleDebug"
          icon="el-icon-video-play"
          type="primary"
        >
          调试
        </el-button>
      </el-col>
      <el-col
        :span="3"
      >
        <el-button
          @click="handleAdd"
          icon="el-icon-plus"
          type="primary"
        >
          创建
        </el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <editor
          ref="keyword"
          v-model="keyword"
          @init="keywordInit"
          lang="python"
          theme="twilight"
          height="480"
        />
      </el-col>
      <el-col :span="12">
        <editor
          ref="mock"
          v-model="mock"
          @init="mockInit"
          lang="json"
          theme="twilight"
          height="480"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader,
    editor: require('vue2-ace-editor')
  },
  data () {
    return {
      team: '',
      project: '',
      keyword: '# 这里使用python写自定义关键字',
      mock: '{"status": 0, "message": "ok", "data": {}}'
    }
  },
  mounted () {
    this.setKeywordEditor()
    this.setMockEditor()
  },
  methods: {
    handleDebug () {
      this.$axios({
        url: '/api/v1/keyword/debug',
        method: 'post',
        data: JSON.stringify({
          'team': this.team,
          'project': this.project,
          'keyword': this.keyword,
          'mock': this.mock
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.mock = JSON.stringify(res.data.data)
          this.$message({
            type: 'success',
            message: res.data.message
          })
        } else {
          this.$message({
            type: 'error',
            message: res.data.message
          })
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务器偷懒了！'
        })
      })
    },
    handleAdd (value) {
      console.log(value)
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    },
    keywordInit () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/mode/sql')
      require('brace/theme/twilight')
    },
    mockInit () {
      require('brace/ext/language_tools')
      require('brace/mode/json')
      require('brace/theme/twilight')
    },
    setKeywordEditor () {
      const editor = this.$refs.keyword.editor
      editor.getSession().setTabSize(4)
      editor.setFontSize(18)
    },
    setMockEditor () {
      const editor = this.$refs.mock.editor
      editor.getSession().setTabSize(4)
      editor.setFontSize(18)
    }
  }
}
</script>

<style scoped>

</style>
