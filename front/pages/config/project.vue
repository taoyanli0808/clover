<template>
  <div>
    <div class="page-header">
      <div style="display: inline">
        <TeamSelector
          ref="teamSelector"
          v-on:selectedTeam="selectedTeam"
        />
      </div>
      <div style="display: inline">
        <OwnerSelector
          ref="ownerSelector"
          v-on:selectedOwner="selectedOwner"
        />
      </div>
      <div style="float: right; padding: 3px 0; display: block;">
        <el-button
          @click="handleAdd"
          icon="el-icon-plus"
          type="primary"
          size="small"
          plain
        >
          创建项目
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
      <el-table-column prop="id" label="ID" width="90" align="center" />
      <el-table-column prop="team" label="团队" width="200" align="center" />
      <el-table-column prop="project" label="项目" width="200" align="center" />
      <el-table-column prop="owner" label="负责人" width="200" align="center" />
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
      <el-table-column fixed="right" label="操作" width="300" align="center">
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
    <el-dialog :visible.sync="addDialogVisible" width="30%" title="添加项目" >
      <el-form ref="form" :model="add" label-width="80px" >
        <el-form-item label="团队名称">
          <el-input v-model="add.team" />
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="add.project" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="add.owner" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button @click="addProject" type="primary">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="editDialogVisible" width="30%" title="编辑项目">
      <el-form ref="form" :model="edit" label-width="80px">
        <el-form-item label="团队名称">
          <el-input v-model="edit.team" />
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="edit.project" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="edit.owner" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button @click="editProject" type="primary">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import TeamSelector from '~/components/TeamSelector.vue'
import OwnerSelector from '~/components/OwnerSelector.vue'

export default {
  components: {
    TeamSelector,
    OwnerSelector
  },
  data () {
    return {
      view: true,
      menuKey: 1,
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      loading: true,
      addDialogVisible: false,
      add: {
        team: '',
        project: '',
        owner: ''
      },
      editDialogVisible: false,
      edit: {
        team: '',
        project: '',
        owner: ''
      },
      team: '',
      owner: ''
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
    handleAdd (index, row) {
      this.addDialogVisible = true
    },
    handleEdit (index, row) {
      this.editDialogVisible = true
      this.edit.team = row.team
      this.edit.project = row.project
      this.edit.owner = row.owner
      this.edit.id = row.id
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '删除项目', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios({
          url: '/api/v1/team/delete',
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
            this.$message({
              type: 'warning',
              message: '团队与项目关联的变量不会被删除，请手动删除！',
              center: true,
              offset: 60
            })
            // 创建团队后下拉框不更新 #8 https://github.com/taoyanli0808/clover/issues/8
            this.$refs.teamSelector.getTeam()
            this.$refs.ownerSelector.getOwner()
          } else {
            this.$message({
              type: 'warning',
              message: res.data.message,
              center: true
            })
          }
        }).catch((error) => {
          if (error.response) {
            const message = JSON.stringify(error.response.data.message)
            this.$message({
              type: 'error',
              message,
              center: true
            })
          } else {
            this.$message({
              type: 'error',
              message: '未知错误，请联系管理员！',
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
    addProject () {
      this.addDialogVisible = false
      this.$axios({
        url: '/api/v1/team/create',
        method: 'post',
        data: JSON.stringify(this.add),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        this.add.team = ''
        this.add.project = ''
        this.add.owner = ''
        if (res.data.status === 0) {
          this.refresh()
          this.$message({
            type: 'success',
            message: res.data.message,
            center: true
          })
          // 创建团队后下拉框不更新 #8 https://github.com/taoyanli0808/clover/issues/8
          this.$refs.teamSelector.getTeam()
          this.$refs.ownerSelector.getOwner()
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
    editProject () {
      this.editDialogVisible = false
      this.$axios({
        url: '/api/v1/team/update',
        method: 'post',
        data: JSON.stringify(this.edit),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          // 创建团队后下拉框不更新 #8 https://github.com/taoyanli0808/clover/issues/8
          this.$refs.teamSelector.getTeam()
          this.$refs.ownerSelector.getOwner()
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
        .get('/api/v1/team/search', {
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
          this.loading = false
        })
    },
    selectedTeam (value) {
      this.team = value
      this.refresh()
    },
    selectedOwner (value) {
      this.owner = value
      this.refresh()
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
