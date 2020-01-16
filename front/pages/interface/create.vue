<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-tabs
          v-model="activeName"
        >
          <el-tab-pane label="基本信息" name="first">
            <el-form
              ref="form"
            >
              <el-form-item label="业务与项目">
                <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
              </el-form-item>
              <el-form-item label="用例名称">
                <el-input
                  v-model="name"
                  placeholder="clover接口测试用例"
                  clearable
                />
              </el-form-item>
              <el-form-item label="测试域名">
                <el-input
                  v-model="host"
                  placeholder="https://github.com"
                  class="input-with-select"
                  clearable
                >
                  <el-select
                    slot="prepend"
                    @change="selectMethod"
                    v-model="method"
                    placeholder="请求方法"
                    clearable
                  >
                    <el-option
                      v-for="m in methods"
                      :key="m"
                      :label="m"
                      :value="m"
                    />
                  </el-select>
                </el-input>
              </el-form-item>
              <el-form-item label="请求路径">
                <el-input
                  v-model="path"
                  placeholder="/taoyanli0808/clover"
                  clearable
                />
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="请求头信息" name="second">
            <el-table
              ref="headerTable"
              :data="header"
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
              :data="param"
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
          <el-tab-pane label="请求体" name="fourth">
            <el-table
              :data="body"
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
                    @click="addBodyTableRow(scope.$index, scope.row)"
                    size="small"
                    type="primary"
                  >
                    添加
                  </el-button>
                  <el-button
                    @click="deleteBodyTableRow(scope.$index, scope.row)"
                    size="small"
                    type="danger"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="添加断言" name="five">
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
                      value="delimiter"
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
          <el-tab-pane label="提取响应" name="six">
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
                width="180"
                align="center"
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
      selectors: [{
        label: '分隔符',
        value: 'delimiter'
      },
      {
        label: '正则',
        value: 're'
      }],
      response: '',
      team: '',
      project: '',
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
      }],
      body: [{
        key: '',
        value: ''
      }],
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
      this.body.push({
        key: '',
        value: ''
      })
    },
    deleteBodyTableRow (index, row) {
      this.body = this.body.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.body) && this.body.length === 0) {
        this.body.push({
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
    addExtractTableRow (index, row) {
      this.extract.push({
        selector: '',
        expression: '',
        expected: ''
      })
      const last = this.$refs.extractTable.data.length
      const currentRow = this.$refs.extractTable.data[last]
      this.$refs.extractTable.setCurrentRow(currentRow)
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
          team: this.team,
          project: this.project,
          name: this.name,
          host: this.host,
          path: this.path,
          method: this.method,
          header: this.header,
          params: this.param,
          body: this.body,
          verify: this.assert,
          extract: this.extract
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
          this.response = JSON.stringify(res.data.data[0].response.json, null, 4)
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
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务器偷懒了！'
        })
      })
    },
    saveCase () {
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
          header: this.header,
          params: this.param,
          body: this.body,
          verify: this.assert,
          extract: this.extract
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.$message({
            type: 'success',
            message: '保存用例成功！用例ID是[' + res.data.data + ']'
          })
          /*
          setTimeout(function () {
            this.$router.push({
              path: '/interface/'
            })
          }, 3000)
          */
        } else {
          let level = 'info'
          if (res.data.status >= 500) {
            level = 'error'
          }
          this.$message({
            type: level,
            message: res.data.message
          })
        }
      }).catch(() => {
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
