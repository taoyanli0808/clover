<template>
  <div class="block">
    <el-row :gutter="20">
      <el-col :span="3">
        <el-select
          @change="changeTeam"
          v-model="selectTeam"
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
      </el-col>
      <el-col :span="3">
        <el-select
          @change="changeOwner"
          v-model="selectOwner"
          placeholder="请选择负责人"
          clearable
        >
          <el-option
            v-for="item in owner"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-col>
      <el-col
        :span="3"
        :offset="15"
      >
        <el-button
          @click="handleAdd"
          icon="el-icon-plus"
          type="primary"
        >
          创建变量
        </el-button>
      </el-col>
    </el-row>
    <el-table
      :data="data"
      style="width: 100%"
      stripe
      border
    >
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
      <el-form ref="form" :model="add" label-width="80px">
        <el-form-item label="团队名称">
          <el-select
            @change="addTeam"
            v-model="addSelectTeam"
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
        <el-form-item label="项目名称">
          <el-select
            @change="addProject"
            v-model="selectProject"
            placeholder="请选择项目"
            clearable
          >
            <el-option
              v-for="item in project"
              :key="item.project"
              :label="item.project"
              :value="item.project"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="add.owner" />
        </el-form-item>
        <el-form-item label="变量名">
          <el-input v-model="add.name" />
        </el-form-item>
        <el-form-item label="变量值">
          <el-input v-model="add.value" />
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
      <el-form ref="form" :model="edit" label-width="80px">
        <el-form-item label="团队名称">
          <el-select
            @change="editTeam"
            v-model="editSelectTeam"
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
        <el-form-item label="项目名称">
          <el-select
            @change="editProject"
            v-model="selectProject"
            placeholder="请选择项目"
            clearable
          >
            <el-option
              v-for="item in project"
              :key="item.project"
              :label="item.project"
              :value="item.project"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="edit.owner" />
        </el-form-item>
        <el-form-item label="变量名">
          <el-input v-model="edit.name" />
        </el-form-item>
        <el-form-item label="变量值">
          <el-input v-model="edit.value" />
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
export default {
  data () {
    return {
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      addDialogVisible: false,
      add: {
        type: 'variable',
        team: '',
        project: '',
        owner: '',
        name: '',
        value: ''
      },
      editDialogVisible: false,
      edit: {
        type: 'variable',
        team: '',
        project: '',
        owner: '',
        name: '',
        value: ''
      },
      team: [],
      selectTeam: '',
      addSelectTeam: '',
      owner: [],
      selectOwner: '',
      selectProject: '',
      project: [],
      editSelectTeam: ''
    }
  },
  mounted () {
    this.refresh()
    this.getTeam()
    this.getOwner()
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
      this.edit.name = row.name
      this.edit.value = row.value
      this.edit._id = row._id
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '删除项目', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios({
          url: '/api/v1/environment/delete',
          method: 'post',
          data: JSON.stringify({
            type: 'variable',
            id_list: [row._id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          this.refresh()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    addVariable () {
      this.addDialogVisible = false
      this.$axios({
        url: '/api/v1/environment/create',
        method: 'post',
        data: JSON.stringify(this.add),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        this.add.team = ''
        this.add.project = ''
        this.add.owner = ''
        this.add.name = ''
        this.add.value = ''
        this.addSelectTeam = ''
        this.selectProject = ''
        this.refresh()
      })
    },
    editVariable () {
      this.editDialogVisible = false
      this.$axios({
        url: '/api/v1/environment/update',
        method: 'post',
        data: JSON.stringify(this.edit),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        this.refresh()
      })
    },
    refresh () {
      const params = {
        limit: this.limit,
        skip: this.page * this.limit,
        type: 'variable'
      }
      if (this.selectTeam !== '') {
        params.team = this.selectTeam
      }
      if (this.selectOwner !== '') {
        params.owner = this.selectOwner
      }
      this.$axios
        .get('/api/v1/environment/search', {
          params
        })
        .then((res) => {
          this.total = res.data.total
          this.data = res.data.data
        })
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
    changeTeam () {
      this.refresh()
    },
    getOwner () {
      this.$axios({
        url: '/api/v1/environment/aggregate',
        method: 'post',
        data: JSON.stringify({
          type: 'variable',
          key: 'owner'
        }),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        for (const index in res.data.data) {
          this.owner.push({
            label: res.data.data[index]._id,
            value: res.data.data[index]._id
          })
        }
      })
    },
    changeOwner () {
      this.refresh()
    },
    addTeam (value) {
      this.add.team = value
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
              project: res.data.data[index].project,
              owner: res.data.data[index].owner
            })
          }
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
        .get('/api/v1/environment/search', {
          params: {
            type: 'team',
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
    },
    editProject (value) {
      this.edit.project = value
      for (const index in this.project) {
        if (this.project[index].project === value) {
          this.edit.owner = this.project[index].owner
        }
      }
    }
  }
}
</script>

<style>
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
