<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <editor
            ref="keyword"
            v-model="keyword"
            @init="keywordInit"
            lang="python"
            theme="twilight"
            height="480"
          />
        </el-card>
        <el-row class="button">
          <el-col
            :span="3"
            :offset="18"
          >
            <el-button
              @click="debugDialogVisible=true"
              icon="el-icon-video-play"
              type="primary"
              size="mini"
            >
              调试
            </el-button>
          </el-col>
          <el-col
            :span="3"
          >
            <el-button
              @click="submitDialogVisible=true"
              icon="el-icon-plus"
              type="primary"
              size="mini"
            >
              保存
            </el-button>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <p class="result">{{result}}</p>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog
      :visible.sync="debugDialogVisible"
      title="请添加调用表达式"
      width="30%">
      <el-input v-model="expression" placeholder="${function_name(parameter, ...)}" />
      <span slot="footer" class="dialog-footer">
        <el-button @click="debugDialogVisible=false" size="mini">取 消</el-button>
        <el-button @click="handleDebug" type="primary" size="mini">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="submitDialogVisible"
      title="请添加调关键字功能介绍"
      width="30%">
      <el-input v-model="description" type="textarea" placeholder="请填写关键字功能描述..." />
      <span slot="footer" class="dialog-footer">
        <el-button @click="submitDialogVisible=false" size="mini">取 消</el-button>
        <el-button @click="handleSubmit" type="primary" size="mini">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  components: {
    editor: require('vue2-ace-editor')
  },
  data () {
    return {
      id: '',
      keyword: '# 这里使用python写自定义关键字',
      result: '点击调试按钮，这里展示执行结果。',
      expression: '',
      description: '',
      debugDialogVisible: false,
      submitDialogVisible: false
    }
  },
  mounted () {
    this.setKeywordEditor()
    this.loadKeyword()
  },
  methods: {
    loadKeyword () {
      this.$axios
        .post('/api/v1/keyword/search', {
          id: this.$route.query.id
        })
        .then((res) => {
          if (res.data.status === 0) {
            this.id = res.data.data.id
            this.name = res.data.data.name
            this.description = res.data.data.description
            this.keyword = res.data.data.keyword
            const editor = this.$refs.keyword.editor
            editor.setValue(this.keyword)
            const lines = editor.session.getLength()
            editor.gotoLine(lines)
          } else {
            this.$message({
              type: 'error',
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
    handleDebug () {
      this.debugDialogVisible = false
      this.$axios({
        url: '/api/v1/keyword/debug',
        method: 'post',
        data: JSON.stringify({
          'keyword': this.keyword,
          'expression': this.expression
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.result = JSON.stringify(res.data.data)
          this.$message({
            type: 'success',
            message: res.data.message,
            center: true
          })
        } else {
          this.$message({
            type: 'error',
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
    handleSubmit (value) {
      this.submitDialogVisible = false
      this.$axios({
        url: '/api/v1/keyword/update',
        method: 'post',
        data: JSON.stringify({
          'id': this.id,
          'name': this.name,
          'keyword': this.keyword,
          'description': this.description
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.result = JSON.stringify(res.data.data)
          this.$message({
            type: 'success',
            message: res.data.message,
            center: true
          })
        } else {
          this.$message({
            type: 'error',
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
    keywordInit () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/mode/sql')
      require('brace/theme/clouds')
    },
    setKeywordEditor () {
      const editor = this.$refs.keyword.editor
      editor.getSession().setTabSize(4)
      editor.setFontSize(18)
    }
  }
}
</script>

<style scoped>
.button {
  padding-top: 20px;
}

.result {
  min-height: 480px;
}
</style>
