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
            :data="suite"
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
              <el-button @click="create" v-if="visible" size="mini" type="primary" icon="el-icon-plus">创建套件</el-button>
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
      suite: []
    }
  },
  computed: {
    visible () {
      return this.suite.length !== 0
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.refresh()
    },
    create () {
      this.$prompt('请输入套件名称', '创建套件', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        const params = {
          team: this.team,
          project: this.project,
          type: 'interface',
          cases: this.suite.map(x => x.caseId),
          name: value
        }
        this.$axios
          .post('/api/v1/suite/create', params)
          .then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'info',
                message: res.data.message,
                center: true
              })
              this.$router.push({
                path: '/suite/'
              })
            } else {
              this.$message({
                type: 'error',
                message: res.data.message,
                center: true
              })
            }
          }).catch(() => {
            this.$message({
              type: 'error',
              message: '服务出错，请联系管理员',
              center: true
            })
            this.loading = false
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消创建套件！',
          center: true
        })
      })
    },
    refresh () {
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
        .catch(() => {
          this.$message({
            type: 'error',
            message: '服务出错，请联系管理员',
            center: true
          })
          this.loading = false
        })
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    handleAdd (index, row) {
      this.suite.push({
        index: this.suite.length + 1,
        caseId: row.id,
        name: row.name
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
        this.suite[index].index = index
        this.suite[index - 1].index = index + 1
        // 对两个元素进行交换处理
        const front = this.suite.splice(index - 1, 1)
        this.suite.splice(index, 0, ...front)
      }
    },
    handleDown (index, row) {
      if (index === this.suite.length - 1) {
        this.$message({
          type: 'warning',
          message: '接口已经在最后一个位置！',
          center: true
        })
      } else {
        // 这里先修改排序的序号
        this.suite[index].index = index + 1
        this.suite[index + 1].index = index
        // 对两个元素进行交换处理
        const front = this.suite.splice(index, 1)
        this.suite.splice(index + 1, 0, ...front)
      }
    },
    handleDelete (index, row) {
      this.suite.splice(index, 1)
      // 刷新索引
      for (const i in this.suite) {
        this.suite[i].index = parseInt(i, 10) + 1
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
