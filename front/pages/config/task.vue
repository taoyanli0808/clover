<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="3">
        <TeamSelector v-on:selectedTeam="selectedTeam" />
      </el-col>
      <el-col
        :span="3"
        :offset="18"
      >
        <el-button
          @click="handleAdd"
          icon="el-icon-plus"
          type="primary"
        >
          创建任务
        </el-button>
      </el-col>
    </el-row>
    <el-table
      :data="data"
      v-loading="loading"
      element-loading-text="拼命加载中"
      style="width: 100%"
      stripe
      border
    >
      <el-table-column
        prop="id"
        label="ID"
        width="90"
        align="center"
      />
      <el-table-column
        prop="team"
        label="团队"
        width="200"
        align="center"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="200"
        align="center"
      />
      <el-table-column
        prop="name"
        label="任务名"
        width="200"
        align="center"
      />
      <el-table-column
        prop="cron"
        label="任务值"
        width="200"
        align="center"
      />
      <el-table-column
        prop="variable"
        label="触发变量"
        width="200"
        align="center"
      />
      <el-table-column
        prop="created"
        label="创建日期"
        width="200"
        align="center"
      />
      <el-table-column
        prop="updated"
        label="更新日期"
        width="200"
        align="center"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleAdd(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-plus"
            type="primary"
          >
            添加
          </el-button>
          <el-button
            @click="handleEdit(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-edit"
            type="warning"
          >
            编辑
          </el-button>
          <el-button
            @click="handleDelete(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-delete"
            type="danger"
          >
            删除
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
    <el-dialog
      :visible.sync="addDialogVisible"
      width="30%"
      title="添加变量"
    >
      <el-form ref="form" label-width="80px">
        <el-form-item label="团队与项目">
          <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
        </el-form-item>
        <el-form-item label="任 务 名">
          <el-input v-model="name" />
        </el-form-item>
        <el-form-item label="定时表达式">
          <el-input v-model="cron" />
        </el-form-item>
        <el-form-item label="触发变量">
          <el-input v-model="variable" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button @click="addVariable" type="primary">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="editDialogVisible"
      width="30%"
      title="编辑项目"
    >
      <el-form ref="form" label-width="80px">
        <el-form-item label="团队名称">
          <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
        </el-form-item>
        <el-form-item label="任 务 名">
          <el-input v-model="name" />
        </el-form-item>
        <el-form-item label="定时表达式">
          <el-input v-model="cron" />
        </el-form-item>
        <el-form-item label="触发变量">
          <el-input v-model="variable" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button @click="editVariable" type="primary">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import TeamSelector from '~/components/TeamSelector.vue'
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader,
    TeamSelector
  },
  data () {
    return {
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      loading: true,
      addDialogVisible: false,
      editDialogVisible: false,
      id: '',
      team: '',
      project: '',
      name: '',
      cron: '',
      variable: '',
      addSelectTeam: '',
      selectProject: '',
      editSelectTeam: ''
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    /*
    * table右侧的操作，增改删按钮的处理事件。
    * */
    handleAdd (index, row) {
      this.addDialogVisible = true
    },
    handleEdit (index, row) {
      this.editDialogVisible = true
      this.team = row.team
      this.project = row.project
      this.owner = row.owner
      this.name = row.name
      this.value = row.value
      this.id = row.id
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '删除项目', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios({
          url: '/api/v1/task/delete',
          method: 'post',
          data: JSON.stringify({
            id: row.id
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          if (res.data.status === 0) {
            this.refresh()
            this.$message({
              type: 'success',
              message: '删除成功!',
              center: true
            })
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message,
              center: true
            })
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除',
          center: true
        })
      })
    },
    addVariable () {
      this.addDialogVisible = false
      this.$axios({
        url: '/api/v1/task/create',
        method: 'post',
        data: JSON.stringify({
          team: this.team,
          project: this.project,
          name: this.name,
          cron: this.cron,
          variable: this.variable
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        this.team = ''
        this.project = ''
        this.name = ''
        this.cron = ''
        this.varable = ''
        this.addSelectTeam = ''
        this.selectProject = ''
        if (res.data.status === 0) {
          this.refresh()
          this.$message({
            type: 'success',
            message: res.data.message,
            center: true
          })
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务端错误，请联系管理员！',
          center: true
        })
      })
    },
    editVariable () {
      this.editDialogVisible = false
      this.$axios({
        url: '/api/v1/task/update',
        method: 'post',
        data: JSON.stringify({
          id: this.id,
          team: this.team,
          project: this.project,
          name: this.name,
          cron: this.cron,
          variable: this.variable
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.team = ''
          this.project = ''
          this.refresh()
        } else {
          this.$message({
            type: 'warning',
            message: res.data.message,
            center: true
          })
        }
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '服务端错误，请联系管理员！',
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
      this.$axios
        .get('/api/v1/task/search', {
          params
        })
        .then((res) => {
          this.total = res.data.total
          this.data = res.data.data
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
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.el-pagination {
  margin-top: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
</style>
