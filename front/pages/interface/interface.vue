<template>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-tabs
        v-model="activeName"
        @tab-click="handleClick"
        tab-position="left"
      >
        <el-tab-pane label="基本信息" name="first">
          <el-form ref="form" :model="form" label-width="80px">
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
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="域名">
            <el-input v-model="form.host"></el-input>
          </el-form-item>
          <el-form-item label="路径">
            <el-input v-model="form.path"></el-input>
          </el-form-item>
          <el-form-item label="所属项目">
            <el-select
              @change="selectMethod"
              v-model="form.method"
              placeholder="请选择项目"
              clearable
            >
              <el-option
                v-for="method in methods"
                :key="method"
                :label="method"
                :value="method"
              />
            </el-select>
          </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="请求头信息" name="second">
          请求头信息
        </el-tab-pane>
        <el-tab-pane label="请求参数" name="third">
          请求参数
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
      response: ''
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
    }
  }
}
</script>
