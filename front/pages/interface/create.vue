<template>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-tabs
        v-model="activeName"
        @tab-click="handleClick"
        tab-position="left"
      >
        <el-tab-pane label="基本信息" name="first">
          <el-form ref="form" :model="form">
            <el-form-item label="业务团队">
              <el-select
                @change="selectTeam"
                v-model="form.team"
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
                v-model="form.project"
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
                v-model="form.name"
                placeholder="clover接口测试用例"
                clearable
              />
            </el-form-item>
            <el-form-item label="测试域名">
              <el-input
                v-model="form.host"
                placeholder="https://github.com"
                class="input-with-select"
                clearable
              >
                <el-select
                  slot="prepend"
                  @change="selectMethod"
                  v-model="form.method"
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
                v-model="form.path"
                placeholder="/taoyanli0808/clover"
                clearable
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="请求头信息" name="second">
          <el-table
            :data="headerTable"
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
            :data="parameterTable"
            @row-click="currentParameterTableChange"
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
          添加断言
        </el-tab-pane>
        <el-tab-pane label="提取响应" name="five">
          提取响应
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-col :span="12">
      <pre>
        <code>
          {{ response }}
        </code>
      </pre>
    </el-col>
  </el-row>
</template>

<script>
export default {
  data () {
    return {
      team: [],
      project: [],
      methods: ['get', 'post', 'put', 'delete'],
      form: {
        team: '',
        project: '',
        name: '',
        host: '',
        path: '',
        method: ''
      },
      activeName: 'first',
      response: '',
      headerTable: [{
        key: '',
        value: ''
      }],
      parameterTable: [{
        key: '',
        value: ''
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
      this.form.team = value
      this.project = []
      this.$axios
        .get('/api/v1/environment/search', {
          params: {
            type: 'team',
            team: value
          }
        })
        .then((res) => {
          console.log(res)
          for (const index in res.data.data) {
            this.project.push({
              label: res.data.data[index].project,
              value: res.data.data[index].project
            })
          }
        })
    },
    selectProject (value) {
      this.form.project = value
    },
    selectMethod (value) {
      this.form.method = value
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
      this.headerTable.push({
        key: '',
        value: ''
      })
    },
    deleteHeaderTableRow (index, row) {
      console.log(index, row)
      this.headerTable = this.headerTable.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.headerTable) && this.headerTable.length === 0) {
        this.headerTable.push({
          key: '',
          value: ''
        })
      }
    },
    currentParameterTableChange (row, event, column) {
      console.log(row, event, column, event.currentTarget)
    },
    addParameterTableRow (index, row) {
      this.parameterTable.push({
        key: '',
        value: ''
      })
    },
    deleteParameterTableRow (index, row) {
      console.log(index, row)
      this.parameterTable = this.parameterTable.filter(item => item.key !== row.key)
      if (Array.prototype.isPrototypeOf(this.parameterTable) && this.parameterTable.length === 0) {
        this.parameterTable.push({
          key: '',
          value: ''
        })
      }
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
