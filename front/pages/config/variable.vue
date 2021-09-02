<template>
  <div>
    <div class="page-header">
      <div style="display: inline">
        <TeamSelector v-on:selectedTeam="selectedTeam" />
      </div>
      <div style="display: inline">
        <OwnerSelector v-on:selectedOwner="selectedOwner" />
      </div>
      <div style="float: right; padding: 3px 0; display: block;">
        <el-button
          @click="handleAdd"
          icon="el-icon-plus"
          type="primary"
          size="small"
          plain
        >
          创建变量
        </el-button>
      </div>
    </div>
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
        prop="owner"
        label="负责人"
        width="200"
        align="center"
      />
      <el-table-column
        prop="name"
        label="变量名"
        width="200"
        align="center"
      />
      <el-table-column
        prop="value"
        label="变量值"
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
          <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject"  placeholder="请选择团队和项目" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="owner" />
        </el-form-item>
        <el-form-item label="变量名">
          <el-input v-model="name" />
        </el-form-item>
        <el-form-item label="变量值">
          <el-input v-model="value" />
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
        <el-form-item label="负责人">
          <el-input v-model="owner" />
        </el-form-item>
        <el-form-item label="变量名">
          <el-input v-model="name" />
        </el-form-item>
        <el-form-item label="变量值">
          <el-input v-model="value" />
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
import OwnerSelector from '~/components/OwnerSelector.vue'
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader,
    OwnerSelector,
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
      owner: '',
      project: '',
      name: '',
      value: '',
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
          url: '/api/v1/variable/delete',
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
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    addVariable () {
      this.addDialogVisible = false
      this.$axios({
        url: '/api/v1/variable/create',
        method: 'post',
        data: JSON.stringify({
          team: this.team,
          project: this.project,
          owner: this.owner,
          name: this.name,
          value: this.value
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        this.team = ''
        this.project = ''
        this.owner = ''
        this.name = ''
        this.value = ''
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
        this.refresh()
      }).catch((error) => {
        this.$message({
          type: 'error',
          message: error.response.data.message,
          center: true
        })
      })
    },
    editVariable () {
      this.editDialogVisible = false
      this.$axios({
        url: '/api/v1/variable/update',
        method: 'post',
        data: JSON.stringify({
          id: this.id,
          team: this.team,
          project: this.project,
          owner: this.owner,
          name: this.name,
          value: this.value
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          this.team = ''
          this.project = ''
          this.owner = ''
          this.refresh()
        } else {
          this.$message({
            type: 'warning',
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
    refresh () {
      this.loading = true
      const params = {
        limit: this.limit,
        offset: this.page * this.limit
      }
      if (this.team !== '') {
        params.team = this.team
      }
      if (this.owner !== '') {
        params.owner = this.owner
      }
      this.$axios
        .get('/api/v1/variable/search', {
          params
        })
        .then((res) => {
          this.total = res.data.total
          this.data = res.data.data
          this.loading = false
        })
        .catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
    },
    selectedTeam (value) {
      this.team = value
      this.refresh()
    },
    selectedOwner (value) {
      this.owner = value
      this.refresh()
    },
    addTeam (value) {
      this.add.team = value
      this.project = []
      this.$axios
        .get('/api/v1/variable/search', {
          params: {
            team: value
          }
        })
        .then((res) => {
          for (const index in res.data.data) {
            this.project.push({
              project: res.data.data[index].project,
              owner: res.data.data[index].owner
            })
          }
        })
        .catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
    },
    addProject (value) {
      this.add.project = value
      for (const index in this.project) {
        if (this.project[index].project === value) {
          this.add.owner = this.project[index].owner
        }
      }
    },
    editTeam (value) {
      this.edit.team = value
      this.project = []
      this.$axios
        .get('/api/v1/variable/search', {
          params: {
            team: value
          }
        })
        .then((res) => {
          for (const index in res.data.data) {
            this.project.push({
              project: res.data.data[index].project,
              owner: res.data.data[index].owner
            })
          }
        })
        .catch((error) => {
          this.$message({
            type: 'error',
            message: error.response.data.message,
            center: true
          })
        })
    },
    editProject (value) {
      this.edit.project = value
      for (const index in this.project) {
        if (this.project[index].project === value) {
          this.edit.owner = this.project[index].owner
        }
      }
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

.page-header {
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
}
</style>
