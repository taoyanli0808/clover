<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-tabs
          v-model="activeName"
          @tab-click="handleClick"
        >
          <el-tab-pane label="基本信息" name="first">
            <el-form
              ref="form"
            >
              <el-form-item label="业务团队">
                <el-select
                  @change="selectTeam"
                  v-model="environment.team"
                  placeholder="请选择团队"
                  clearable
                >
                  <el-option
                    v-for="item in team"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="所属项目">
                <el-select
                  @change="selectProject"
                  v-model="environment.project"
                  placeholder="请选择项目"
                  clearable
                >
                  <el-option
                    v-for="item in project"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="用例名称">
                <el-input
                  v-model="request.name"
                  placeholder="clover接口测试用例"
                  clearable
                />
              </el-form-item>
              <el-form-item label="测试域名">
                <el-input
                  v-model="request.host"
                  placeholder="https://github.com"
                  class="input-with-select"
                  clearable
                >
                  <el-select
                    slot="prepend"
                    @change="selectMethod"
                    v-model="request.method"
                    placeholder="请求方法"
                    clearable
                  >
                    <el-option
                      v-for="method in methods"
                      :key="method"
                      :label="method"
                      :value="method"
                    />
                  </el-select>
                </el-input>
              </el-form-item>
              <el-form-item label="请求路径">
                <el-input
                  v-model="request.path"
                  placeholder="/taoyanli0808/clover"
                  clearable
                />
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="请求头信息" name="second">
            <el-table
              ref="headerTable"
              :data="request.header"
              @row-click="currentHeaderTableChange"
              class="tb-edit"
              style="width: 100%"
              highlight-current-row
              border
            >
              <el-table-column
                label="KEY"
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.key"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.key }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="VALUE"
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.value"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.value }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                align="center"
              >
                <template scope="scope">
                  <el-button
                    @click="addHeaderTableRow(scope.$index, scope.row)"
                    size="small"
                    type="primary"
                  >
                    添加
                  </el-button>
                  <el-button
                    @click="deleteHeaderTableRow(scope.$index, scope.row)"
                    size="small"
                    type="danger"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="请求参数" name="third">
            <el-table
              :data="request.param"
              @row-click="currentParameterTableChange"
              class="tb-edit"
              style="width: 100%"
              highlight-current-row
              border
            >
              <el-table-column
                label="KEY"
                width="180"
                header-align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.key"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.key }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="VALUE"
                width="180"
                header-align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.value"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.value }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                align="center"
              >
                <template scope="scope">
                  <el-button
                    @click="addParameterTableRow(scope.$index, scope.row)"
                    size="small"
                    type="primary"
                  >
                    添加
                  </el-button>
                  <el-button
                    @click="deleteParameterTableRow(scope.$index, scope.row)"
                    size="small"
                    type="danger"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
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
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-select v-model="scope.row.extractor" placeholder="请选择">
                    <el-option
                      label="delimiter"
                      value="re"
                    />
                    <el-option
                      label="re"
                      value="re"
                    />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column
                label="EXPRESSION"
                width="180"
                align="center"
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
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-select v-model="scope.row.comparator" placeholder="请选择">
                    <el-option
                      label="contains"
                      value="contains"
                    />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column
                label="CONVERTOR"
                width="180"
                align="center"
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
                </template>
              </el-table-column>
              <el-table-column
                label="EXPECTED"
                width="180"
                align="center"
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
                label="操作"
                align="center"
                width="180"
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
              @row-click="currentExtractTableChange"
              class="tb-edit"
              style="width: 100%"
              highlight-current-row
              border
            >
              <el-table-column
                label="SELECTOR"
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-select v-model="scope.row.selector" placeholder="请选择">
                    <el-option
                      v-for="item in selectors"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column
                label="EXPRESSION"
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.expression"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.key }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="EXPECTED"
                width="180"
                align="center"
              >
                <template scope="scope">
                  <el-input
                    v-model="scope.row.expected"
                    size="small"
                    placeholder="请输入内容"
                  />
                  <span>
                    {{ scope.row.value }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
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
        <el-row
          :gutter="20"
        >
          <el-col
            :span="4"
            :offset="16"
          >
            <el-button
              @click="debugCase"
              type="primary"
            >
              Debug
            </el-button>
          </el-col>
          <el-col
            :span="4"
          >
            <el-button
              @click="saveCase"
              type="primary"
            >
              Save
            </el-button>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="12">
        <pre>
          <code>
            {{ response }}
          </code>
        </pre>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      team: [],
      project: [],
      methods: ['get', 'post', 'put', 'delete'],
      activeName: 'first',
      selectors: [{
        label: '分隔符',
        value: 'delimiter'
      },
      {
        label: '正则',
        value: 're'
      }],
      response: '',
      environment: {
        team: '',
        project: ''
      },
      request: {
        name: '',
        host: '',
        path: '',
        method: '',
        header: [{
          key: '',
          value: ''
        }],
        param: [{
          key: '',
          value: ''
        }]
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
        expected: ''
      }]
    }
  },
  mounted () {
    this.getTeam()
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event)
    },
    selectTeam (value) {
      this.environment.team = value
      this.project = []
      this.$axios
        .get('/api/v1/environment/search', {
          params: {
            type: 'team',
            team: value
          }
        })
        .then((res) => {
          for (const index in res.data.data) {
            this.project.push({
              label: res.data.data[index].project,
              value: res.data.data[index].project
            })
          }
        })
    },
    selectProject (value) {
      this.environment.project = value
    },
    selectMethod (value) {
      this.request.method = value
    },
    getTeam () {
      this.$axios({
        url: '/api/v1/environment/aggregate',
        method: 'post',
        data: JSON.stringify({
          type: 'team',
          key: 'team'
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        for (const index in res.data.data) {
          this.team.push({
            label: res.data.data[index]._id,
            value: res.data.data[index]._id
          })
        }
      })
    },
    currentHeaderTableChange (row, event, column) {
      console.log(row, event, column, event.currentTarget)
    },
    addHeaderTableRow (index, row) {
      this.request.header.push({
        key: '',
        value: ''
      })
      const last = this.$refs.headerTable.data.length
      const currentRow = this.$refs.headerTable.data[last]
      this.$refs.headerTable.setCurrentRow(currentRow)
      console.log(last)
    },
    deleteHeaderTableRow (index, row) {
      this.request.header = this.request.header.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.request.header) && this.request.header.length === 0) {
        this.request.header.push({
          key: '',
          value: ''
        })
      }
    },
    currentParameterTableChange (row, event, column) {
      console.log(row, event, column)
    },
    addParameterTableRow (index, row) {
      this.request.param.push({
        key: '',
        value: ''
      })
    },
    deleteParameterTableRow (index, row) {
      console.log(index, row)
      this.request.param = this.request.param.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.request.param) && this.request.param.length === 0) {
        this.request.param.push({
          key: '',
          value: ''
        })
      }
    },
    currentAssertTableChange (row, event, column) {
      console.log(row, event, column, event.currentTarget)
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
      this.assert = this.assert.filter(item => item.expression !== row.expression)
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
    currentExtractTableChange (row, event, column) {
      console.log(row, event, column)
    },
    addExtractTableRow (index, row) {
      this.extract.push({
        selector: '',
        expression: '',
        expected: ''
      })
      const last = this.$refs.extractTable.data.length
      const currentRow = this.$refs.extractTable.data[last]
      this.$refs.extractTable.setCurrentRow(currentRow)
      console.log(last)
    },
    deleteExtractTableRow (index, row) {
      this.extract = this.extract.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.extract) && this.extract.length === 0) {
        this.extract.push({
          selector: '',
          expression: '',
          expected: ''
        })
      }
    },
    debugCase () {
      this.$axios({
        url: '/api/v1/interface/debug',
        method: 'post',
        data: JSON.stringify({
          assert: this.assert,
          request: this.request,
          extract: this.extract,
          environment: this.environment
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: '测试成功'
          })
          this.response = res.data.data.response.content
        } else {
          let level = 'info'
          if (res.data.status >= 500) {
            level = 'error'
          }
          this.$message({
            type: level,
            message: res.data.message
          })
          this.response = res.data.data
        }
      }).catch((error) => {
        console.log(error)
        this.$message({
          type: 'error',
          message: '服务器偷懒了！'
        })
      })
    },
    saveCase () {
      this.$axios({
        url: '/api/v1/interface/save',
        method: 'post',
        data: JSON.stringify({
          assert: this.assert,
          request: this.request,
          extract: this.extract,
          environment: this.environment
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: '测试成功'
          })
          this.response = res.data.data.response.content
        } else {
          let level = 'info'
          if (res.data.status >= 500) {
            level = 'error'
          }
          this.$message({
            type: level,
            message: res.data.message
          })
          this.response = res.data.data
        }
      }).catch((error) => {
        console.log(error)
        this.$message({
          type: 'error',
          message: '服务器偷懒了！'
        })
      })
    }
  }
}
</script>

<style>
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
</style>
