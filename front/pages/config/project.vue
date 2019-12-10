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
      layout="total, prev, pager, next, jumper"
      :total="total"
      background
    >
    </el-pagination>
    <el-dialog
      title="添加项目"
      :visible.sync="addDialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form ref="form" :model="params" label-width="80px">
        <el-form-item label="团队名称">
          <el-input v-model="params.team"></el-input>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="params.project"></el-input>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="params.owner"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDialogVisible = false">确 定</el-button>
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
      params: {
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
      console.log(row)
      this.addDialogVisible = true
    },
    handleEdit (row) {
      console.log(row)
    },
    handleDelete (row) {
      console.log(row)
    },
    handleClose (value) {
      console.log(value)
    }
  }
}
</script>
