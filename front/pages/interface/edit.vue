<template>
  <div class="container">
    <el-row>
      <h1>Interface</h1>
    </el-row>
    <el-row>
      <el-col :span="10">
        <el-input
          v-model="host"
          placeholder="https://github.com"
          class="input-with-select"
          clearable
        >
          <template slot="prepend">
            <el-select
              slot="prepend"
              @change="selectMethod"
              v-model="method"
              placeholder="请求方法"
              style="width:120px;"
              clearable
            >
              <el-option
                v-for="m in methods"
                :key="m"
                :label="m"
                :value="m"
              />
            </el-select>
          </template>
        </el-input>
      </el-col>
      <el-col :span="12">
        <el-input
          v-model="path"
          placeholder="/taoyanli0808/clover"
          clearable
        />
      </el-col>
      <el-col
        :span="2"
        style="text-align: right;"
      >
        <el-button
          @click="dialogSubmitFormVisible=true"
          type="primary"
        >
          保存
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <h1>Request</h1>
    </el-row>
    <el-row :gutter="20">
      <el-tabs
        v-model="activeName"
      >
        <el-tab-pane label="请求头信息" name="first">
          <el-input
            v-model="header"
            :autosize="minsize"
            type="textarea"
            placeholder="请输入请求头信息,key:value形式，使用换行分隔参数。"
            show-word-limit
          />
        </el-tab-pane>
        <el-tab-pane label="请求参数" name="second">
          <el-input
            v-model="params"
            :autosize="minsize"
            type="textarea"
            placeholder="请输入请求参数,key:value形式，使用换行分隔参数。一般情况下请求参数会拼接成url，例如http://52clover.cn/s?a=1&b=2"
            show-word-limit
          />
        </el-tab-pane>
        <el-tab-pane label="请求体" name="third">
          <el-select v-model="body.mode" placeholder="请选择">
            <el-option
              v-for="type in bodyType"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
          <el-input
            v-model="body.data"
            :autosize="minsize"
            type="textarea"
            placeholder="请输入请求体,key:value形式，使用换行分隔参数。一般情况下请求体是表单数据。"
            show-word-limit
          />
        </el-tab-pane>
        <el-tab-pane label="添加断言" name="fourth">
          <el-table
            ref="assertTable"
            :data="assert"
            @row-click="currentAssertTableChange"
            class="tb-edit"
            style="width: 100%"
            highlight-current-row
            border
          >
            <el-table-column
              label="EXTRACTOR"
              min-width="16%"
              align="left"
            >
              <template scope="scope">
                <el-select v-model="scope.row.extractor" placeholder="请选择">
                  <el-option
                    label="jemspath"
                    value="jemspath"
                  />
                  <el-option
                    label="delimiter"
                    value="delimiter"
                  />
                  <el-option
                    label="regular"
                    value="regular"
                  />
                </el-select>
                <span>
                  {{ scope.row.extractor }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="EXPRESSION"
              min-width="17%"
              align="left"
            >
              <template scope="scope">
                <el-input
                  v-model="scope.row.expression"
                  size="small"
                  placeholder="请输入内容"
                />
                <span>
                  {{ scope.row.expression }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="COMPARATOR"
              min-width="16%"
              align="left"
            >
              <template scope="scope">
                <el-select v-model="scope.row.comparator" placeholder="请选择">
                  <el-option
                    label="等于"
                    value="equal"
                  />
                  <el-option
                    label="不等于"
                    value="not_equal"
                  />
                  <el-option
                    label="包含"
                    value="contain"
                  />
                  <el-option
                    label="不包含"
                    value="not_contain"
                  />
                  <el-option
                    label="大于"
                    value="greater"
                  />
                  <el-option
                    label="大于等于"
                    value="not_less"
                  />
                  <el-option
                    label="小于"
                    value="less"
                  />
                  <el-option
                    label="小于等于"
                    value="not_greater"
                  />
                </el-select>
                <span>
                  {{ scope.row.comparator }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="EXPECTED"
              min-width="16%"
              align="left"
            >
              <template scope="scope">
                <el-input
                  v-model="scope.row.expected"
                  size="small"
                  placeholder="请输入内容"
                />
                <span>
                  {{ scope.row.expected }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="CONVERTOR"
              min-width="16%"
              align="left"
            >
              <template scope="scope">
                <el-select v-model="scope.row.convertor" placeholder="请选择">
                  <el-option
                    label="string"
                    value="str"
                  />
                  <el-option
                    label="int"
                    value="int"
                  />
                  <el-option
                    label="float"
                    value="float"
                  />
                  <el-option
                    label="boolean"
                    value="boolean"
                  />
                </el-select>
                <span>
                  {{ scope.row.convertor }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              align="center"
              min-width="16%"
              fixed="right"
            >
              <template scope="scope">
                <el-button
                  @click="addAssertTableRow(scope.$index, scope.row)"
                  size="small"
                  type="primary"
                >
                  添加
                </el-button>
                <el-button
                  @click="deleteAssertTableRow(scope.$index, scope.row)"
                  size="small"
                  type="danger"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="提取响应" name="five">
          <el-table
            ref="extractTable"
            :data="extract"
            class="tb-edit"
            style="width: 100%"
            highlight-current-row
            border
          >
            <el-table-column
              label="SELECTOR"
              min-width="25%"
              align="left"
            >
              <template scope="scope">
                <el-select v-model="scope.row.selector" placeholder="请选择">
                  <el-option
                    v-for="item in selectors"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
                <span>
                  {{ scope.row.selector }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="EXPRESSION"
              min-width="25%"
              align="left"
            >
              <template scope="scope">
                <el-input
                  v-model="scope.row.expression"
                  size="small"
                  placeholder="请输入内容"
                />
                <span>
                  {{ scope.row.expression }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="VARIABLE"
              min-width="25%"
              align="left"
            >
              <template scope="scope">
                <el-input
                  v-model="scope.row.variable"
                  size="small"
                  placeholder="请输入内容"
                />
                <span>
                  {{ scope.row.variable }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              min-width="25%"
              align="center"
            >
              <template scope="scope">
                <el-button
                  @click="addExtractTableRow(scope.$index, scope.row)"
                  size="small"
                  type="primary"
                >
                  添加
                </el-button>
                <el-button
                  @click="deleteExtractTableRow(scope.$index, scope.row)"
                  size="small"
                  type="danger"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="高级设置" name="six">
          <el-form ref="form" label-width="80px">
            <el-form-item label="超时时间">
              <el-input v-model="timeout" />
            </el-form-item>
            <el-form-item label="重试次数">
              <el-input v-model="retry" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    <el-row>
      <h1>Response</h1>
    </el-row>
    <el-row>
      <el-tabs v-model="activeResponseTab">
        <el-tab-pane label="响应体" name="responseBody">
          <pre><code>{{ response.json || response.content }}</code></pre>
        </el-tab-pane>
        <el-tab-pane label="响应头" name="responseHeader">
          <pre><code>{{ response.header }}</code></pre>
        </el-tab-pane>
        <el-tab-pane label="响应Cookie" name="responseCookie">
          <pre><code>{{ cookie }}</code></pre>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    <el-dialog :visible.sync="dialogSubmitFormVisible" title="提交接口">
      <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
      <el-form>
        <el-form-item label="用例名称">
          <el-input v-model="name" autocomplete="off" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogSubmitFormVisible = false">
          取消
        </el-button>
        <el-button @click="submit" type="primary">
          确定
        </el-button>
      </div>
    </el-dialog>
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
      teams: [],
      projects: [],
      methods: ['get', 'post', 'put', 'delete'],
      activeName: 'first',
      activeResponseTab: 'responseBody',
      selectors: [{
        label: 'jemspath',
        value: 'jemspath'
      },
      {
        label: '分隔符',
        value: 'delimiter'
      },
      {
        label: '正则',
        value: 're'
      }],
      bodyType: [{
        label: 'formdata',
        value: 'formdata'
      }, {
        label: 'urlencoded',
        value: 'urlencoded'
      }, {
        label: 'raw',
        value: 'raw'
      }],
      response: '',
      cookie: '',
      id: '',
      team: '',
      project: '',
      name: '',
      host: '',
      path: '',
      method: '',
      header: '',
      params: '',
      body: {
        'mode': 'raw',
        'data': ''
      },
      retry: 1,
      timeout: 120,
      assert: [{
        extractor: '',
        expression: '',
        comparator: '',
        convertor: '',
        expected: ''
      }],
      extract: [{
        selector: '',
        expression: '',
        varibale: ''
      }],
      minsize: { minRows: 6 },
      dialogSubmitFormVisible: false
    }
  },
  mounted () {
    this.fetch()
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    },
    selectMethod (value) {
      this.method = value
    },
    addHeaderTableRow (index, row) {
      this.header.push({
        key: '',
        value: ''
      })
      const last = this.$refs.headerTable.data.length
      const currentRow = this.$refs.headerTable.data[last]
      this.$refs.headerTable.setCurrentRow(currentRow)
    },
    deleteHeaderTableRow (index, row) {
      this.header = this.header.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.header) && this.header.length === 0) {
        this.header.push({
          key: '',
          value: ''
        })
      }
    },
    addParameterTableRow (index, row) {
      this.param.push({
        key: '',
        value: ''
      })
    },
    deleteParameterTableRow (index, row) {
      this.param = this.param.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.param) && this.param.length === 0) {
        this.param.push({
          key: '',
          value: ''
        })
      }
    },
    addBodyTableRow (index, row) {
      this.body.data.push({
        key: '',
        value: ''
      })
    },
    deleteBodyTableRow (index, row) {
      this.body.data = this.body.data.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.body.data) && this.body.data.length === 0) {
        this.body.data.push({
          key: '',
          value: ''
        })
      }
    },
    currentAssertTableChange (row, event, column) {
    },
    addAssertTableRow (index, row) {
      this.assert.push({
        extractor: '',
        expression: '',
        comparator: '',
        convertor: '',
        expected: ''
      })
    },
    deleteAssertTableRow (index, row) {
      this.assert = this.assert.filter((item, idx) => idx !== index)
      if (Array.prototype.isPrototypeOf(this.assert) && this.assert.length === 0) {
        this.assert.push({
          extractor: '',
          expression: '',
          comparator: '',
          convertor: '',
          expected: ''
        })
      }
    },
    addExtractTableRow (index, row) {
      this.extract.push({
        selector: '',
        expression: '',
        variabel: ''
      })
      const last = this.$refs.extractTable.data.length
      const currentRow = this.$refs.extractTable.data[last]
      this.$refs.extractTable.setCurrentRow(currentRow)
    },
    deleteExtractTableRow (index, row) {
      this.extract = this.extract.filter((item, idx) => idx !== index)
      if (Array.prototype.isPrototypeOf(this.extract) && this.extract.length === 0) {
        this.extract.push({
          selector: '',
          expression: '',
          expected: ''
        })
      }
    },
    translateData (data) {
      const result = []
      const variables = data.split('\n')
      for (const index in variables) {
        // remove empty string
        if (variables[index] === '') {
          continue
        }
        const sep = variables[index].indexOf(':')
        result.push({
          key: variables[index].slice(0, sep),
          value: variables[index].slice(sep + 1, variables[index].length)
        })
      }
      return result
    },
    translateBody (data) {
      if (data.mode === 'formdata' || data.mode === 'urlencoded') {
        const result = []
        const newData = { ...data }
        const variables = data.data.split('\n')
        for (const index in variables) {
          // remove empty string
          if (variables[index] === '') {
            continue
          }
          const sep = variables[index].indexOf(':')
          result.push({
            key: variables[index].slice(0, sep),
            value: variables[index].slice(sep + 1, variables[index].length)
          })
        }
        newData.data = result
        return newData
      } else if (data.mode === 'file') { // mode === 'file'
        return data
      } else { // mode === 'raw'
        return data
      }
    },
    translateVerify (data) {
      return data.filter(item => item.extractor !== '')
    },
    translateExtract (data) {
      return data.filter(item => item.selector !== '')
    },
    update () {
      this.$axios({
        url: '/api/v1/interface/update',
        method: 'post',
        data: JSON.stringify({
          id: this.id,
          team: this.team,
          project: this.project,
          name: this.name,
          host: this.host,
          path: this.path,
          method: this.method,
          header: this.translateData(this.header),
          params: this.translateData(this.params),
          body: this.translateBody(this.body),
          verify: this.translateVerify(this.assert),
          extract: this.translateExtract(this.extract),
          timeout: this.timeout,
          retry: this.retry
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: '提交成功',
            center: true
          })
          this.id = res.data.data.id
          this.team = res.data.data.team
          this.project = res.data.data.project
          this.name = res.data.data.name
          this.host = res.data.data.host
          this.path = res.data.data.path
          this.method = res.data.data.method
          this.cookie = this.getcookie(res.data.data.response.header)
          this.header = this.untranslateData(res.data.data.header)
          this.params = this.untranslateData(res.data.data.params)
          this.body = this.untranslateBody(res.data.data.body)
          this.assert = this.untranslateVerify(res.data.data.verify)
          this.extract = this.untranslateExtract(res.data.data.extract)
          this.response = res.data.data.response
          this.timeout = res.data.data.timeout
          this.retry = res.data.data.retry
        } else {
          this.$message({
            type: 'info',
            message: res.data.message,
            center: true
          })
          this.response = res.data.data
        }
        this.dialogSubmitFormVisible = false
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    submit () {
      if (this.id === '') {
        this.create()
      } else {
        this.update()
      }
    },
    untranslateData (data) {
      let result = ''
      for (const i in data) {
        if (data[i].key !== '') {
          result += data[i].key + ':' + data[i].value + '\n'
        }
      }
      return result
    },
    getcookie (data) {
      let result = ''
      for (const key in data) {
        if (key.match('Cookie')) {
          result = key + ':' + data[key] + '\n'
        }
      }
      return result
    },
    untranslateBody (data) {
      /*
      * 由于页面展示body数据使用的是areatext，因此如果数据格式是
      * formdata或urlencoded需要转换为\n分割的字符串格式以便显示
      * 如果格式是file，暂时为定义处理方式，暂不支持
      * 如果数据格式是raw则直接展示，默认情况下格式为raw
      */
      switch (data.mode) {
        case 'formdata':
          const formdata = []
          for (const i in data.data) {
            const item = data.data[i].key + ':' + data.data[i].value
            formdata.push(item)
          }
          data.data = formdata.join('\n')
          break
        case 'urlencoded':
          const urlencoded = []
          for (const i in data.data) {
            const item = data.data[i].key + ':' + data.data[i].value
            urlencoded.push(item)
          }
          data.data = urlencoded.join('\n')
          break
        case 'file':
          break
        default:
          data.mode = data.mode || 'raw'
          data.data = data.data || ''
          break
      }
      return data
    },
    untranslateVerify (data) {
      if (Array.prototype.isPrototypeOf(data) && data.length === 0) {
        data = [
          {
            'expected': '',
            'convertor': '',
            'extractor': '',
            'comparator': '',
            'expression': ''
          }
        ]
        return data
      } else {
        return data
      }
    },
    untranslateExtract (data) {
      if (Array.prototype.isPrototypeOf(data) && data.length === 0) {
        data = [
          {
            'selector': '',
            'variable': '',
            'expression': ''
          }
        ]
        return data
      } else {
        return data
      }
    },
    fetch () {
      this.$axios
        .post('/api/v1/interface/search', {
          id: this.$route.query.id
        })
        .then((res) => {
          if (res.data.status === 0) {
            this.id = res.data.data.id
            this.team = res.data.data.team
            this.project = res.data.data.project
            this.name = res.data.data.name
            this.host = res.data.data.host
            this.path = res.data.data.path
            this.method = res.data.data.method
            this.header = this.untranslateData(res.data.data.header)
            this.params = this.untranslateData(res.data.data.params)
            this.body = this.untranslateBody(res.data.data.body)
            this.assert = this.untranslateVerify(res.data.data.verify)
            this.extract = this.untranslateExtract(res.data.data.extract)
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              center: true
            })
          }
          this.loading = false
        })
        .catch((error) => {
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

<style scoped>
.container {
  padding-left: 100px;
  padding-right: 100px;
}

.el-row {
  padding-top: 20px;
  padding-bottom: 20px;
}

h1 {
  margin-bottom: -20px;
}

.el-select {
  width: 100%;
}

.input-with-select .el-input-group__prepend {
  width: 130px;
  background-color: #fff;
}

.tb-edit .el-input {
  display: none
}

.tb-edit .current-row .el-input {
  display: block
}

.tb-edit .current-row .el-input+span {
  display: none
}

.tb-edit .el-select {
  display: none
}

.tb-edit .current-row .el-select {
  display: block
}

.tb-edit .current-row .el-select+span {
  display: none
}
</style>
