<template>
  <div class="block">
    <el-table
      :data="data"
      style="width: 100%"
      stripe
      border
    >
      <el-table-column
        prop="_id"
        label="ID"
        width="220"
      />
      <el-table-column
        prop="team"
        label="团队"
        width="200"
      />
      <el-table-column
        prop="project"
        label="项目"
        width="200"
      />
      <el-table-column
        prop="owner"
        label="负责人"
        width="200"
      />
      <el-table-column
        prop="created"
        label="创建日期"
        width="200"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleAdd(scope.$index, scope.row)"
            size="mini"
            type="primary"
          >
            添加
          </el-button>
          <el-button
            @click="handleEdit(scope.$index, scope.row)"
            size="mini"
            type="warning"
          >
            编辑
          </el-button>
          <el-button
            @click="handleDelete(scope.$index, scope.row)"
            size="mini"
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
      title="添加项目"
    >
      <el-form ref="form" :model="add" label-width="80px">
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
    <el-dialog
      :visible.sync="editDialogVisible"
      width="30%"
      title="添加项目"
    >
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
export default {
  data () {
    return {
      baseUrl: 'http://127.0.0.1:5000',
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      addDialogVisible: false,
      add: {
        type: 'team',
        team: '',
        project: '',
        owner: ''
      },
      editDialogVisible: false,
      edit: {
        type: 'team',
        team: '',
        project: '',
        owner: ''
      }
    }
  },
  mounted () {
    this.$axios
      .get(this.baseUrl + '/environment/api/v1/search', {
        params: { limit: this.limit, type: 'team' }
      })
      .then((res) => {
        console.log(res)
        this.total = res.data.total
        this.data = res.data.data
      })
  },
  methods: {
    handleCurrentChange (value) {
      this.page = value - 1
      console.log(value)
      this.$axios
        .get(this.baseUrl + '/environment/api/v1/search', {
          params: { limit: this.limit, skip: (value - 1) * this.limit, type: 'team' }
        })
        .then((res) => {
          console.log(res)
          this.total = res.data.total
          this.data = res.data.data
        })
    },
    handleAdd (row) {
      this.addDialogVisible = true
    },
    handleEdit (index, row) {
      this.editDialogVisible = true
      this.edit.team = row.team
      this.edit.project = row.project
      this.edit.owner = row.owner
      this.edit._id = row._id
    },
    handleDelete (row) {
      console.log(row)
    },
    handleClose (value) {
      console.log(value)
    },
    addProject () {
      this.addDialogVisible = false
      this.$axios({
        url: this.baseUrl + '/environment/api/v1/create',
        method: 'post',
        data: JSON.stringify(this.add),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        console.log(res)
      })
    },
    editProject () {
      this.editDialogVisible = false
      this.$axios({
        url: this.baseUrl + '/environment/api/v1/update',
        method: 'post',
        data: JSON.stringify(this.edit),
        headers: {
          'Content-Type': 'application/json;'
        }
      }).then((res) => {
        console.log(res)
      })
    }
  }
}
</script>
