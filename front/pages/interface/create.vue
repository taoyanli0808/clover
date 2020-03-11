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
          提 交
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
          Cookie
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
        label: '分隔符',
        value: 'delimiter'
      },
      {
        label: '正则',
        value: 're'
      }],
      response: '',
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
        'mode': 'formdata',
        'data': []
      },
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
        variable: ''
      }],
      minsize: { minRows: 6 },
      dialogSubmitFormVisible: false
    }
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
      const result = []
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
      data.body = result
      return data
    },
    translateVerify (data) {
      return data.filter(item => item.extractor !== '')
    },
    translateExtract (data) {
      return data.filter(item => item.selector !== '')
    },
    create () {
      this.$axios({
        url: '/api/v1/interface/create',
        method: 'post',
        data: JSON.stringify({
          team: this.team,
          project: this.project,
          name: this.name,
          host: this.host,
          path: this.path,
          method: this.method,
          header: this.translateData(this.header),
          params: this.translateData(this.params),
          body: this.translateData(this.body),
          verify: this.translateVerify(this.assert),
          extract: this.translateExtract(this.extract)
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
          this.response = res.data.data.response
          this.dialogSubmitFormVisible = false
        } else {
          let level = 'info'
          if (res.data.status >= 500) {
            level = 'error'
          }
          this.$message({
            type: level,
            message: res.data.message,
            center: true
          })
          this.response = res.data.data
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务器偷懒了！',
          center: true
        })
      })
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
          extract: this.translateExtract(this.extract)
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
          this.response = res.data.data.response
          this.dialogSubmitFormVisible = false
        } else {
          let level = 'info'
          if (res.data.status >= 500) {
            level = 'error'
          }
          this.$message({
            type: level,
            message: res.data.message,
            center: true
          })
          this.response = res.data.data
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务器偷懒了！',
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
