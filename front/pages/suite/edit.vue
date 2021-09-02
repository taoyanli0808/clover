<template>
  <div>
    <el-row>
      <el-col><TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" /></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-table
          :data="data"
          v-loading="loading"
          element-loading-text="拼命加载中"
          style="width: 100%"
          border
        >
          <el-table-column
            prop="id"
            label="ID"
            width="80"
          />
          <el-table-column
            prop="project"
            label="项目"
            width="150"
          />
          <el-table-column
            prop="team"
            label="团队"
            width="150"
          />
          <el-table-column
            prop="name"
            label="用例"
            width="180"
          />
          <el-table-column
            fixed="right"
            label="操作"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                @click="handleAdd(scope.$index, scope.row)"
                size="mini"
                icon="el-icon-video-play"
                type="primary"
              >
                添加
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @current-change="handleCurrentChange"
          :total="total"
          background
          layout="total, prev, pager, next, jumper"
        />
      </el-col>
      <el-col :span="12">
        <div>
          <el-table
            :data="suite.cases"
            v-loading="loading"
            element-loading-text="拼命加载中"
            style="width: 100%"
            border
          >
            <el-table-column
              prop="index"
              label="执行编号"
              width="80"
            />
            <el-table-column
              prop="caseId"
              label="用例ID"
              width="80"
            />
            <el-table-column
              prop="name"
              label="用例名"
              width="200"
            />
            <el-table-column
              fixed="right"
              label="操作"
              align="center"
            >
              <template slot-scope="scope">
                <el-button
                  @click="handleUp(scope.$index, scope.row)"
                  size="mini"
                  icon="el-icon-top"
                  type="primary"
                >
                  上移
                </el-button>
                <el-button
                  @click="handleDown(scope.$index, scope.row)"
                  size="mini"
                  icon="el-icon-bottom"
                  type="primary"
                >
                  下移
                </el-button>
                <el-button
                  @click="handleDelete(scope.$index, scope.row)"
                  size="mini"
                  icon="el-icon-delete"
                  type="danger"
                >
                  移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-row :gutter="20">
            <el-col :span="18">
              <!-- <el-input v-model="name" v-if="visible" size="mini" placeholder="请填写套件名称" /> -->
            </el-col>
            <el-col :span="6">
              <el-button @click="update" v-if="visible" size="mini" type="primary" icon="el-icon-plus">更新套件</el-button>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// import Sortable from 'sortablejs'
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader
  },
  data () {
    return {
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      team: '',
      project: '',
      loading: true,
      suite: {
        cases: []
      }
    }
  },
  computed: {
    visible () {
      console.log('here!')
      console.log(this.suite)
      console.log(this.suite.cases)
      return this.suite.cases.length !== 0
    }
  },
  mounted () {
    this.search()
    this.load()
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.search()
    },
    update () {
      this.$axios
        .post('/api/v1/suite/update', {
          id: this.suite.id,
          name: this.suite.name,
          team: this.suite.team,
          project: this.suite.project,
          cases: this.suite.cases
        })
        .then((res) => {
          if (res.data.status === 0) {
            this.suite = res.data.data
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
          this.loading = false
        })
    },
    search () {
      this.loading = true
      const params = {
        limit: this.limit,
        offset: this.page * this.limit
      }
      if (this.team !== '') {
        params.team = this.team
      }
      if (this.project !== '') {
        params.project = this.project
      }
      this.$axios
        .post('/api/v1/interface/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
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
          this.loading = false
        })
    },
    load () {
      this.$axios
        .post('/api/v1/suite/search', { id: this.$route.query.id })
        .then((res) => {
          if (res.data.status === 0) {
            this.suite = res.data.data
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
          this.loading = false
        })
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.search()
    },
    handleAdd (index, row) {
      this.suite.cases.push({
        index: this.suite.cases.length + 1,
        caseId: row.id,
        name: row.name,
        data: row
      })
    },
    handleUp (index, row) {
      if (index === 0) {
        this.$message({
          type: 'warning',
          message: '接口已经在第一个位置！',
          center: true
        })
      } else {
        // 这里先修改排序的序号
        this.suite.cases[index].index = index
        this.suite.cases[index - 1].index = index + 1
        // 对两个元素进行交换处理
        const front = this.suite.cases.splice(index - 1, 1)
        this.suite.cases.splice(index, 0, ...front)
      }
    },
    handleDown (index, row) {
      if (index === this.suite.cases.length - 1) {
        this.$message({
          type: 'warning',
          message: '接口已经在最后一个位置！',
          center: true
        })
      } else {
        // 这里先修改排序的序号
        this.suite.cases[index].index = index + 1
        this.suite.cases[index + 1].index = index
        // 对两个元素进行交换处理
        const front = this.suite.cases.splice(index, 1)
        this.suite.cases.splice(index + 1, 0, ...front)
      }
    },
    handleDelete (index, row) {
      this.suite.cases.splice(index, 1)
      // 刷新索引
      for (const i in this.suite.cases) {
        this.suite.cases[i].index = parseInt(i, 10) + 1
      }
    }
  }
}
</script>

<style scoped>
.el-row {
  padding-top: 20px;
}
</style>
