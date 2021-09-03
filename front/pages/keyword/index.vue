<template>
  <div>
    <el-row>
      <el-col :span="2" :offset="22">
        <el-button
          @click="createKeyword"
          type="primary"
          plain
        >
          创建关键字
        </el-button>
      </el-col>
    </el-row>
    <el-table
      :data="data"
      @selection-change="handleSelectionChange"
      v-loading="loading"
      element-loading-text="拼命加载中"
      style="width: 100%"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="80"
      />
      <el-table-column
        prop="name"
        label="关键字名称"
        width="180"
      />
      <el-table-column
        prop="description"
        label="关键字功能"
        width="450"
      />
      <el-table-column
        prop="created"
        label="创建时间"
        width="180"
      />
      <el-table-column
        prop="updated"
        label="更新时间"
        width="180"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
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
      cases: [],
      column: {},
      report: '',
      variables: '',
      loading: true,
      dialogFormVisible: false
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    createKeyword () {
      this.$router.push({
        path: '/keyword/create'
      })
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    refresh () {
      this.loading = true
      const params = {
        limit: this.limit,
        offset: this.page * this.limit
      }
      this.$axios
        .post('/api/v1/keyword/search', params)
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
    handleEdit (index, row) {
      this.$router.push({
        path: '/keyword/edit',
        query: {
          id: row.id
        }
      })
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        this.$axios({
          url: '/api/v1/keyword/delete',
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
              message: res.data.message,
              center: true
            })
          } else {
            this.$message({
              type: 'error',
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
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除',
          center: true
        })
      })
    },
    handleSelectionChange (value) {
      const index = []
      value.forEach((val, idx) => {
        this.data.forEach((v, i) => {
          if (val.id === v.id) {
            index.push(i)
          }
        })
      })
      this.cases = []
      const temp = index.sort()
      for (const i in temp) {
        this.cases.push(this.data[temp[i]].id)
      }
    }
  }
}
</script>
