<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="3">
        <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
          ref="snippet"
          v-model="content"
          @init="snippetInit"
          lang="python"
          theme="twilight"
          height="480"
        />
      </el-col>
      <el-col :span="12">
        <editor
          ref="mock"
          v-model="data"
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
      content: '# 这里使用python写自定义关键字',
      data: '{"status": 0, "message": "ok", "data": {}}'
    }
  },
  mounted () {
    this.setSnippetEditor()
    this.setMockEditor()
  },
  methods: {
    handleDebug () {
      console.log(this.content)
    },
    handleAdd (value) {
      console.log(value)
    },
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    },
    snippetInit () {
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
    setSnippetEditor () {
      const editor = this.$refs.snippet.editor
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
